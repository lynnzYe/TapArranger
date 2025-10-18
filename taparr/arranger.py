"""
Author: Lynn Ye
Created on: 2025/9/15
Brief: 
"""
import random

import mido
from overrides import overrides

from taparr.score import Score
from taparr.taparr_context import TapArrContext


class Arranger:
    def __init__(self):
        pass

    def predict_midi(self, msg: mido.Message, score: Score, context: TapArrContext):
        raise NotImplementedError
        # return 60

    # def update_context(self, ):


class NearestArranger(Arranger):
    """
    Given a MIDI input, find the nearest available pitch given chord information
    """

    def __init__(self):
        super().__init__()

    @overrides
    def predict_midi(self, msg: mido.Message, score: Score, context: TapArrContext):
        # Extract current harmony information
        curr_melody_seg = score.get_curr_melody_segment()
        return curr_melody_seg.harmony.nearest_midi(msg.note)


class NearestRootArranger(Arranger):
    """
    Given a MIDI input, find the nearest available pitch given chord information
    """

    def __init__(self):
        super().__init__()

    @overrides
    def predict_midi(self, msg: mido.Message, score: Score, context: TapArrContext):
        # Define all notes below C3 (including) to be biased towards the root of the chord
        curr_melody_seg = score.get_curr_melody_segment()
        if msg.note <= 48:
            return curr_melody_seg.harmony.nearest_root(msg.note)
        return curr_melody_seg.harmony.nearest_midi(msg.note)


class ProbabilisticArranger(Arranger):
    """
    Given a MIDI input, find the nearest available pitch given chord information
    """

    def __init__(self):
        super().__init__()

    @overrides
    def predict_midi(self, msg: mido.Message, score: Score, context: TapArrContext):
        # Define all notes below C3 (including) to be biased towards the root of the chord
        curr_melody_seg = score.get_curr_melody_segment()
        harmony = curr_melody_seg.harmony
        if msg.note <= 48:
            # bias towards root for bass
            return harmony.nearest_root(msg.note)
        else:
            if random.random() < 0.6:
                # Prefer third to seventh
                return harmony.nearest_nth(msg.note, 1) if random.random() < 0.7 \
                    else harmony.nearest_nth(msg.note, 3)
            else:
                # Select the rest
                return harmony.nearest_nth(msg.note, random.randrange(min(2, harmony.npitch()), harmony.npitch()))


def main():
    print("Hello, world!")


if __name__ == "__main__":
    main()
