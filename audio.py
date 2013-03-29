import time
import math
import struct
import ao
from itertools import *

FS = 48000
DEVICE = ao.AudioDevice('pulse')

NOTES = {
    'C': 261.626,
    'D': 293.665,
    'E': 329.628,
    'G': 391.995,
    'A': 440
}


def create_tone(frequency, amplitude, duration, fs):
    N = int(fs / frequency)
    T = int(frequency * duration)  # repeat for T cycles
    dt = 1.0 / fs
    # 1 cycle
    tone = (amplitude * math.sin(2 * math.pi * frequency * n * dt)
            for n in xrange(N))
    return list(chain.from_iterable(repeat(tuple(tone), T)))


def create_chord(freqs, amp, duration, fs):
    signals = [create_tone(freq, amp, duration, fs) for freq in freqs]
    return map(sum, zip(*signals))


def to_samples(tone):
    return ''.join(struct.pack('f', samp) for samp in tone)


def play(notes, amp=.5, duration=1):
    for note in notes:
        DEVICE.play(to_samples(create_tone(note, amp, duration, FS)))

if __name__ == "__main__":
    chord = [NOTES[note] for note in ['C', 'E', 'G']]
    play(chord)
