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


class MelodySegment:
    def __init__(self, midi_pitches: [int], harmony: Harmony):
        self.midi_pitches = midi_pitches
        self.harmony = harmony
        pass

    def __len__(self):
        return len(self.midi_pitches)

    def __repr__(self):
        return f"Harmony:{self.harmony}, Melody={self.midi_pitches}"


class Score:
    melody_segs: [MelodySegment]

    def __init__(self, melodies: [MelodySegment] = None):
        self.melody_segs = melodies
        self._pointer = [0, 0]  # [nth segment, nth pitch within the nth segment]

    def build_melody_segments(self):
        # Reserved for transforming a midi file to MelodySegments and corresponding Harmonies
        pass

    def consume_curr_melody(self):
        curr_melody_pitch = self.melody_segs[self._pointer[0]][self._pointer[1]]
        self.advance()
        return curr_melody_pitch

    def advance(self):
        assert self.melody_segs is not None and type(self.melody_segs) == list
        # Advance _pointer
        if len(self.melody_segs[self._pointer[0]]) == self._pointer[1] + 1:
            self._pointer[0] += 1
            self._pointer[1] = 0
            if self._pointer[0] >= len(self.melody_segs):
                logger.info("Reached end of melody")
        else:
            self._pointer[1] += 1

    def curr_pointer(self):
        return self._pointer[0], self._pointer[1]


def create_score(melodies, chords):
    assert len(melodies) == len(chords)
    all_mseg = []
    for i, m in enumerate(melodies):
        mseg = MelodySegment(m, chords[i])
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
    # symbol = Harmony(hart_str='Bb:sus4(b9)')
    # print(symbol.harmony.prettify())
    # print("Hello world")

    for c in [
        'Eb:6', 'C:min7', 'G:min7', 'Eb:maj7', 'A:7(b9,#11)', 'Ab:maj9', 'Bb:sus4(b9)',
        'G:min11', 'C:7(b9)', 'Ab:maj9', 'Db:13', 'Eb:maj7', 'C:7(b9)', 'F:13', 'Bb:9', 'E:7(#9,b13)', 'Eb',
        'F:min9', 'Bb:9'
    ]:
        try:
            c = Harmony(hart_str=c)
        except Exception as e:
            logger.error("Cannot parse chord:", c)
    logger.info("parsed all chords!")


def main():
    # check_chord()
    star = ExampleScore.some_where_over_the_rainbow
    print(star)


if __name__ == "__main__":
    main()
