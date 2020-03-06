SRC := $(shell find strcuta -type f -name "*.py")
TARDIST := dist/strcuta-0.0.1.tar.gz
WHEEL := dist/strcuta-0.0.1-py3-none-any.whl
DIST := $(TARDIST) $(WHEEL)

.PHONY: all clean bdist publish.test publish.pypi

all: bdist

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
