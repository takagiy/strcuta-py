# Copyright (C) Yuki Takagi 2020
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE_1_0.txt or copy at
# https://www.boost.org/LICENSE_1_0.txt)

def load(path_, encoding="cp932"):
    prefix_map = {}
    with open(path_, encoding=encoding) as f:
        for line in f.readlines():
            prefix_map.update((line.strip().split(),))
    return prefix_map
