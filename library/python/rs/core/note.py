import math

NOTES: list = [
    'C',
    'C#',
    'D',
    'D#',
    'E',
    'F',
    'F#',
    'G',
    'G#',
    'A',
    'A#',
    'B',
]


def index2frequency(note_index: int) -> float:
    return 440.0 * 2.0 ** ((note_index - 69) / 12.0)  # A4(69)を基準に計算


def index2pitch(note_index: int) -> float:
    return math.log(index2frequency(note_index))


def index2name(note_index: int) -> str:
    return NOTES[note_index % 12] + str(note_index // 12 - 1)


def name2index(note_name: str) -> int:
    note_name = note_name.upper()
    #
    note = note_name[0:-1]
    if note not in NOTES:
        return -1
    #
    try:
        octave = int(note_name[-1])
    except ValueError:
        return -1

    return NOTES.index(note) + 12 * (octave + 1)


if __name__ == "__main__":
    print(index2frequency(0))
    print(index2frequency(60))
    print(index2frequency(69))
    print(index2frequency(127))
    print(index2pitch(69))
    print(index2name(69))
    print(name2index('C#4'))
    print(name2index('A#3'))
