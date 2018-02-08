import os
from math import cos, log10
from numpy import abs
from ffmpy import FFmpeg
from ThinkDSP.code import thinkdsp, thinkplot

# All the utterances that were collected during tests were
# sampled at 11 kHz and each sample is represented in 8 bits. In this analysis the speech signals are divided into
# frames of length 256 samples (.023 sec.).
from ThinkDSP.code.thinkdsp import PI2

# Path to files
input_path = 'input.mp4'
audio_path = 'audio.wav'
images_path = 'images/frame%d.jpg'

# Value from the research paper
samples_per_frame = 256


# Input is the path to the video.
def convert(input_file):
    """Converts video into audio and images.

    :param input_file = path to video file

    outputs files into global directories.
    """

    if os.path.exists(audio_path):
        print('Output file already exists')
    else:
        print('Converting Video into Audio and Images')
        os.mkdir('images')
        ff = FFmpeg(
            inputs={input_file: None},
            # 11kbit audio output and frames
            outputs={audio_path: ['-ar', '11000', '-ac', '2'],
                     images_path: ['-map', '0:v']
                     }
            )
        ff.run()


def split(input_file):
    """ Splits audio file into frames
    and applies hamming window.

    :param input_file: path to audio file
    :return: array of waves (frames)
    """
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
            frames[framenumber].ys[samplenumber] *= hammingwindow[samplenumber]

    return frames


# computing energy
def energy(framearray):
    """ Calculates the energy of each frame

    :param framearray: array of waves (frames)
    :return: array of energy per frame
    """
    frame_energy = []
    for framenumber in range(len(framearray)):
        frame_energy.append([])
        for samplenumber in range(256):
            frame_energy[framenumber] += (framearray[framenumber].ys[samplenumber])**2
    return frame_energy


# creating spectrums, have to implement so only real
def fourier(framearray):
    """ Fourier transforms all waves from array.
    (Real values only)

    :param framearray: array of waves (frames)
    :return: array of FFT waves (spectrums)
    """
    fourier_frame = []
    for frame in framearray:
        index = frame.make_spectrum()
        index.hs = index.hs.real
        fourier_frame.append(index)
    return fourier_frame


# calculating logarithm of magntiude spectrum
def inverse_fourier(fourierarray):
    """ Apply logarithm to magnitude spectrum
    and IFFT to get output of homomorphic operation

    :param fourierarray: array of spectrums (frames)
    :return: array of IFFT spectrums (waves)
    """
    framearray = []
    for frame in fourierarray:
        framearray.append([])
        for samplenumber in range(len(frame.hs)):
            frame.hs[samplenumber] = 20 * log10(abs(frame.hs[samplenumber]))
    # ifft back
    for framenumber in range(len(framearray)):
        framearray[framenumber] = fourierarray[framenumber].make_wave()

    # fix first sample
    for frame in framearray:
        frame.ys[0] = 0
    return framearray


convert(input_path)
frames = split(audio_path)
frames[0].plot()
thinkplot.show()
energy = energy(frames)
fourier = fourier(frames)
frames = inverse_fourier(fourier)
frames[0].plot()
thinkplot.show()