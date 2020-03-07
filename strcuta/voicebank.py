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
    def __init__(self, start, end_overlapping, end_prepronounced, end_fixed, end):
        self.start = start
        self.end_overlapping = end_overlapping
        self.end_prepronounced = end_prepronounced
        self.end_fixed = end_fixed
        self.end = end

class Counts:
    def __init__(self, prepronounced, overlapping, fixed, full):
        self.prepronounced = prepronounced
        self.overlapping = overlapping
        self.fixed = fixed
        self.full = full
        self.stretchable = full - fixed

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

def _ms2nframes(rate, millisec):
    return round(rate * millisec / 1000)

class Type:
    def __init__(self, rootdir, oto, prefix):
        self.rootdir = rootdir
        self.oto = oto
        self.prefix = prefix

    def voice(self, spell, key):
        info = self.oto[spell + self.prefix[key]]
        with wave.open(path.join(self.rootdir, info["source"]), mode="rb") as w:
            w = Wave.make(w)

            rate = w.parameter.framerate
            nframes = w.parameter.nframes

            nf_left_margin = _ms2nframes(rate, info["leftMargin"])
            nf_fixed = _ms2nframes(rate, info["fixed"])
            nf_prepronounced = _ms2nframes(rate, info["prepronounced"])
            nf_overlapping = _ms2nframes(rate, info["overlapping"])
            if info["duration"] != None:
                nf_used = _ms2nframes(rate, info["duration"])
            else:
                nf_right_margin = _ms2nframes(rate, info["rightMargin"])
                nf_used = nframes - nf_left_margin - nf_right_margin
            
            w = w[nf_left_margin : nf_left_margin + nf_used]

        return Voice(
                wave=w,
                count=Counts(
                    prepronounced=nf_prepronounced,
                    overlapping=nf_overlapping,
                    fixed=nf_fixed,
                    full=nf_used,
                    )
                )

class Voice:
    def __init__(self, wave, count):
        self.wave = wave
        self.count = count
        self.cursor = Cursors(
                start=0,
                end_overlapping=count.overlapping,
                end_prepronounced=count.prepronounced,
                end_fixed=count.fixed,
                end=count.full
                )

    def write(self, outputpath):
        self.wave.write(outputpath)

    def range_prepronounced(self):
        return slice(self.cursor.start, self.cursor.end_prepronounced)

    def range_overlapping(self):
        return slice(self.cursor.start, self.cursor.end_overlapping)

    def range_fixed(self):
        return slice(self.cursor.start, self.cursor.end_fixed)

    def range_stretchable(self):
        return slice(self.cursor.end_fixed, self.cursor.end)


    def prepronounced(self):
        return self.wave[self.range_prepronounced()]

    def overlapping(self):
        return self.wave[self.range_overlapping()]

    def fixed(self):
        return self.wave[self.range_fixed()]

    def stretchable(self):
        return self.wave[self.range_stretchable()]


def load(path_):
    oto = otoini.load_recursive(path_)
    prefix = prefixmap.load(path.join(path_, 'prefix.map'))
    return Type(
            rootdir=path_,
            oto=oto,
            prefix=prefix)
