import numpy
import scipy.io.wavfile
import scipy.signal

import PIL

import sys

import wave
import audioop

import time

BASE_RATE = 20800
NOAA_LINE_LENGTH = 2080

class WavFormatter(object):
    """
    Object to handle the a WAV file.
    Runs a series of tests to make sure the file is proper for handling.
    """
    def __init__(self, wav_fn):
        """
        Init and run tests.
        """
        self.filename = wav_fn
        self.workfile = 'resampled.wav'

        self.rate = None

        self.samples = None
        self.signal = None

        self.health_check()

    def get_wav(self):
        """
        Get the wav.
        """
        return scipy.io.wavfile.read(self.workfile)

    def health_check(self):
        """
        Check health of input file.
        """
        with wave.open(self.filename, 'rb') as f:
            if f.getframerate() is not BASE_RATE:
                if not self.resample_rate(f):
                    print('something failed in resample')
                if not self.write_resampled():
                    print('something failed in writing resampled file.')

            if f.getnchannels() is not 1:
                if not to_mono(f):
                    print('something failed.')

    def write_resampled(self):
        """
        Write the workfile with the data.
        """
        try:
            scipy.io.wavfile.write(self.workfile, self.rate, self.signal)
            return True
        except:
            return False

    def resample_rate(self, f):
        """
        Resample to correct rate
        """
        try:
            if not f:
                (self.rate, self.signal) = scipy.io.wavfile.read(f)
                coef = BASE_RATE / float(self.rate)
                self.samples = int(coef * len(self.signal))
                self.signal = scipy.signal.resample(self.signal, self.samples)
                return True
        except:
            return False

    def to_mono(self, f):
        """
        Stereo to Mono converter.
        """
        try:
            with wave.open(self.workfile, 'wb') as mono:
                mono.setparams(f.getparams())
                mono.setnchannels(1)
                mono.writeframes(audioop.tomono(f.readframes(float('inf')), f.getsampwidth(), 1, 1))
            return True

        except:
            return False
