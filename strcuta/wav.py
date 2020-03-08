# Copyright (C) Yuki Takagi 2020
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE_1_0.txt or copy at
# https://www.boost.org/LICENSE_1_0.txt)

import wave as _wave

class Type:
    def __init__(self, parameter, frames):
        assert parameter.nchannels == 1
        self.parameter = parameter
        self.frames = frames

    def __getitem__(self, key):
        if isinstance(key, slice):
            k = slice(key.start * self.parameter.sampwidth, key.stop * self.parameter.sampwidth)
            return Type(
                    parameter=self.parameter._replace(nframes=k.stop - k.start),
                    frames=self.frames[k])
        elif isinstance(key, int):
            return self.frames[key * self.parameter.sampwidth]
        else:
            raise "not an index"

    def write(self, outputpath):
        with _wave.open(outputpath, mode="wb") as w:
            w.setparams(self.parameter)
            w.writeframes(self.frames)

    _audio_stream = None

    def play(self):
        from sounddevice import RawOutputStream
        Type._audio_stream = Type._audio_stream or RawOutputStream(
                channels=self.parameter.nchannels,
                dtype='int' + str(8 * self.parameter.sampwidth),
                samplerate=self.parameter.framerate * self.parameter.nchannels,)
        Type._audio_stream.start()
        Type._audio_stream.write(self.frames)

def load(path):
    with _wave.open(path, mode="rb") as w:
        return Type(
                parameter=w.getparams(),
                frames=w.readframes(w.getnframes())
                )
