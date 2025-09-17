import os
import time

import fluidsynth
import mido

from taparr.util.logger import logger
from taparr.util.midi_util import choose_midi_input


def check_fluidsynth_library():
    if os.name == 'posix':
        possible_paths = [
            "/usr/local/lib/libfluidsynth.dylib",
            "/opt/homebrew/lib/libfluidsynth.dylib"
        ]
        found = False
        for path in possible_paths:
            if os.path.exists(path):
                found = True
                break

        if not found:
            raise Exception("FluidSynth library not found. If you're using macOS with Homebrew, "
                            "try running:\n\n    export DYLD_LIBRARY_PATH=/opt/homebrew/lib\n")
    return True


class Fluidx:
    fs = None  # fluidsynth instance

    def __init__(self, sf_path=None, sr=44100.0, gain=1.0, listen_chnl=None):
        if listen_chnl is None:
            listen_chnl = [0]
        self.fs = fluidsynth.Synth(samplerate=sr, gain=gain)
        self.fs.start()

        if sf_path is not None:
            logger.debug("Loading soundfont:", sf_path)
        self.load_sf(sf_path, channels=listen_chnl)

    def __del__(self):
        self.stop()

    def stop(self):
        if self.fs:
            self.fs.delete()
            self.fs = None
            logger.debug("Fluidx synthesizer stopped and resources released.")

    def load_sf(self, sf_path, channels=None):
        if channels == None:
            channels = [0]
        sfid = self.fs.sfload(sf_path)
        for c in channels:
            self.fs.program_select(c, sfid, 0, 0)

    def noteon(self, chan, key, vel):
        return self.fs.noteon(chan, key, vel)

    def noteoff(self, chan, key):
        return self.fs.noteoff(chan, key)

    def release_all(self, chan=0):
        self.fs.all_notes_off(chan)


def syn_midi_notes(notes):
    soundfont_path = '../../data/piano.sf2'
    fs = Fluidx(soundfont_path)

    import itertools
    flat_notes = list(itertools.chain(*notes))
    for nt in flat_notes:
        fs.noteon(0, nt, 60)
        time.sleep(0.3)
        fs.noteoff(0, nt)
        # time.sleep(0.5)


def example():
    """
    Toy example using Fluidx (pyFluidSynth)
    :return:
    """
    soundfont_path = '../../data/piano.sf2'
    fs = Fluidx(soundfont_path)
    # input("Start?")

    fs.noteon(0, 60, 60)
    fs.noteon(0, 64, 60)
    fs.noteon(0, 67, 60)
    time.sleep(1)
    # fs.noteoff(0, 60)
    # fs.noteoff(0, 64)
    # fs.noteoff(0, 67)

    while True:
        input("Release all current noteon?")
        fs.release_all(0)


def main():
    # example()
    syn_midi_notes(
        [[60, 60, 67, 67], [69, 69], [67], [65, 65], [64, 64], [62, 62], [60], [67, 67], [65, 65], [64, 64], [62],
         [67, 67], [65, 65], [64, 64], [62], [60, 60, 67, 67], [69, 69], [67], [65, 65], [64, 64], [62, 62], [60]]

    )
    pass


def synth_by_keyboard():
    soundfont_path = '../../data/piano.sf2'
    fs = Fluidx(soundfont_path)

    ports = choose_midi_input()
    input_port = mido.open_input(ports[0])
    output_port = mido.open_output(ports[1])

    while True:
        for msg in input_port.iter_pending():
            output_port.send(msg)


if __name__ == '__main__':
    # main()
    synth_by_keyboard()
