# Copyright (C) Yuki Takagi 2020
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE_1_0.txt or copy at
# https://www.boost.org/LICENSE_1_0.txt)

import wave
from os import path
from collections import namedtuple

from strcuta import otoini
from strcuta import prefixmap
from strcuta import frq

class Cursors:
    def __init__(self, start, end_ovl, end_pre, end_con, end):
        self.start = start
        self.end_ovl = end_ovl
        self.end_pre = end_pre
        self.end_con = end_con
        self.end_fixed = self.end_con
        self.end = end

class Counts:
    def __init__(self, pre, ovl, con, full):
        self.pre = pre
        self.ovl = ovl
        self.con = con
        self.fixed = self.con
        self.full = full
        self.vow = full - con
        self.stretchable = self.vow

_WaveParams = namedtuple("_wave_params", "nchannels sampwidth framerate nframes comptype compname")

class Wave:
    def __init__(self, parameter, frames):
        assert parameter.nchannels == 1
        self.parameter = parameter
        self.frames = frames

    @staticmethod
    def make(wave_):
        return Wave(
                parameter=wave_.getparams(),
                frames=wave_.readframes(wave_.getnframes())
                )

    def __getitem__(self, key):
        if isinstance(key, slice):
            k = slice(key.start * self.parameter.sampwidth, key.stop * self.parameter.sampwidth)
            return Wave(
                    parameter=self.parameter._replace(nframes=k.stop - k.start),
                    frames=self.frames[k])
        elif isinstance(key, int):
            return self.frames[key * self.parameter.sampwidth]
        else:
            raise "not an index"

    def write(self, outputpath):
        with wave.open(outputpath, mode="wb") as w:
            w.setparams(self.parameter)
            w.writeframes(self.frames)

    _audio_stream = None

    def play(self):
        from sounddevice import RawOutputStream
        Wave._audio_stream = Wave._audio_stream or RawOutputStream(
                channels=self.parameter.nchannels,
                dtype='int' + str(8 * self.parameter.sampwidth),
                samplerate=self.parameter.framerate * self.parameter.nchannels,)
        Wave._audio_stream.start()
        Wave._audio_stream.write(self.frames)


def _ms2nframes(rate, millisec):
    return round(rate * millisec / 1000)

class Type:
    def __init__(self, rootdir, oto, prefix):
        self.rootdir = rootdir
        self.oto = oto
        self.prefix = prefix

    def voice(self, spell, key):
        info = self.oto[spell + self.prefix[key]]
        with wave.open(path.join(self.rootdir, info.source), mode="rb") as w:
            w = Wave.make(w)

            rate = w.parameter.framerate
            nframes = w.parameter.nframes

            nf_offset = _ms2nframes(rate, info.offset)
            nf_con = _ms2nframes(rate, info.consonant)
            nf_pre = _ms2nframes(rate, info.preutterance)
            nf_ovl = _ms2nframes(rate, info.overlap)
            if info.duration != None:
                nf_used = _ms2nframes(rate, info.duration)
            else:
                nf_cutoff = _ms2nframes(rate, info.cutoff)
                nf_used = nframes - nf_offset - nf_cutoff
            
            w = w[nf_offset : nf_offset + nf_used]

        return Voice(
                wave=w,
                count=Counts(
                    pre=nf_pre,
                    ovl=nf_ovl,
                    con=nf_con,
                    full=nf_used,
                    )
                )

class Voice(Wave):
    def __init__(self, wave, count):
        self.count = count
        self.cursor = Cursors(
                start=0,
                end_ovl=count.ovl,
                end_pre=count.pre,
                end_con=count.con,
                end=count.full
                )
        super().__init__(
                parameter=wave.parameter,
                frames=wave.frames)

    def range_pre(self):
        return slice(self.cursor.start, self.cursor.end_pre)

    def range_ovl(self):
        return slice(self.cursor.start, self.cursor.end_ovl)

    def range_con(self):
        return slice(self.cursor.start, self.cursor.end_con)

    def range_fixed(self):
        return self.range_fixed()

    def range_vow(self):
        return slice(self.cursor.end_con, self.cursor.end)

    def range_stretchable(self):
        return self.range_vow()

    def range_intime(self):
        return slice(self.cursor.end_pre, self.cursor.end)


    def pre(self):
        return self[self.range_pre()]

    def ovl(self):
        return self[self.range_ovl()]

    def con(self):
        return self[self.range_con()]

    def fixed(self):
        return self.con()

    def vow(self):
        return self[self.range_vow()]

    def stretchable(self):
        return self.vow()

    def intime(self):
        return self[self.range_intime()]


def load(path_):
    oto = otoini.load_recursive(path_)
    prefix = prefixmap.load(path.join(path_, 'prefix.map'))
    return Type(
            rootdir=path_,
            oto=oto,
            prefix=prefix)
