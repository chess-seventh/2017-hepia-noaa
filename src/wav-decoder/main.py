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

from wav_decoder import WAVDecoder

if __name__ == '__main__':
    if len(sys.argv) is not 3:
        print("Usage: python apt_wav2png.py <wav_filename> <png_filename>")
        print("<wav_filename>: Input WAV filename")
        print("<png_filename>: Output PNG filename")
        exit(0)

    wav_filename = sys.argv[1]
    png_filename = sys.argv[2]

    decoder = WAVDecoder(wav_filename, png_filename)
    decoder.decode()
    decoder.save()
