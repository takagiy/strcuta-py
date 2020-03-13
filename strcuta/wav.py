# Copyright (C) Yuki Takagi 2020
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE_1_0.txt or copy at
# https://www.boost.org/LICENSE_1_0.txt)

import wave as _wave
from strcuta import cursor as _cursor
from strcuta import frq as _frq

class Type:
    def __init__(self, frq, parameter, frames):
        assert parameter.nchannels == 1
        self.frq = frq
        self.parameter = parameter
        self.frames = frames

    def __len__(self):
        return self.parameter.nframes

    def __getitem__(self, key):
        if isinstance(key, slice):
            k = _cursor.resolve_slice(key, self.parameter.framerate, self.parameter.sampwidth)
            f = self.frames[k]
            kf = _cursor.resolve_slice(key, self.frq.samplerate, 1 / self.frq.sample_interval)
            return Type(
                    frq=self.frq[kf],
                    parameter=self.parameter._replace(nframes=int(len(f) / self.parameter.sampwidth)),
                    frames=f)
        else:
            return self.frames[_cursor.resolve_to_slice(key, self.parameter.framerate, self.parameter.sampwidth)]

    def __add__(self, rhs):
        return Type(
                frq=self.frq + rhs.frq,
                parameter=self.parameter._replace(nframes=self.parameter.nframes + rhs.parameter.nframes),
                frames=self.frames + rhs.frames)

    def __mul__(self, n):
        return Type(
                frq=self.frq * n,
                parameter=self.parameter._replace(nframes=self.parameter.nframes * n),
                frames=self.frames * n
                )

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

def _frq_path(wav_path):
    return wav_path[:-4] + "_wav.frq"

def load(path):
    with _wave.open(path, mode="rb") as w:
        return Type(
                frq=_frq.load(_frq_path(path)),
                parameter=w.getparams(),
                frames=w.readframes(w.getnframes())
                )

def write(wav, outputpath):
    wav.write(outputpath)
