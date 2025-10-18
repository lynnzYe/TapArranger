"""
Author: Lynn Ye
Created on: 2025/9/8
Brief: 
"""
from enum import Enum

from harte.harte import Harte

from taparr.util.logger import logger
from taparr.util.midi_util import midi_to_pitch_name


class HarmonyType(Enum):
    major = 'maj'
    minor = 'min'
    aug = 'aug'
    dim = 'dim'


class Harmony:
    # Wrapper around Harte
    harte: Harte or None

    def __init__(self, hart_str=None, root=None, htype=None):
        if hart_str is not None:
            # initialize chord from Harte notation
            self.harte = Harte(hart_str)
        else:
            assert root is not None and htype is not None
            self.harte = Harte(midi_to_pitch_name(root % 12) + f':{htype}')

    def __str__(self):
        return self.harte.prettify()

    def pitch_classes(self):
        # Convert Harte notation to a list of pitch classes covering the harmony
        return self.harte.pitchClasses

    def npitch(self):
        return len(self.harte.pitchClasses)

    def nearest_midi(self, midi_pitch):
        """
        Return the nearest chord tone given input MIDI pitch
        :param midi_pitch:
        :return:
        """
        # Loop through all chord pitch classes and find the minimal distance
        target_class = midi_pitch % 12
        # Notice that when there are multiple valid candidates, it is resolved to the lower pitch ~ [0, 11]
        nearest_class = min(self.pitch_classes(),
                            key=lambda n: min(abs((n % 12) - target_class), 12 - abs((n % 12) - target_class)))
        candidate = nearest_class + midi_pitch // 12 * 12
        options = [candidate - 12, candidate, candidate + 12]
        return min(options, key=lambda x: abs(x - midi_pitch))

    def nearest_root(self, midi_pitch):
        # Loop through all chord pitch classes and find the minimal distance
        root_class = self.harte.pitchClasses[0]  # chord root pitch class (0-11)

        # Find the nearest octave of the root to the given midi_pitch
        candidate = root_class + (midi_pitch // 12) * 12
        options = [candidate - 12, candidate, candidate + 12]

        # Return the one closest to the midi_pitch
        return min(options, key=lambda x: abs(x - midi_pitch))

    def nearest_nth(self, midi_pitch, nth=0):
        """
        When nth=0, it trivially becomes nearest root function
        :param midi_pitch:
        :param nth:
        :return:
        """
        if nth >= len(self.harte.pitchClasses):
            nth = len(self.harte.pitchClasses) - 1
        assert nth >= 0
        # Loop through all chord pitch classes and find the minimal distance
        root_class = self.harte.pitchClasses[nth]  # chord root pitch class (0-11)

        # Find the nearest octave of the root to the given midi_pitch
        candidate = root_class + (midi_pitch // 12) * 12
        options = [candidate - 12, candidate, candidate + 12]

        # Return the one closest to the midi_pitch
        return min(options, key=lambda x: abs(x - midi_pitch))


class MelodySegment:
    def __init__(self, midi_pitches: [int], harmony: Harmony):
        self.midi_pitches = midi_pitches
        self.harmony = harmony
        pass

    def __len__(self):
        return len(self.midi_pitches)

    def __repr__(self):
        return f"Harmony:{self.harmony}, Melody={self.midi_pitches}"

    def __getitem__(self, index):
        return self.midi_pitches[index]


class Score:
    melody_segs: [MelodySegment]

    def __init__(self, melodies: [MelodySegment] = None):
        self.melody_segs = melodies
        self._pointer = [0, -1]  # [nth segment, nth pitch within the nth segment]
        # Define 0, -1 as the starting state, so that we can first advance then consume melody note
        # (Pointer always points to the current active melody note)

    def build_melody_segments(self):
        # Reserved for transforming a midi file to MelodySegments and corresponding Harmonies
        raise NotImplementedError

    def reset_pointer(self):
        self._pointer = [0, -1]

    def eos(self):
        return self._pointer == [-1, -1]

    def is_last_note(self):
        return (self._pointer[0] + 1 == len(self.melody_segs) and
                self._pointer[1] == len(self.melody_segs[self._pointer[0]]) - 1)

    def is_init_state(self):
        # Start of score
        return self._pointer == [0, -1]

    def get_curr_melody_segment(self) -> MelodySegment or None:
        if self.eos():
            return None
        return self.melody_segs[self._pointer[0]]

    def consume_curr_melody(self):
        if self.eos():
            return None
        self.advance()
        curr_melody_pitch = self.melody_segs[self._pointer[0]][self._pointer[1]]
        return curr_melody_pitch

    def advance(self):
        assert self.melody_segs is not None and type(self.melody_segs) == list
        # Advance _pointer
        if self._pointer[1] + 1 == len(self.melody_segs[self._pointer[0]]):
            self._pointer[0] += 1
            self._pointer[1] = 0
            if self._pointer[0] >= len(self.melody_segs):
                logger.info("Reached end of melody")
                self._pointer = [-1, -1]
        else:
            # Melody idx within segment size
            assert self._pointer[1] < len(self.melody_segs[self._pointer[0]])
            self._pointer[1] += 1

    def curr_pointer(self):
        return self._pointer[0], self._pointer[1]


def create_score(melodies, chords):
    assert len(melodies) == len(chords)
    all_mseg = []
    for i, m in enumerate(melodies):
        mseg = MelodySegment(m, Harmony(chords[i]))
        all_mseg.append(mseg)
    return Score(all_mseg)


class ExampleScore:
    star_m545 = create_score(
        [[60, 60, 67, 67], [69, 69], [67], [65, 65], [64, 64], [62, 62], [60],
         [67, 67], [65, 65], [64, 64], [62], [67, 67], [65, 65], [64, 64], [62],
         [60, 60, 67, 67], [69, 69], [67], [65, 65], [64, 64], [62, 62], [60]],
        [
            'C', 'F', 'C', 'G', 'C', 'G', 'C',
            'C', 'G', 'C', 'G', 'C', 'G', 'C', 'G',
            'C', 'F', 'C', 'G', 'C', 'G', 'C',
        ]
    )

    some_where_over_the_rainbow = create_score(
        [[63], [75], [74, 70, 72], [74], [75], [63], [72], [70], [64],
         [60], [68], [67, 63, 65], [67, 68], [65, 62, 63], [65], [67], [63],
         [60, 58], [62, 65]],
        [
            'Eb:6', 'C:min7', 'G:min7', 'Eb:maj7', 'A:7(b9,#11)', 'Ab:maj9', 'Bb:sus4(b9)',
            'G:min11', 'C:7(b9)', 'Ab:maj9', 'Db:13', 'Eb:maj7', 'C:7(b9)', 'F:13', 'Bb:9', 'E:7(#9,b13)', 'Eb',
            'F:min9', 'Bb:9'
        ]
    )


def check_chord():
    symbol = Harmony(hart_str='B:7(#9,b13)')

    m = symbol.nearest_midi(69)
    print(symbol.harte.prettify())
    print("Hello world")

    # for c in [
    #     'Eb:6', 'C:min7', 'G:min7', 'Eb:maj7', 'A:7(b9,#11)', 'Ab:maj9', 'Bb:sus4(b9)',
    #     'G:min11', 'C:7(b9)', 'Ab:maj9', 'Db:13', 'Eb:maj7', 'C:7(b9)', 'F:13', 'Bb:9', 'E:7(#9,b13)', 'Eb',
    #     'F:min9', 'Bb:9'
    # ]:
    #     try:
    #         c = Harmony(hart_str=c)
    #     except Exception as e:
    #         logger.error("Cannot parse chord:", c)
    # logger.info("parsed all chords!")


def main():
    check_chord()
    # star = ExampleScore.some_where_over_the_rainbow
    # print(star)


if __name__ == "__main__":
    main()
