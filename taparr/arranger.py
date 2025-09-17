"""
Author: Lynn Ye
Created on: 2025/9/15
Brief: 
"""
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


def main():
    print("Hello, world!")


if __name__ == "__main__":
    main()
