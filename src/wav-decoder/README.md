[![Build Status](https://travis-ci.org/chess-seventh/2017-hepia-noaa.svg?branch=master)](https://travis-ci.org/chess-seventh/2017-hepia-noaa)

# WAV Decoder and WAV Formatter

## Usage

```
    python wav-decoder.py soundfile.wav image_out.png
```

## Virtualenv

- `virtualenv venv` to create a Python Virtual Environment.

- `source venv/bin/activate`

- `pip install -r requirements.txt`

- `python wav-decoder.py soundfile.wav image_out.png`

- To quit the virtualenv, you can simply close the terminal or type `deactivate`.



# TODO:


- [ ] .. Class to verify that the output has `jpg`,`png`,`bmp` format / Mime-Type.
- [ ] .. Check with previous step on how to plug it in to streamline it.


# Done


- [x] .. Refactor `def decode(self)` function.
- [x] .. PEP-8 style guide refactoring.
- [x] .. Create class to health check
- [x] .. Create class to handle main task
- [x] .. Implement both classes and run tests

