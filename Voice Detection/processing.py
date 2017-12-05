import os
from math import cos
import numpy as np
import matplotlib.pyplot as plt
import struct
from ffmpy import FFmpeg
from ThinkDSP.code import thinkdsp, thinkplot

# All the utterances that were collected during tests were
# sampled at 11 kHz and each sample is represented in 8 bits. In this analysis the speech signals are divided into
# frames of length 256 samples (.023 sec.).
from ThinkDSP.code.thinkdsp import PI2

input_path = 'input.mp4'
audio_path = 'audio.wav'
frames_path = 'audio/frame%d.jpg '
images_path = 'images/frame%d.jpg'


# Input is the path to the video.
def convert(input_file):
    print('Converting Video into Audio and Images')
    os.mkdir('images')
    ff = FFmpeg(
        inputs={input_file: None},
        # 16kbit audio output and frames
        outputs={audio_path: ['-ar', '11000', '-ac', '2'],
                 images_path: ['-map', '0:v']
                 }
        )
    ff.run()


# Value from the research paper
samples_per_frame = 256


def split(input_file):
    # Splits audio into frames and multiplies by hamming window
    frames = []
    hammingwindow = []
    wave = thinkdsp.read_wave(input_file)

    # Some values that we might need
    totframes = len(wave.ts)
    framerate = wave.framerate
    length = totframes / framerate
    framelength = samples_per_frame / framerate
    numframes = int(length / framelength)

    print('Framelength:', framelength, 'seconds')
    print('Frames to calcuate:', numframes)

    for index in range(numframes):
        currentstart = index * framelength
        frames.append(wave.segment(start=currentstart, duration=framelength))

    for index in range(samples_per_frame):
        hammingwindow.append((0.54 + 0.46 * (cos(PI2 * index / 255))))

    for framenumber in range(len(frames)):
        for samplenumber in range(len(hammingwindow)):
            frames[framenumber].ts[samplenumber] *= hammingwindow[samplenumber]

    return frames


if os.path.exists(audio_path):
    print('Input file already converted')
else:
    convert(input_path)

frames = split(audio_path)

