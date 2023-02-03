SHELL = bash
# System python interpreter. Used only to create virtual environment
PY = python3
VENVDIR = ./venv
BIN := $(VENVDIR)/bin
RM = rm -f
RMR := $(RM)r
ACTIVATE=source $(BIN)/activate


all: format lint test-cov

venv:
	@if [ -d $(VENVDIR) ] ; then \
		echo "venv already exists."; \
		echo "To recreate it, remove it first with \`make clean-venv'."; \
	else \
		$(MAKE) ensure-venv; \
	fi
		
.PHONY: ensure-venv
ensure-venv:
	@if [ ! -d $(VENVDIR) ] ; then \
		$(PY) -m venv $(VENVDIR); \
		$(BIN)/$(PY) -m pip install --upgrade pip setuptools wheel; \
		echo "The venv has been created in the $(VENVDIR) directory"; \
	fi

.piptools: venv
	$(BIN)/$(PY) -m pip install pip-tools
	touch .piptools

requirements/requirements.txt: .piptools requirements/requirements.in
	$(PY) -m piptools compile -o requirements/requirements.txt --no-header --no-annotate requirements/requirements.in

requirements/requirements-binaries.txt: .piptools requirements/requirements-binaries.in
	$(PY) -m piptools compile -o requirements/requirements-binaries.txt --no-header --no-annotate requirements/requirements-binaries.in

requirements/requirements-dev.txt: .piptools requirements/requirements-dev.in
	$(PY) -m piptools compile -o requirements/requirements-dev.txt --no-header --no-annotate requirements/requirements-dev.in

# Sync virtual environment with dependencies
.PHONY: build
build: requirements/requirements.txt requirements/requirements-binaries.txt
	$(PY) -m piptools sync requirements/requirements.txt requirements/requirements-binaries.txt

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
typecheck: dev
	$(PY) -m mypy -p youtube_dl_gui

.PHONY: clean
clean: clean-build clean-requirements clean-test

.PHONY: clean-venv
clean-venv:
	$(RMR) $(VENVDIR)

clean-build:
	$(RMR) build dist *.egg-info

clean-requirements:
	$(RM) .piptools
	$(RM) requirements/requirements.txt
	$(RM) requirements/requirements-dev.txt

clean-pyc:
		find . -type f -name "*.pyc" -exec rm -f {} \;
		find . -type f -name "*.pyo" -exec rm -f {} \;
		-find . -type d -name "__pycache__" -exec rm -rf {} \;

clean-test:
		$(RMR) .tox/ htmlcov/
		$(RM) .coverage
