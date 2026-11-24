# Copyright (C) Yuki Takagi 2020
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE_1_0.txt or copy at
# https://www.boost.org/LICENSE_1_0.txt)

def load(path_, encoding="cp932"):
    """Map each note to its (prefix, suffix). A line is "note<TAB>prefix<TAB>suffix"; either may be empty."""
    prefix_map = {}
    with open(path_, encoding=encoding) as f:
        for line in f:
            note, *affixes = line.rstrip("\r\n").split("\t")
            if note:
                prefix, suffix = (affixes + ["", ""])[:2]
                prefix_map[note] = (prefix, suffix)
    return prefix_map
