# Copyright (C) Yuki Takagi 2020
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE_1_0.txt or copy at
# https://www.boost.org/LICENSE_1_0.txt)

class Cursor:
    def _resolve(self, samplerate, samplewidth):
        pass

    def __neg__(self):
        pass

class MilliSeconds(Cursor):
    def __init__(self, value):
        self.value = value

    def __neg__(self):
        return MilliSeconds(-self.value)

    def _resolve(self, samplerate, samplewidth):
        return round(samplerate * self.value / 1000 * samplewidth)

class Samples(Cursor):
    def __init__(self, value):
        self.value = value

    def __neg__(self):
        return Samples(-self.value)

    def _resolve(self, samplerate, samplewidth):
        return round(samplewidth * self.value)

def ms(milliseconds):
    return MilliSeconds(milliseconds)

def smp(frames):
    return Samples(frames)

def resolve(cursor, samplerate, samplewidth):
    if isinstance(cursor, Cursor):
        return cursor._resolve(samplerate, samplewidth)
    elif isinstance(cursor, int):
        return round(cursor * samplewidth)
    elif cursor == None:
        return None
    else:
        raise "Unsupported Cursor type " + cursor.__class__.__name__

def resolve_slice(slice_, samplerate, samplewidth):
    return slice(
            resolve(slice_.start, samplerate, samplewidth),
            resolve(slice_.stop, samplerate, samplewidth),
            resolve(slice_.step, samplerate, samplewidth))

def resolve_to_slice(cursor, samplerate, samplewidth):
    return slice(
            resolve(cursor, samplerate, samplewidth),
            resolve(cursor, samplerate, samplewidth) + round(samplewidth))
