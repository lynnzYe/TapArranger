"""
Author: Lynn Ye
Created on: 2025/9/15
Brief: 
"""
import mido

from taparr_context import TapArrContext


class TapArranger:
    melody_range = [60, 128]
    acc_range = [0, 59]
    tap_map = {}  # Record active note-on events
    context: TapArrContext = None

    def __init__(self, input_port_name, output_port_name, chnl=0,
                 melody_range=None, acc_range=None):
        self.input_port = mido.open_input(input_port_name)
        self.output_port = mido.open_output(output_port_name)

        if melody_range is not None:
            self.melody_range = melody_range
        if acc_range is not None:
            self.acc_range = acc_range

    def tap_score(self):
        # Query score for current melody pointer
        # Then, send MIDI note-on with that midi pitch and incoming tap.
        pass

    def tap_arr(self):
        # Query arranger and obtain the corresponding MIDI pitch
        pass


def main():
    print("Hello, world!")


if __name__ == "__main__":
    main()
