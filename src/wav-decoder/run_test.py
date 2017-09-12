from wav_decoder import WAVDecoder as WD

def test_all():
    """
    Function that runs all the tests
    """
    try:
        wd = WD('noaa_test.wav', 'noaa_test.png')
        return True
    except:
        return False

