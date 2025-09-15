"""
Author: Lynn Ye
Created on: 2025/9/8
Brief: 
"""
from enum import Enum

import mido


class HarmonyType(Enum):
    major = 0
    minor = 1
    aug = 2
    dim = 3


class Harmony:
    root: int
    htype: HarmonyType

    def __init__(self, root, htype):
        self.root = root
        self.htype = htype


class MelodySegment:
    def __init__(self, midi_pitches, harmony_type, harte=None):
        self.midi_pitches = midi_pitches
        self.htype = harmony_type
        self.harte = harte
        pass


class Score:
    melody_segs: [MelodySegment]

    def __init__(self, midi_path):
        self.score = mido.MidiFile(midi_path)
        self.melody_segs = None
        self._pointer = [0, 0]  # [nth segment, nth pitch within the nth segment]

    def build_melody_segments(self):
        pass

    def advance(self):
        # Advance _pointer
        pass


def main():
    print("Hello, world!")


if __name__ == "__main__":
    main()
