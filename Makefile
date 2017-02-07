SHELL := /bin/sh
PYTHON :=python # must be python 3.x
PY_FILES = $(shell git ls-files | grep '.py$$')

clean:
	@ test -d .virt && rm -Rf .virt

bootstrap: clean
	@ virtualenv --python=$(PYTHON) .virt && \
    source .virt/bin/activate && \
	pip install uwsgi && \
	pip install flake8

test: bootstrap
	source .virt/bin/activate && sh tests/test.sh

style: test
	@ source .virt/bin/activate && flake8 $(PY_FILES)
	