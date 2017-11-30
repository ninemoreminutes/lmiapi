.PHONY: core-requirements update-pip-requirements requirements clean-pyc \
	develop reports pycodestyle flake8 check8 test

core-requirements:
	pip install "pip>=9,<9.1" setuptools "pip-tools>=1"

update-pip-requirements: core-requirements
	pip install -U "pip>=9,<9.1" setuptools "pip-tools>=1"
	pip-compile -U requirements/base.in
	pip-compile -U requirements/dev.in

requirements: core-requirements
	pip-sync requirements/base.txt requirements/dev.txt

clean-pyc: requirements
	find . -iname "*.pyc" -delete

develop: clean-pyc
	python setup.py develop

reports:
	mkdir -p $@

pycodestyle: reports requirements
	set -o pipefail && $@ lmiapi examples tests | tee reports/$@.report

flake8: reports requirements
	set -o pipefail && $@ lmiapi examples tests | tee reports/$@.report

check8: pycodestyle flake8

test: check8
	py.test -v
