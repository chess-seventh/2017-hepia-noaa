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

class WAVFormatter(object):
    """
    Object to handle the a WAV file.
    Runs a series of tests to make sure the file is proper for handling.
    """
    def __init__(self, wav_fn):
        """
        Init and run tests.
        """
        self.filename = wav_fn
        self.workfile = 're.wav'

        self.rate = None

        self.samples = None
        self.signal = None

        self.health_check()

    def health_check(self):
        """
        Check health of input file.
        """
        with wave.open(self.filename, 'rb') as f:
            if f.getframerate() is not BASE_RATE:
                if not self.resample_rate():
                    print('something failed in resample')
                if not self.write_resampled():
                    print('something failed in writing resampled file.')

            if f.getnchannels() is not 1:
                if not to_mono():
                    print('something failed.')

    def write_resampled(self):
        """
        Write the workfile with the data.
        """
        # try:
        scipy.io.wavfile.write(self.workfile, self.rate, self.signal)
        return True
        # except:
        #     return False

    def resample_rate(self):
        """
        Resample to correct rate
        """
        # try:
        # with wave.open(self.filename, 'rb') as f:
        (self.rate, self.signal) = scipy.io.wavfile.read(self.filename)
        coef = BASE_RATE / float(self.rate)
        self.samples = int(coef * len(self.signal))
        self.signal = scipy.signal.resample(self.signal, self.samples)
        return True
        # except:
        #     return False

    def to_mono(self):
        """
        Stereo to Mono converter.
        """
        # try:
        with wave.open(self.filename, 'rb') as f:
            with wave.open(self.workfile, 'wb') as mono:
                mono.setparams(f.getparams())
                mono.setnchannels(1)
                mono.writeframes(audioop.tomono(f.readframes(float('inf')), f.getsampwidth(), 1, 1))
        return True

        # except:
        #     return False

    def get_wav(self):
        """
        Get the wav.
        """
        return scipy.io.wavfile.read(self.workfile)
