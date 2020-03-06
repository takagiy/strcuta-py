import wave
from os import path
from collections import namedtuple

from strcuta import otoini
from strcuta import prefixmap
from strcuta import frq

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
            if info["duration"] != None:
                nf_used = _ms2nframes(rate, info["duration"])
            else:
                nf_right_margin = _ms2nframes(rate, info["rightMargin"])
                nf_used = nframes - nf_left_margin - nf_right_margin
            
            w.readframes(nf_left_margin)
            frames = w.readframes(nf_used)

        return Voice(
                sampwidth=sampwidth,
                frames=frames,
                nframes=nf_used,
                nchannels=nchannels,
                framerate=rate,
                nprepronounced=nf_prepronounced,
                nfixed=nf_fixed,
                comptype="NONE",
                compname="not compressed"
                )
# class _WaveParams:
#     def __init__(self, nchannels, sampwidth, framerate, nframes, comptype):
#         self.nchannels = nchannels
#         self.sampwidth = sampwidth
#         self.framerate = framerate
#         self.nframes = nframes
#         self.comptype = comptype

_WaveParams = namedtuple("_wave_params", "nchannels sampwidth framerate nframes comptype compname")

class Voice:
    def __init__(self, frames, sampwidth, nframes, nchannels, framerate, nprepronounced, nfixed, comptype, compname):
        self.frames = frames
        self.sampwidth = sampwidth
        self.nframes  = nframes
        self.nchannels = nchannels
        self.framerate = framerate
        self.comptype = comptype
        self.compname = compname
        self.nprepronounced = nprepronounced
        self.nfixed = nfixed

    def getparams(self):
        return _WaveParams(
                nchannels=self.nchannels,
                sampwidth=self.sampwidth,
                framerate=self.framerate,
                nframes=self.nframes,
                comptype=self.comptype,
                compname=self.compname)

    def write(self, outputpath):
        with wave.open(outputpath, "wb") as w:
            w.setparams(self.getparams())
            #w.setnchannels(self.nchannels)
            #w.setsampwidth(self.sampwidth)
            #w.setframerate(self.framerate)
            #w.setnframes(self.nframes)
            w.writeframes(self.frames)


def load(path_):
    oto = otoini.load_recursive(path_)
    prefix = prefixmap.load(path.join(path_, 'prefix.map'))
    return Type(
            rootdir=path_,
            oto=oto,
            prefix=prefix)
