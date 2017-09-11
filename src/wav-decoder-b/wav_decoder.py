# --------------------------------------------------
# @authors C. Rejas, F. Poroli, F. Piva
# @date 2017-09-11
# @project APT decoder - WAV to PNG
# --------------------------------------------------

import numpy
import scipy.io.wavfile
import scipy.signal
import sys
import PIL

NOAA_LINE_LENGTH = 2080

class WAVDecoder(object):

    def __init__(self, wav_filename, png_filename):
        """
        Constructor
        """
        (self.rate, self.signal) = scipy.io.wavfile.read(wav_filename)
        self.output_filename = png_filename
        self.matrix = None

    def save(self):
        """
        Method to save the decoded signal into a PNG file
        """
        if not self.matrix is None:
            image = PIL.Image.fromarray(self.matrix)
            if not self.output_filename is None:
                image.save(self.output_filename)
        else:
            print "Please decode first the signal"

    def decode(self):
        """
        Method to decode the signal
        """
        hilbert = scipy.signal.hilbert(self.signal)
        filtered = scipy.signal.medfilt(numpy.abs(hilbert), 5)
        reshaped = filtered.reshape(len(filtered) / 5, 5)
        self.signal = reshaped[:, 2]

        numerized = self.numerize()
        lines = int(len(numerized) / NOAA_LINE_LENGTH) # Get the amount of lines captured
        self.matrix = numerized.reshape((lines, NOAA_LINE_LENGTH)) # Reshape the matrix

    def numerize(self, plow=0.5, phigh=99.5):
        """
        Method to numerize the signal
        """
        (low, high) = numpy.percentile(self.signal, (plow, phigh))
        delta = high - low

        data = numpy.round(255 * (self.signal - low) / delta)
        data[data < 0] = 0
        data[data > 255] = 255

        return data.astype(numpy.uint8)
