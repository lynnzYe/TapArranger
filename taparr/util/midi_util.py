"""
Author: Lynn Ye
Created on: 2025/9/15
Brief: 
"""
import mido


def generate_seq_from_pitch_class(pitch_list, octave=4):
    """
    Generate note sequence given pitch class input
    :param pitch_list:
    :param octave: default C4
    :return:
    """
    return [i % 12 + 12 * (i // 12) + 12 * (octave + 1) for i in pitch_list]


def generate_seq_from_pitch_name(pitch_name_list):
    """
    Generate note sequence given pitch class input
    :param pitch_name_list:
    :param octave: default C4
    :return:
    """
    return [pitch_name_to_midi(i) for i in pitch_name_list]


def pitch_name_to_midi(pname: str):
    note_map = {
        'C': 0,
        'D': 2,
        'E': 4,
        'F': 5,
        'G': 7,
        'A': 9,
        'B': 11
    }
    base = pname[0].upper()
    acc = None
    if len(pname) > 2:
        assert pname[1] in '#b'
        acc = pname[1]
        octave = int(pname[2:])
    else:
        octave = int(pname[1:])
    semitone = note_map[base]
    if acc:
        semitone += 1 if acc == '#' else - 1
    return (12 * (octave + 1)) + semitone


def midi_to_pitch_name(midi: int, all_sharp=True):
    midi_map = {
        0: 'C',
        2: 'D',
        4: 'E',
        5: 'F',
        7: 'G',
        9: 'A',
        11: 'B',
    }
    assert midi >= 0
    octave = midi // 12 - 1  # C4 = 60
    base = midi % 12
    if base in midi_map.keys():
        return f"{midi_map[base]}{octave}"
    # Now determine flat or sharp
    if all_sharp:
        return f"{midi_map[base - 1]}#{octave}"
    else:
        return f"{midi_map[base + 1]}b{octave}"


def generate_test_scores():
    # print([generate_seq_from_pitch_name(p) for p in [
    #     ['eb4'], ['eb5'], ['d5', 'bb4', 'c5'], ['d5', 'eb5'], ['eb4'], ['c5'], ['bb4'], ['e4'],
    #     ['c4'], ['ab4'], ['g4', 'eb4', 'f4'], ['g4', 'ab4'], ['f4', 'd4', 'eb4'], ['f4'], ['g4'], ['eb4'],
    #     ['c4', 'bb3'], ['d4', 'f4']
    # ]])
    print([generate_seq_from_pitch_name(p) for p in [
        ['c4', 'c4', 'g4', 'g4'], ['a4', 'a4'], ['g4'], ['f4', 'f4'], ['e4', 'e4'], ['d4', 'd4'], ['c4'],
        ['g4', 'g4'], ['f4', 'f4'], ['e4', 'e4'], ['d4'], ['g4', 'g4'], ['f4', 'f4'], ['e4', 'e4'], ['d4'],
        ['c4', 'c4', 'g4', 'g4'], ['a4', 'a4'], ['g4'], ['f4', 'f4'], ['e4', 'e4'], ['d4', 'd4'], ['c4']
    ]])


def is_note_on(m: mido.Message):
    return m.type == 'note_on' and m.velocity > 0


def is_note_off(m: mido.Message):
    return m.type == 'note_off' or (m.type == 'note_on' and m.velocity == 0)


def check_mido():
    mid = mido.MidiFile('/Users/kurono/Desktop/AG/magic-ldm_half_chnl_gen.mid')
    print(mid)


def array_choice(arr_begin, arr_end, hint=''):
    while True:
        try:
            in_choice = int(input(hint))
            if arr_begin <= in_choice < arr_end:
                return in_choice
            else:
                print(f"Invalid input. Please input a valid number between {arr_begin} and {arr_end - 1}")
        except Exception:
            print(f"Invalid input. Please input a valid number between {arr_begin} and {arr_end - 1}")


def choose_midi_input():
    # logger.info("Available MIDI input devices:")
    input_list = mido.get_input_names()
    output_list = mido.get_output_names()
    if len(input_list) == 0 or len(output_list) == 0:
        raise RuntimeError("No MIDI input/output device found.")
    print("=============================")
    print("Please choose an input device")
    for i, e in enumerate(input_list):
        print(i, ': ', e)
    input_choice = array_choice(0, len(input_list), '')
    print("=============================")
    print("Please choose an output device (If you see FluidSynth virtual port, plz choose this one.)")
    for i, e in enumerate(output_list):
        print(i, ': ', e)
    output_choice = array_choice(0, len(output_list), '')
    return [input_list[input_choice], output_list[output_choice]]


def main():
    """
    Problems with MIDI
    - cannot handle chord change within one melody note
    """
    # generate_test_scores()
    check_mido()


if __name__ == "__main__":
    main()
