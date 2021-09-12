# System python interpreter. Used only to create virtual environment
PY=python3
VENV=venv
BIN=$(VENV)/bin
TOUCH=touch
ACTIVATE=source $(BIN)/activate

ifeq ($(OS), Windows_NT)
	PY=python
	BIN=$(VENV)/Scripts
	TOUCH=echo "" >
	RM=del /S
	ACTIVATE=$(BIN)/activate
endif


all: format lint test

$(VENV):
		$(PY) -m venv $(VENV)
		@echo Activate the Virtual Environment for next targets!
		@echo     $(ACTIVATE)

.piptools: $(VENV)
		$(PY) -m pip install --upgrade pip setuptools wheel
		$(PY) -m pip install pip-tools
		$(TOUCH) .piptools

requirements/requirements.txt: .piptools requirements/requirements.in
		$(PY) -m piptools compile -o requirements/requirements.txt --no-header --no-annotate requirements/requirements.in

requirements/requirements-dev.txt: .piptools requirements/requirements-dev.in
		$(PY) -m piptools compile -o requirements/requirements-dev.txt --no-header --no-annotate requirements/requirements-dev.in

# Sync virtual environment with dependencies
.PHONY: build
build: requirements/requirements.txt
		$(PY) -m piptools sync requirements/requirements.txt

.PHONY: dev
dev: requirements/requirements.txt requirements/requirements-dev.txt
		$(PY) -m piptools sync requirements/requirements.txt requirements/requirements-dev.txt

.PHONY: lint
lint: dev
		$(PY) -m flake8

format-check: dev
		$(PY) -m black --check .

.PHONY: format
format: dev
		$(PY) -m black .

.PHONY: translation
translation: build
		$(PY) setup.py build_trans

.PHONY: test
test: translation
		$(PY) -m unittest discover -s tests -v

.PHONY: test-cov
test-cov: dev
		$(PY) -m pytest --cov-report term-missing --cov=youtube_dl_gui tests/ -vv

.PHONY: install
install: translation
		$(PY) setup.py install

.PHONY: pyinstaller
pyinstaller: translation
		$(PY) setup.py pyinstaller

.PHONY: typecheck
typecheck:
		$(PY) -m mypy -p youtube_dl_gui

.PHONY: clean
clean: clean-build clean-requirements clean-pyc clean-test

clean-build:
		rm -rf build dist *.egg-info

clean-requirements:
		${RM} .piptools
		${RM} "requirements*.txt"

clean-pyc:
		find . -type f -name "*.pyc" -exec rm -f {} \;
		find . -type f -name "*.pyo" -exec rm -f {} \;
		find . -type d -name "__pycache__" -exec rm -rf {} \;

clean-test:
		rm -rf .tox/ htmlcov/
		rm -f .coverage
