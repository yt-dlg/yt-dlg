# System python interpreter. Used only to create virtual environment
PY = python
VENV = venv
BIN = $(VENV)/bin

ifeq ($(OS), Windows_NT)
	BIN = $(VENV)/Scripts
	PY = python
endif


all: format lint test

$(VENV):
		$(PY) -m venv $(VENV)

.PHONY: pip-tools
pip-tools: $(VENV)
		$(PY) -m pip install pip-tools

requirements.txt: requirements.in
		$(PY) -m piptools compile -o requirements.txt --no-header --no-annotate requirements.in

requirements-dev.txt: requirements.txt requirements-dev.in
		$(PY) -m piptools compile -o requirements-dev.txt --no-header --no-annotate requirements-dev.in

# Sync virtual environt with dependencies
.PHONY: build
build: pip-tools requirements.txt
		$(BIN)/pip-sync

.PHONY: dev
dev: pip-tools requirements-dev.txt
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

.PHONY: pyinstaller
pyinstaller: translation
		$(PY) setup.py pyinstaller

.PHONY: clean
clean: clean-build clean-requirements clean-pyc clean-test

clean-build:
		rm -rf build/ dist/ *.eggs-info

clean-requirements:
		rm -f requirements*.txt

clean-pyc:
		find . -type f -name *.pyc -delete
		find . -type f -name *.pyo -delete
		find . -type d -name __pycache__ -delete

clean-test:
		rm -rf .tox/ htmlcov/
		rm -f .coverage
