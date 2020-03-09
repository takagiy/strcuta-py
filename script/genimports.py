import re
from pathlib import Path

_pat = re.compile(r"^(from [^\s]+ |)import [^\s]+")

def generate(path_):
    pathobj = Path(path_)
    with (pathobj / "__init__.py").open("r+") as f:
        lines = f.readlines()
        f.seek(0, 0)

        leadings = "".join(filter(lambda l: not _pat.match(l), lines))
        f.write(leadings)

        module = path_.replace("/", ".")
        for subpy in filter(lambda p: p.suffix == ".py" and not p.stem.startswith("__"), pathobj.glob("*")):
            f.write("from " + module + " import " + subpy.stem + "\n")
            f.truncate()

generate("strcuta")
