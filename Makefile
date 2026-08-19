SHELL = bash
UV ?= uv
RM = rm -f
RMR := $(RM)r


all: format lint test-cov

.PHONY: lock
lock:
	$(UV) lock

.PHONY: sync
sync:
	$(UV) sync --frozen --no-dev

.PHONY: build
build:
	$(UV) sync --frozen --no-dev --extra binaries

.PHONY: dev
dev:
	$(UV) sync --frozen --extra binaries

.PHONY: lint
lint: dev
	$(UV) run flake8

.PHONY: format-check
format-check: dev
	$(UV) run black --check .

.PHONY: format
format: dev
	$(UV) run black .

.PHONY: translation
translation:
	$(UV) sync --frozen --no-dev --group build
	$(UV) run --no-dev --group build python -m devscripts.build_translations

.PHONY: test
test: translation dev
	$(UV) run python -m unittest discover -s tests -v

.PHONY: test-cov
test-cov: translation dev
	$(UV) run pytest --cov-report term-missing --cov=youtube_dl_gui tests/ -vv

.PHONY: install
install: translation

.PHONY: pyinstaller
pyinstaller: translation
	$(UV) run --no-dev --extra binaries python -m devscripts.build_executable

.PHONY: typecheck
typecheck: dev
	$(UV) run mypy -p youtube_dl_gui

.PHONY: clean
clean: clean-build clean-test

.PHONY: clean-venv
clean-venv:
	$(RMR) .venv

.PHONY: clean-build
clean-build:
	$(RMR) build dist *.egg-info

.PHONY: clean-pyc
clean-pyc:
	find . -type f -name "*.pyc" -exec rm -f {} \;
	find . -type f -name "*.pyo" -exec rm -f {} \;
	-find . -type d -name "__pycache__" -exec rm -rf {} \;

.PHONY: clean-test
clean-test:
	$(RMR) .tox/ htmlcov/
	$(RM) .coverage
