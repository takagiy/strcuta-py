# Copyright (C) Yuki Takagi 2020
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE_1_0.txt or copy at
# https://www.boost.org/LICENSE_1_0.txt)

from os import path as _path

from strcuta import otoini as _otoini
from strcuta import prefixmap as _prefixmap
from strcuta import frq as _frq
from strcuta import wav as _wav

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

def _ms2nframes(rate, millisec):
    return round(rate * millisec / 1000)

class Type:
    def __init__(self, rootdir, otos, prefixes):
        self.rootdir = rootdir
        self.otos = otos
        self.prefixes = prefixes

    def resolve(self, spell, key):
        return spell + self.prefixes[key]

    def oto(self, spell, key):
        return self.otos[self.resolve(spell, key)]

    def voice(self, spell, key):
        info = self.oto(spell, key)
        w = _wav.load(_path.join(self.rootdir, info.source))

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
        
        return Voice(
                wave=w[nf_offset : nf_offset + nf_used],
                count=Counts(
                    pre=nf_pre,
                    ovl=nf_ovl,
                    con=nf_con,
                    full=nf_used,
                    )
                )

class Voice(_wav.Type):
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


def load(path, encoding='cp932', greedy_oto_load=False):
    otos = _otoini.load_recursive(path, encoding=encoding, greedy_recursion=greedy_oto_load)
    prefixes = _prefixmap.load(_path.join(path, 'prefix.map'), encoding=encoding)
    return Type(
            rootdir=path,
            otos=otos,
            prefixes=prefixes)
