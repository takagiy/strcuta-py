# Copyright (C) Yuki Takagi 2020
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE_1_0.txt or copy at
# https://www.boost.org/LICENSE_1_0.txt)

from setuptools import setup
from setuptools import find_packages

setup(
        name="strcuta",
        version="0.0.2",
        url="https://github.com/takagiy/strcutau",
        description="Load UTAU voice banks into the Python data structure.",
        author="takagiy",
        author_email="takagiy.4dev@gmail.com",
        license="BSL-1.0",
        packages=find_packages(),
        include_package_data=False,
        install_requires=[])
