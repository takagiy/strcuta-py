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
    def __init__(self, start, end_overlap, end_preutterance, end_consonant, end):
        self.start = start
        self.end_overlap = end_overlap
        self.end_preutterance = end_preutterance
        self.end_consonant = end_consonant
        self.end_fixed = end_consonant
        self.end = end

class Counts:
    def __init__(self, preutterance, overlap, consonant, full):
        self.preutterance = preutterance
        self.overlap = overlap
        self.consonant = consonant
        self.fixed = consonant
        self.full = full
        self.stretchable = full - consonant

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
        with wave.open(path.join(self.rootdir, info.source), mode="rb") as w:
            w = Wave.make(w)

            rate = w.parameter.framerate
            nframes = w.parameter.nframes

            nf_offset = _ms2nframes(rate, info.offset)
            nf_consonant = _ms2nframes(rate, info.consonant)
            nf_preutterance = _ms2nframes(rate, info.preutterance)
            nf_overlap = _ms2nframes(rate, info.overlap)
            if info.duration != None:
                nf_used = _ms2nframes(rate, info.duration)
            else:
                nf_cutoff = _ms2nframes(rate, info.cutoff)
                nf_used = nframes - nf_offset - nf_cutoff
            
            w = w[nf_offset : nf_offset + nf_used]

        return Voice(
                wave=w,
                count=Counts(
                    preutterance=nf_preutterance,
                    overlap=nf_overlap,
                    consonant=nf_consonant,
                    full=nf_used,
                    )
                )

class Voice(Wave):
    def __init__(self, wave, count):
        self.count = count
        self.cursor = Cursors(
                start=0,
                end_overlap=count.overlap,
                end_preutterance=count.preutterance,
                end_consonant=count.consonant,
                end=count.full
                )
        super().__init__(
                parameter=wave.parameter,
                frames=wave.frames)

    def range_preutterance(self):
        return slice(self.cursor.start, self.cursor.end_preutterance)

    def range_overlap(self):
        return slice(self.cursor.start, self.cursor.end_overlap)

    def range_consonant(self):
        return slice(self.cursor.start, self.cursor.end_consonant)

    def range_fixed(self):
        return self.range_fixed()

    def range_stretchable(self):
        return slice(self.cursor.end_consonant, self.cursor.end)


    def preutterance(self):
        return self[self.range_preutterance()]

    def overlap(self):
        return self[self.range_overlap()]

    def consonant(self):
        return self[self.range_consonant()]

    def fixed(self):
        return self.consonant()

    def stretchable(self):
        return self[self.range_stretchable()]


def load(path_):
    oto = otoini.load_recursive(path_)
    prefix = prefixmap.load(path.join(path_, 'prefix.map'))
    return Type(
            rootdir=path_,
            oto=oto,
            prefix=prefix)
