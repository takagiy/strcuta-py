# Copyright (C) Yuki Takagi 2020
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE_1_0.txt or copy at
# https://www.boost.org/LICENSE_1_0.txt)

import struct

class Type:
    def __init__(self, format_id, sample_width, key_frequency, comment, nsamples, frq_samples, amp_samples):
        self.format_id = format_id
        self.sample_width = sample_width
        self.key_frequency = key_frequency
        self.comment = comment
        self.nsamples = nsamples
        self.frq_samples = frq_samples
        self.amp_samples = amp_samples

    def write(self, outputpath):
        buffer_ = bytearray(_fmt_hdr.size + _fmt_smp.size * self.nsamples)
        _fmt_hdr.pack_into(
                buffer_,
                0,
                self.format_id,
                self.sample_width,
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


_fmt_hdr = struct.Struct('<8sid16si')
_fmt_smp = struct.Struct('<dd')

def load(path_):
    with open(path_, "rb") as f:
        buffer_ = f.read()

    [format_id, sample_width, key_frequency, comment, nsamples] = _fmt_hdr.unpack_from(buffer_)

    frq_samples = []
    amp_samples = []

    for (frq, amp) in _fmt_smp.iter_unpack(buffer_[_fmt_hdr.size:]):
        frq_samples.append(frq)
        amp_samples.append(amp)

    assert len(frq_samples) == nsamples
    assert len(amp_samples) == nsamples

    return Type(
            format_id=format_id,
            sample_width=sample_width,
            key_frequency=key_frequency,
            comment=comment,
            nsamples=nsamples,
            frq_samples=frq_samples,
            amp_samples=amp_samples
            )

def write(frq_, outputpath):
    frq_.write(outputpath)
