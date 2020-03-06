import glob
import os.path as path

def load_recursive(path_, encoding="cp932"):
    oto_json = {}
    for oto_ini in glob.glob(path.join(path_, "**/oto.ini"), recursive=True):
        oto_json.update(load(oto_ini, root=path_, encoding=encoding))
    return oto_json

def load(path_, root=None, encoding="cp932"):
    oto_json = {}
    with open(path_, "r", encoding=encoding) as f:
        for line in f.readlines():
            line = line.strip()
            [source, params] = line.split("=")
            [name, left_margin, fixed, right_margin, prepronounced, overlapping] = params.split(",")
            oto_dir = path.dirname(path_) if root == None else path.relpath(path.dirname(path_), root)
            source = path.join(oto_dir, source)
            oto_json[name] = {
                    "source": source,
                    "leftMargin": left_margin,
                    "rightMargin": right_margin,
                    "fixed": fixed,
                    "prepronounced": prepronounced,
                    "overlapping": overlapping
                    }
    return oto_json

if __name__ == "__main__":
    import json

    print(json.dumps(load_recursive("."), indent=2, ensure_ascii=False))
