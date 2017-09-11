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

def decode(rate, signal):
    hilbert = scipy.signal.hilbert(signal)
    filtered = scipy.signal.medfilt(numpy.abs(hilbert), 5)
    reshaped = filtered.reshape(len(filtered) / 5, 5)
    digitized = _digitize(reshaped[:, 2])
    lines = int(len(digitized) / NOAA_LINE_LENGTH) # Get the amount of lines captured
    return digitized.reshape((lines, NOAA_LINE_LENGTH)) # Reshape the matrix

def _digitize(signal, plow=0.5, phigh=99.5):
    (low, high) = numpy.percentile(signal, (plow, phigh))
    delta = high - low

    data = numpy.round(255 * (signal - low) / delta)
    data[data < 0] = 0
    data[data > 255] = 255

    return data.astype(numpy.uint8)

def save_image(matrix, filename):
    image = PIL.Image.fromarray(matrix)
    if not filename is None:
        image.save(filename)

def wav2png(wav_filename, png_filename):
    (rate, signal) = scipy.io.wavfile.read(wav_filename)
    truncate = rate * int (len(signal) // rate)
    signal = signal[:truncate]
    m = decode(rate, signal) 
    save_image(m, png_filename)

if __name__ == '__main__':
    wav_filename = sys.argv[1]
    png_filename = sys.argv[2]
    wav2png(wav_filename, png_filename)