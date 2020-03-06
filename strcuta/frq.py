import struct

class Type:
    def __init__(self, format_id, sample_width, key_frequency, nsamples, frq_samples, amp_samples):
        self.format_id = format_id
        self.sample_width = sample_width
        self.key_frequency = key_frequency
        self.nsamples = nsamples
        self.frq_samples = frq_samples
        self.amp_samples = amp_samples


_fmt_hdr = struct.Struct('<8sid16si')
_fmt_smp = struct.Struct('<dd')

def load(path_):
    with open(path_, "rb") as f:
        buffer_ = f.read()

    [format_id, sample_width, key_frequency, _, nsamples] = _fmt_hdr.unpack_from(buffer_)

    frq_samples = []
    amp_samples = []

    for (frq, amp) in _fmt_smp.iter_unpack(buffer_[_fmt_hdr.size:]):
        frq_samples.append(frq)
        amp_samples.append(amp)

    assert len(frq_samples) == nsamples
    assert len(amp_samples) == nsamples

    return Type(
            format_id = format_id,
            sample_width = sample_width,
            key_frequency = key_frequency,
            nsamples = nsamples,
            frq_samples = frq_samples,
            amp_samples = amp_samples
            )
