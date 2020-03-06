# Copyright (C) Yuki Takagi 2020
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE_1_0.txt or copy at
# https://www.boost.org/LICENSE_1_0.txt)

PKGVER := $(shell cat setup.py | grep "version" | sed -e 's/^ *version="//;s/",//')
SRC := $(shell find strcuta -type f -name "*.py")
TARDIST := dist/strcuta-$(PKGVER).tar.gz
WHEEL := dist/strcuta-$(PKGVER)-py3-none-any.whl
DIST := $(TARDIST) $(WHEEL)

.PHONY: all clean bdist publish.test publish.pypi licensenote

all: licensenote bdist

clean:
	rm -rf dist
	rm -rf build
	rm -rf strcuta.egg-info

bdist: $(DIST)

$(DIST): $(SRC) setup.py
	python setup.py sdist bdist_wheel

publish.test: $(DIST)
	twine upload --repository testpypi dist/*

publish.pypi: $(DIST)
	twine upload --repository pypi dist/*

licensenote:
	python script/notelicense.py
