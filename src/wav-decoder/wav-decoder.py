import numpy
import scipy.io.wavfile
import scipy.signal

import PIL

import sys

import wave
import audioop

import time


class WavTransformer(object):
    """
    Object to handle the a WAV file.
    Runs a series of tests to make sure the file is proper for handling.
    """

    def __init__(self, fn):
        """
        Init and run tests.
        """
        self.RATE = 20800
        self.NOAA_LINE_LENGTH = 2080  # From documentation.

        self.monofile = None
        self.framerate = None

        self.original_file = fn
        self.workfile = "workfile.wav"

        self.run_tests()

        if not self.monofile and not self.framerate:
            if not self.standardize():
                print("something went wrong in standardize().")


    def standardize(self):
        """
        Run the Standardisation process.
        """
        try:
            if not self.monofile:
                if not to_mono():
                    print("something failed while converting to mono.")

            if not self.framerate:
                if not self.resample():
                    print("something went wrong with the resampling.")
        except:
            return False

    def run_tests(self):
        """
        Check health of input file.
        """
        with wave.open(self.original_file, 'rb') as cur_file:
            if cur_file.getframerate() is not self.RATE:
                self.framerate = False

            if cur_file.getnchannels() is not 1:
                self.monofile = False

    def to_mono(self):
        """
        Stereo to Mono converter.
        """
        try:
            with wave.open(self.workfile, 'wb') as mono:
                print("to mono !")
                mono.setparams(cur_file.getparams())
                mono.setnchannels(1)
                mono.writeframes(audioop.tomono(cur_file.readframes(
                    float('inf')), cur_file.getsampwidth(), 1, 1))
                self.monotest = True
            return True

        except:
            return False

    def resample(self):
        """
        Resample to correct bitrate.
        """
        try:
            if self.monofile:
                (rate, self.signal) = scipy.io.wavfile.read(self.workfile)
            else:
                (rate, self.signal) = scipy.io.wavfile.read(self.original_file)

            coef = self.RATE / rate
            samples = int(coef * len(self.signal))

            self.signal = scipy.signal.resample(self.signal, samples)
            truncate = self.RATE * int(len(self.signal) // self.RATE)
            self.signal = self.signal[:truncate]
            return True

        except:
            return False

    def decode(self, outfile=None):
        """
        Decoder function from wav to png.
        """
        try:
            hilbert = scipy.signal.hilbert(self.signal)
            filtered = scipy.signal.medfilt(numpy.abs(hilbert), 5)
            reshaped = filtered.reshape(len(filtered) // 5, 5)
            digitized = self.digi(reshaped[:, 2])
            lines = int(len(digitized) / self.NOAA_LINE_LENGTH)

            matrix = digitized.reshape((lines, self.NOAA_LINE_LENGTH))
            image = PIL.Image.fromarray(matrix)
            if not outfile is None:
                image.save(outfile)
            image.show()
            return matrix

        except:
            print("somehting went wrong while decoding the file.")
            return False

    def digi(self, signal, plow=0.5, phigh=99.5):
        """
        Digitalize the signal.
        """
        (low, high) = numpy.percentile(signal, (plow, phigh))
        delta = high - low
        data = numpy.round(255 * (signal - low) / delta)
        data[data < 0] = 0
        data[data > 255] = 255
        return data.astype(numpy.uint8)

if __name__ == '__main__':
    WavTransformer = WavTransformer(sys.argv[1])

    if len(sys.argv) > 2:
        outfile = sys.argv[2]
    else:
        outfile = None

    if not WavTransformer.decode(outfile):
        print("Failed. Exiting now. Try again, insert coins.")
