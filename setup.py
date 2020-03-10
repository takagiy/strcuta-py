# Copyright (C) Yuki Takagi 2020
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE_1_0.txt or copy at
# https://www.boost.org/LICENSE_1_0.txt)

from setuptools import setup
from setuptools import find_packages

from os import path
pkgdir = path.abspath(path.dirname(__file__))
with open(path.join(pkgdir, "README.md"), encoding="utf-8") as f:
    readme_md = f.read()

setup(
        name="strcuta",
        version="0.0.15",
        url="https://github.com/takagiy/strcuta-py",
        project_urls={
            "Repository": "https://github.com/takagiy/strcuta-py",
            "Bug reports": "https://github.com/takagiy/strcuta-py/issues"
            },
        description="Loading UTAU voice banks into the Python data structure.",
        long_description=readme_md,
        long_description_content_type="text/markdown",
        author="takagiy",
        author_email="takagiy.4dev@gmail.com",
        classifiers=[
            "License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)",
            "Development Status :: 3 - Alpha"
            ],
        packages=find_packages(),
        include_package_data=False,
        install_requires=[],
        extras_require={
            "play": ["sounddevice"]
            })
