# Copyright (C) Yuki Takagi 2020
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE_1_0.txt or copy at
# https://www.boost.org/LICENSE_1_0.txt)

import wave as _wave
import struct as _struct
from strcuta import cursor as _cursor

class Type:
    def __init__(self, format_id, sample_interval, samplerate, key_frequency, comment, nsamples, frq_samples, amp_samples):
        self.format_id = format_id
        self.sample_interval = sample_interval
        self.samplerate = samplerate
        self.key_frequency = key_frequency
        self.comment = comment
        self.nsamples = nsamples
        self.frq_samples = frq_samples
        self.amp_samples = amp_samples

    def __getitem__(self, key):
        if isinstance(key, slice):
            k = _cursor.resolve_slice(key, self.samplerate, 1)
            return Type(
                    self.format_id,
                    self.sample_interval,
                    self.samplerate,
                    self.key_frequency,
                    self.comment,
                    int((k.stop - k.start) / (k.step or 1)),
                    self.frq_samples[k],
                    self.amp_samples[k])
        else:
            k = _cursor.resolve(key, self.samplerate, 1)
            return (self.frq_samples[k], self.amp_samples[k])

    def write(self, outputpath):
        buffer_ = bytearray(_fmt_hdr.size + _fmt_smp.size * self.nsamples)
        _fmt_hdr.pack_into(
                buffer_,
                0,
                self.format_id,
                self.sample_interval,
                self.key_frequency,
                self.comment,
                self.nsamples)
        for i in range(0, self.nsamples):
            _fmt_smp.pack_into(
                    buffer_,
                    _fmt_hdr.size + i * _fmt_smp.size,
                    self.frq_samples[i],
                    self.amp_samples[i])
        with open(outputpath, "wb") as f:
            f.write(buffer_)


_fmt_hdr = _struct.Struct('<8sid16si')
_fmt_smp = _struct.Struct('<dd')

def _wave_path(frq_path):
    return frq_path[:-8] + ".wav"

def load(path_, wave=None):
    with open(path_, "rb") as f:
        buffer_ = f.read()

    [format_id, sample_interval, key_frequency, comment, nsamples] = _fmt_hdr.unpack_from(buffer_)

    if wave:
        sample_interval = wave.getnchannels() * wave.getframerate() / sample_interval
    else:
        with _wave.open(_wave_path(path_), "rb") as w:
            samplerate = w.getnchannels() * w.getframerate() / sample_interval

    frq_samples = []
    amp_samples = []

    for (frq, amp) in _fmt_smp.iter_unpack(buffer_[_fmt_hdr.size:]):
        frq_samples.append(frq)
        amp_samples.append(amp)

    assert len(frq_samples) == nsamples
    assert len(amp_samples) == nsamples

    return Type(
            format_id=format_id,
            sample_interval=sample_interval,
            samplerate=samplerate,
            key_frequency=key_frequency,
            comment=comment,
            nsamples=nsamples,
            frq_samples=frq_samples,
            amp_samples=amp_samples
            )

def write(frq, outputpath):
    frq.write(outputpath)
