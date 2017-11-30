import os
import numpy as np
import matplotlib.pyplot as plt
import struct
import wave
from ffmpy import FFmpeg
from ThinkDSP import thinkdsp, thinkplot

# All the utterances that were collected during tests were
# sampled at 11 kHz and each sample is represented in 8 bits. In this analysis the speech signals are divided into
# frames of length 256 samples (.023 sec.).

input_path = 'input.mp4'
audio_path = 'audio.wav'
images_path = 'images/frame%d.jpg'


# Input is the path to the video.
def convert(input_file):
    os.mkdir('images')
    ff = FFmpeg(
        inputs={input_file: None},
        # 16kbit audio output and frames
        outputs={audio_path: ['-ar', '16000', '-ac', '2'],
                 images_path: ['-map', '0:v']
                 }
        )
    ff.run()


if os.path.exists(audio_path):
    print('Input file already converted')
else:
    convert(input_path)

pywave = wave.open(audio_path, 'rb')
frames = pywave.getnframes()
frequency = pywave.getframerate()
length = frames / frequency

# Values from the research paper
frames = round(length/0.023)
samples_per_frame = 128

# thinkwave = thinkdsp.read_wave(audio_path)
# spectrum = thinkwave.make_spectrum()

