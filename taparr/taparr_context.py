"""
Author: Lynn Ye
Created on: 2025/9/15
Brief: 
"""
from dataclasses import dataclass, field


@dataclass
class TapArrContext:
    def __init__(self):
        self.acc_history = field(default_factory=list)  # Actual synthesized notes
        self.tap_history = field(default_factory=list)  # User tapping input (pitched midi)

    def append_tap_history(self, taps):
        pass

    def append_acc_history(self, arranged):
        assert len(self.acc_history) + len(arranged) == len(self.tap_history)
        pass

    # timestamp of the last active arr tap is important -> tells if this is a chord e.g. <20ms
    # ask Roger(what is a good empirical threshold value?)


def main():
    print("Hello, world!")


if __name__ == "__main__":
    main()
