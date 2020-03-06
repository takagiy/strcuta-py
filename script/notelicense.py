# Copyright (C) Yuki Takagi 2020
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE_1_0.txt or copy at
# https://www.boost.org/LICENSE_1_0.txt)

"""Copyright (C) Yuki Takagi 2020
Distributed under the Boost Software License, Version 1.0.
(See accompanying file LICENSE_1_0.txt or copy at
https://www.boost.org/LICENSE_1_0.txt)"""

import glob
import re

def note(glob_, comment_start, comment_end=""):
    for source in glob.glob(glob_, recursive=True):
        with open(source, "r+") as f:
            content = f.read()
            notice = re.sub(r"^", comment_start, re.sub(r"$", comment_end, __doc__, flags=re.M), flags=re.M)
            if not content.startswith(notice):
                f.seek(0, 0)
                f.write(notice)
                f.write("\n\n")
                f.write(content)

note("**/*.py", "# ")
note("**/*.md", "<!-- ", " -->")
note("Makefile", "# ")
