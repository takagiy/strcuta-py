# Copyright (C) Yuki Takagi 2020
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE_1_0.txt or copy at
# https://www.boost.org/LICENSE_1_0.txt)

import glob
from os import path
from collections import namedtuple

_OtoNode = namedtuple("_OtoNode", "source leftMargin rightMargin duration fixed prepronounced overlapping")

def load_recursive(path_, encoding="cp932", node_type=_OtoNode):
    oto_dict = {}
    for oto_ini in glob.glob(path.join(path_, "**/oto.ini"), recursive=True):
        oto_dict.update(load(oto_ini, root=path_, encoding=encoding, node_type=node_type))
    return oto_dict

def load(path_, root=None, encoding="cp932", node_type=_OtoNode):
    oto_dict = {}
    with open(path_, "r", encoding=encoding) as f:
        for line in f.readlines():
            line = line.strip()
            [source, params] = line.split("=")
            [name, left_margin, fixed, right_margin, prepronounced, overlapping] = params.split(",")

            rm = float(right_margin)
            if rm > 0:
                rm_ = rm
                duration = None
            else:
                rm_ = None
                duration = - rm

            oto_dir = path.dirname(path_) if root == None else path.relpath(path.dirname(path_), root)
            source = path.join(oto_dir, source)

            oto_dict[name]= node_type(
                    source=source,
                    leftMargin=float(left_margin),
                    rightMargin=rm_,
                    duration=duration,
                    fixed=float(fixed),
                    prepronounced=float(prepronounced),
                    overlapping=float(overlapping)
                    )
    return oto_dict

if __name__ == "__main__":
    import json

    print(json.dumps(load_recursive(".", node_type=dict), indent=2, ensure_ascii=False))
