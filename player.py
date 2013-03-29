import time
import audio
from itertools import *
import operator

WEIGHTS = [1, 1, 1, 10, 15]
BASE_NOTES = [audio.NOTES[note] for note in ['C','D','E','G','A']]

def play_data(data):
    weighted = map(operator.mul, data, WEIGHTS)
    notes = map(operator.add, BASE_NOTES, weighted)
    notes = [audio.NOTES['C']] + notes  # So we always have a baseline
    audio.play(notes, duration=.15)

if __name__ == "__main__":
    lines = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 30, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [100, -20, 30, .5, .4],
        [0, 0, 0, 0, 0],
        [100, 100, 100, 10, 6],
        [0, 0, 0, 0, 0],
    ]
    for line in lines:
        play_data(line)
        time.sleep(.5)
