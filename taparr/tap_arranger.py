"""
Author: Lynn Ye
Created on: 2025/9/15
Brief: 
"""

import time
from threading import Thread, Event

import mido

from taparr.arranger import Arranger
from taparr.score import Score
from taparr.taparr_context import TapArrContext
from taparr.util.logger import logger
from taparr.util.midi_util import is_note_on, is_note_off


class MidiBinder:
    class _RevView:
        def __init__(self, rev):
            self._rev = rev

        def __contains__(self, item):
            return item in self._rev

        def __getitem__(self, item):
            return self._rev[item]

        def keys(self):
            return self._rev.keys()

        def values(self):
            return self._rev.values()

        def items(self):
            return self._rev.items()

    def __init__(self, data=None):
        self._fwd = {}
        self._rev = {}
        if data:
            for k, v in data.items():
                self[k] = v  # use __setitem__
        self.pitch_to_midi = MidiBinder._RevView(self._rev)

    def __setitem__(self, key, value):
        if key in self._fwd:
            del self._rev[self._fwd[key]]
        if value in self._rev:
            del self._fwd[self._rev[value]]
        self._fwd[key] = value
        self._rev[value] = key

    def __getitem__(self, key):
        return self._fwd[key]

    def __delitem__(self, key):
        val = self._fwd.pop(key)
        del self._rev[val]

    def __contains__(self, key):
        return key in self._fwd

    def items(self):
        return self._fwd.items()


class TapArranger:
    melody_range = [60, 128]
    acc_range = [0, 59]
    tap_map = MidiBinder()  # map input MIDI to pred MIDI, tracks current active MIDI note on
    context: TapArrContext = None
    score: Score = None
    arranger: Arranger = None
    loop: bool = False  # if all the melodies are played, should we start once more from the beginning

    def __init__(self, input_port_name, output_port_name, score_chnl=0, arr_chnl=0,
                 melody_range=None, loop=False):
        self.input_port = mido.open_input(input_port_name)
        self.output_port = mido.open_output(output_port_name)

        self.melody_range = melody_range if melody_range is not None else self.melody_range

        self.score_chnl = score_chnl
        self.arr_chnl = arr_chnl
        self.loop = loop

        self.start_time = time.time()

        # Threads
        self.is_active = Event()
        self.capture_thread = Thread(target=self.listen)

        self._stopped = True

    def load_score(self, score: Score, arr: Arranger):
        self.score = score
        self.arranger = arr

    def start_realtime_capture(self):
        self._stopped = False
        self.is_active.set()
        self.capture_thread.start()
        self.start_time = time.time()
        logger.info("TapArranger system started")

    def is_melody(self, m: mido.Message):
        if self.melody_range[0] <= m.note <= self.melody_range[1]:
            return True
        return False

    def listen(self):
        while self.is_active.is_set():
            if self.input_port is None:
                break
            try:
                for msg in self.input_port.iter_pending():
                    if not self.is_active.is_set():
                        break
                    logger.debug('Received input:', msg)
                    # real-time melody / arrangement synthesis
                    if is_note_on(msg):
                        if self.is_melody(msg):
                            self.tap_melody(msg)
                        else:
                            self.tap_arr(msg)
                    elif is_note_off(msg):
                        self.release(msg)
                    else:
                        self.output_port.send(msg)
                    # Update history
                    self.context  # do something with arr context

            except (EOFError, OSError) as e:
                # Handle port closing or other IO errors
                logger.debug(f"Port error during listen: {e}")

    def stop(self):
        if self._stopped:
            return
        logger.info("Stopping TapArranger...")
        self.is_active.clear()
        if self.input_port is not None:
            self.input_port.close()
            logger.debug("MIDI input port closed.")
            self.input_port = None

        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=2.0)  # Add timeout to prevent hanging
            if self.capture_thread.is_alive():
                logger.warn("Capture thread didn't stop gracefully within timeout")
            else:
                logger.debug("Realtime capture stopped.")
            self.capture_thread = None

        if self.output_port is not None:
            self.output_port.close()
            logger.debug("MIDI output port closed.")
            self.output_port = None

        self._stopped = True

    def send_noteon(self, tgt_pitch, corresp_msg: mido.Message, chnl, time_delay=0):
        if tgt_pitch in self.tap_map.pitch_to_midi:
            # Case when there's already a note-on with tgt_pitch -> immediately end the current noteon
            end_note = mido.Message(type='note_off', note=tgt_pitch, channel=chnl, time=time_delay)
            self.output_port.send(end_note)
            # Update tap_map
            self.tap_map[corresp_msg.note] = tgt_pitch
            # Send a new note on
            self.output_port.send(
                mido.Message(type=corresp_msg.type, note=tgt_pitch, channel=chnl, velocity=corresp_msg.velocity,
                             time=time_delay))
        else:
            tgt_event = mido.Message(type=corresp_msg.type, note=tgt_pitch, channel=chnl,
                                     velocity=corresp_msg.velocity, time=time_delay)
            self.output_port.send(tgt_event)
            self.tap_map[corresp_msg.note] = tgt_pitch

    def tap_melody(self, msg: mido.Message):
        # Query score for current melody pointer
        if self.score is None:
            return
        elif self.score.is_last_note() and self.loop:
            self.score.reset_pointer()
        elif self.score.eos():
            logger.debug("End of Score. No more notes to play")
            return
        tgt_pitch = self.score.consume_curr_melody()
        if tgt_pitch is not None:
            self.send_noteon(tgt_pitch, msg, chnl=self.score_chnl)

    def tap_arr(self, msg: mido.Message):
        # Query arranger and obtain the corresponding MIDI pitch
        if self.score is None or self.score.eos() or self.score.is_init_state():
            return  # Start arranging only after the melody note is hit
        tgt_midi = self.arranger.predict_midi(msg, self.score, self.context)
        self.send_noteon(tgt_midi, msg, chnl=self.arr_chnl)  # TODO @Bmois may require special logic
        # (instead of renewing same pitch onset, keep it.

    def release(self, msg: mido.Message, time_delay=0):
        if msg.note not in self.tap_map:
            # logger.warn("cannot find tap map key with", msg.note)
            return
        tgt_event = mido.Message(type=msg.type, note=self.tap_map[msg.note], channel=self.score_chnl,
                                 velocity=0, time=time_delay)
        del self.tap_map[msg.note]
        self.output_port.send(tgt_event)


def main():
    print("Hello, world!")


if __name__ == "__main__":
    main()
