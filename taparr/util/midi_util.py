"""
Author: Lynn Ye
Created on: 2025/9/15
Brief: 
"""


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


def main():
    """
    Problems with MIDI
    - cannot handle chord change within one melody note
    """
    generate_test_scores()


if __name__ == "__main__":
    main()
