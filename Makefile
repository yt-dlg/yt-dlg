# System python interpreter. Used only to create virtual environment
PY=python3
VENV=venv
BIN=$(VENV)/bin
ACTIVATE=source $(BIN)/activate

ifeq ($(OS), Windows_NT)
	BIN=$(VENV)/Scripts
	PY=python
	ACTIVATE=$(BIN)/activate
endif


all: format lint test

$(VENV):
		$(PY) -m venv $(VENV)
		echo "Activate the Virtual Environment for next targets!"

.PHONY: pip-tools
pip-tools: $(VENV)
		$(PY) -m pip install --upgrade pip setuptools wheel
		$(PY) -m pip install pip-tools

requirements.txt: pip-tools requirements.in
		$(PY) -m piptools compile -o requirements.txt --no-header --no-annotate requirements.in

requirements-dev.txt: pip-tools requirements-dev.in
		$(PY) -m piptools compile -o requirements-dev.txt --no-header --no-annotate requirements-dev.in

# Sync virtual environment with dependencies
.PHONY: build
build: requirements.txt
		$(BIN)/pip-sync

.PHONY: dev
dev: requirements.txt requirements-dev.txt
		$(BIN)/pip-sync requirements.txt requirements-dev.txt

.PHONY: lint
lint: dev
		$(BIN)/flake8

format-check: dev
		$(BIN)/black --check .

.PHONY: format
format: dev
		$(BIN)/black .

.PHONY: translation
translation: build
		$(PY) setup.py build_trans

.PHONY: test
test: translation
		$(PY) -m unittest discover -s tests -v

.PHONY: install
install: translation
		$(PY) setup.py install

.PHONY: pyinstaller
pyinstaller: translation
		$(PY) setup.py pyinstaller

.PHONY: typecheck
typecheck:
		mypy -p youtube_dl_gui

.PHONY: clean
clean: clean-build clean-requirements clean-pyc clean-test

clean-build:
		rm -rf build dist *.egg-info

clean-requirements:
		rm -f requirements*.txt

clean-pyc:
		find . -type f -name "*.pyc" -exec rm -f {} \;
		find . -type f -name "*.pyo" -exec rm -f {} \;
		find . -type d -name "__pycache__" -exec rm -rf {} \;

clean-test:
		rm -rf .tox/ htmlcov/
		rm -f .coverage
