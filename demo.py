"""
Author: Lynn Ye
Created on: 2025/9/16
Brief: 
"""
import argparse
import logging
import os
import time

from taparr.score import ExampleScore
from taparr.synthesizer.fluidx import check_fluidsynth_library, Fluidx
from taparr.tap_arranger import TapArranger
from taparr.util.logger import logger
from taparr.util.midi_util import choose_midi_input

check_fluidsynth_library()


def start_interactive_session(sf_path):
    assert os.path.exists(sf_path)
    synthesizer = Fluidx(sf_path, listen_chnl=[0, 1])
    time.sleep(0.5)

    in_port, out_port = choose_midi_input()

    taparr = TapArranger(in_port, out_port)
    score = ExampleScore.star_m545
    taparr.load_score(score, None)
    taparr.start_realtime_capture()

    input("\nPress [Enter] to stop\n")
    taparr.stop()
    synthesizer.stop()


def debug_main():
    start_interactive_session('data/piano.sf2')


def main():
    parser = argparse.ArgumentParser(
        description='Tap Arranger V0.1 Demo'
    )
    # Adding arguments
    parser.add_argument('--sf_path', type=str, required=True, help="Path to the sound font")
    args = parser.parse_args()
    logger.set_level(logging.INFO)
    start_interactive_session(sf_path=args.sf_path)


if __name__ == "__main__":
    # main()
    debug_main()
