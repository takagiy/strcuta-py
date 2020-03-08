# Copyright (C) Yuki Takagi 2020
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE_1_0.txt or copy at
# https://www.boost.org/LICENSE_1_0.txt)

from os import path
from glob import glob
from itertools import chain
from collections import namedtuple

_OtoNode = namedtuple("_OtoNode", "source offset cutoff duration consonant preutterance overlap")

def load_recursive(path_, encoding="cp932", node_type=_OtoNode, greedy_recursion=True):
    if greedy_recursion:
        inis = glob(path.join(path_, "**/oto.ini"), recursive=True)
    else:
        inis = chain(glob(path.join(path_, "oto.ini")), glob(path.join(path_, "*/oto.ini")))

    oto_dict = {}
    for oto_ini in inis:
        oto_dict.update(load(oto_ini, root=path_, encoding=encoding, node_type=node_type))
    return oto_dict

def load(path_, root=None, encoding="cp932", node_type=_OtoNode):
    oto_dict = {}
    with open(path_, "r", encoding=encoding) as f:
        for line in f.readlines():
            line = line.strip()
            [source, params] = line.split("=")
            [name, offset, consonant, cutoff, preutterance, overlap] = params.split(",")

            cf = float(cutoff)
            if cf > 0:
                cf_ = cf
                duration = None
            else:
                cf_ = None
                duration = -cf

            oto_dir = path.dirname(path_) if root == None else path.relpath(path.dirname(path_), root)
            source = path.join(oto_dir, source)

            oto_dict[name]= node_type(
                    source=source,
                    offset=float(offset),
                    cutoff=cf_,
                    duration=duration,
                    consonant=float(consonant),
                    preutterance=float(preutterance),
                    overlap=float(overlap)
                    )
    return oto_dict

if __name__ == "__main__":
    import json

    print(json.dumps(load_recursive(".", node_type=dict), indent=2, ensure_ascii=False))
