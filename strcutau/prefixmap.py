def load(path_, encoding="cp932"):
    prefix_map = {}
    with open(path_, encoding=encoding) as f:
        for line in f.readlines():
            prefix_map.update((line.strip().split(),))
    return prefix_map
