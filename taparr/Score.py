"""
Author: Lynn Ye
Created on: 2025/9/8
Brief: 
"""
import mido


class Score:
    def __init__(self, midi_path):
        self.score = mido.MidiFile(midi_path)




def main():
    print("Hello, world!")


if __name__ == "__main__":
    main()
