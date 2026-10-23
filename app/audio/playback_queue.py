'''
Author: Ayemhenre Isikhuemhen
Date: 2026-10-18
LastEditors:
File Description: Manages the queue for generated speech audio.
'''

# imports
import sounddevice as sd

# play(): Takes in text sample, and tts speed and starts reading
def play(samples, sample_rate):
    sd.play(samples, sample_rate)

# stop(): Stops the reading process
def stop():
    sd.stop()