import os
from math import cos, log10
from numpy import abs
from ffmpy import FFmpeg
from ThinkDSP.code import thinkdsp, thinkplot

# All the utterances that were collected during tests were
# sampled at 11 kHz and each sample is represented in 8 bits.
# In this analysis the speech signals are divided into
# frames of length 256 samples (.023 sec.).
from ThinkDSP.code.thinkdsp import PI2

# Path to files
input_path = 'input.mp4' # os.path.join(uploads,filename
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

    return frames


# Computing Hamming Window
def applyhamming(framearray):
    """Multiplying each frame with a hamming window

    :param framearray: array of waves (frames)
    :return: array of hamming window filtered frames
    """

    hammingwindow = []

    # Setup hamming window array
    for index in range(samples_per_frame):
        hammingwindow.append((0.54 + 0.46 * (cos(PI2 * index / 255))))

    # Multiplying each frame with the hamming window
    for framenumber in range(len(frames)):
        for samplenumber in range(len(hammingwindow)):
            frames[framenumber].ys[samplenumber] *= hammingwindow[samplenumber]

    return framearray


# Computing Energy
def energy(framearray):
    """ Calculates the energy of each frame

    :param framearray: array of waves (frames)
    :return: array of energy per frame
    """

    frame_energy = []

    for framenumber in range(len(framearray)):
        frame_energy.append([0])
        for samplenumber in range(samples_per_frame):
            frame_energy[framenumber] += ((framearray[framenumber].ys[samplenumber])**2)
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

    # Computing logarithm of the magnitude spectrum of the frame
    # 20log10(frame) == 20log10(i) i sample between 0 - 255
    # Other spectral analysis uses 10log10
    for frame in fourierarray:
        framearray.append([])
        for samplenumber in range(len(frame.hs)):
            frame.hs[samplenumber] = 20 * log10(abs(frame.hs[samplenumber]))

    # ifft back
    for framenumber in range(len(framearray)):
        framearray[framenumber] = fourierarray[framenumber].make_wave()

    # fix first sample in first frame
    for frame in framearray:
        frame.ys[0] = 0

    return framearray


# High time sampling for the peak. Different between male and women/children
def sampling(framearray):

    # Ask and check if subject is male, female, or a child
    char = input("Male, female, or child subject?"
                 "(m for Male, f for Female, c for Child)")

    if char == 'm':
        index = 40
    elif char == 'f' or 'c':
        index = 20

    framesample = []

    # Split frames and calculate maximum amplitude
    for frame in framearray:
        framesplit = frame.ys[index:int(samples_per_frame / 2)].tolist()
        value = max(framesplit)
        maxindex = framesplit.index(value) + index
        framesample.append(thinkdsp.Wave(frame.ys[maxindex],
                                         frame.ts[maxindex],
                                         frame.framerate))

    # Amplitude of the signal at Pitch Period
    # Pitch Period is index(framesample) (Not sure what this is yet)
    # F(Pitch Period) is frame number with pitch period given.

    return framesample

maxAmp = 0

# Calculate mean energy of utterance
def meanenergy(energyarray):

    total1 = []
    total2 = 0
    for energy in energyarray:
        mean = float(energy/len(energyarray))
        total2 += energy
        total1.append(mean)

    total2 /= len(energyarray)

    print("Mean Energy stuff:")
    print(total1)
    print(total2)


def maxpitchamp(framearray):

    maxpitch = []

    for frames in framearray:
        maxpitch.append(max(frames.ys))
        print(frames.ts)

    print("Max Pitch Amp stuff:")
    print(maxpitch)

    maxAmp = max(maxpitch)
    print(maxAmp)


def vowelduration(framearray):

    vowels = []
    v = 0

    threshold = 0.1 * maxAmp
    for frames in framearray:

        for sample in frames.ys:
            if sample >= threshold:
                v += 1

        vowels.append(0.23*(v/2))
        v = 0

    print("Vowel Duration stuff:")
    print(vowels)


convert(input_path)
frames = split(audio_path)
filteredframes = applyhamming(frames)
energy = energy(filteredframes)
fourier = fourier(filteredframes)
frames = inverse_fourier(fourier)
sampling(frames)
meanenergy(energy)
maxpitchamp(frames)
vowelduration(frames)
