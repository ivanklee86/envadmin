SHELL := /bin/bash
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = envadmin

#-----------------------------------------------------------------------
# Rules of Rules : Grouped rules that _doathing_
#-----------------------------------------------------------------------

test: lint pytest

install: clean install-package

build: clean generate-requirements build-package upload

build-local: clean generate-requirements build-package

#-----------------------------------------------------------------------
# Testing & Linting
#-----------------------------------------------------------------------

lint:
	pylint ${PROJECT_NAME} && \
	mypy ${PROJECT_NAME};

pytest:
	export PYTHONPATH=${ROOT_DIR}: $$PYTHONPATH && \
	py.test -n 4 --cov ${PROJECT_NAME} tests

#-----------------------------------------------------------------------
# Distribution
#-----------------------------------------------------------------------
clean:
	rm -rf build && \
	rm -rf dist && \
	rm -rf ${PROJECT_NAME}.egg-info;

generate-requirements:
	pipenv lock -r > requirements.txt && \
	pipenv lock -r --dev > requirements-dev.txt;

install-package:
	python setup.py install

build-package:
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*
