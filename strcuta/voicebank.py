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

_WaveParams = namedtuple("_wave_params", "nchannels sampwidth framerate nframes comptype compname")

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

            rate = w.getframerate()
            sampwidth = w.getsampwidth()
            nchannels = w.getnchannels()
            assert nchannels == 1

            nframes = w.getnframes()
            nf_left_margin = _ms2nframes(rate, info["leftMargin"])
            nf_fixed = _ms2nframes(rate, info["fixed"])
            nf_prepronounced = _ms2nframes(rate, info["prepronounced"])
            nf_overlapping = _ms2nframes(rate, info["overlapping"])
            if info["duration"] != None:
                nf_used = _ms2nframes(rate, info["duration"])
            else:
                nf_right_margin = _ms2nframes(rate, info["rightMargin"])
                nf_used = nframes - nf_left_margin - nf_right_margin
            
            w.readframes(nf_left_margin)
            frames = w.readframes(nf_used)

        return Voice(
                wave_parameters=_WaveParams(
                    sampwidth=sampwidth,
                    nframes=nf_used,
                    nchannels=nchannels,
                    framerate=rate,
                    comptype="NONE",
                    compname="not compressed"
                    ),
                count=Counts(
                    prepronounced=nf_prepronounced,
                    overlapping=nf_overlapping,
                    fixed=nf_fixed,
                    full=nf_used,
                    ),
                frames=frames,
                )

class Voice:
    def __init__(self, frames, wave_parameters, count):
        self.wave_parameters=wave_parameters
        self.frames = frames
        self.count = count
        self.cursor = Cursors(
                start=0,
                end_overlapping=count.overlapping,
                end_prepronounced=count.prepronounced,
                end_fixed=count.fixed,
                end=count.full
                )

    def write(self, outputpath):
        with wave.open(outputpath, "wb") as w:
            w.setparams(self.wave_parameters)
            w.writeframes(self.frames)

    def range_prepronounced(self):
        return slice(self.cursor.start, self.cursor.end_prepronounced)

    def range_overlapping(self):
        return slice(self.cursor.start, self.cursor.end_overlapping)

    def range_fixed(self):
        return slice(self.cursor.start, self.cursor.end_fixed)

    def range_stretchable(self):
        return slice(self.cursor.end_fixed, self.cursor.end)


def load(path_):
    oto = otoini.load_recursive(path_)
    prefix = prefixmap.load(path.join(path_, 'prefix.map'))
    return Type(
            rootdir=path_,
            oto=oto,
            prefix=prefix)
