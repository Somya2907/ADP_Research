## help: list all targets with one-line descriptions
## setup: install Poetry deps, create empty output dirs
## check: run scripts/check_setup.py
## test: run pytest on tests/
## extract: run full extraction (teacher + both students, all 6 cases)
## extract-teacher: teacher only
## extract-gpt5: GPT-5 only
## extract-small: small model only
## breakdown: run the node-type breakdown diagnostic
## clean: remove .cache/ and data/outputs/graphs/*.json
## clean-all: remove .cache/, all generated files, and __pycache__
## lint: run ruff on src/ and scripts/
## format: run black on src/ and scripts/

.PHONY: help setup check test extract extract-teacher extract-gpt5 extract-small \
        breakdown clean clean-all lint format

PYTHON := poetry run python
PYTEST := poetry run pytest

help:  ## list all targets with one-line descriptions
	@echo "L-DRL — make targets"
	@echo ""
	@awk 'BEGIN { FS = ":" } /^## / { sub(/^## /, "", $$0); split($$0, a, ":"); printf "  \033[36mmake %-18s\033[0m %s\n", a[1], a[2] }' $(MAKEFILE_LIST)

setup:  ## install Poetry deps and create empty output dirs
	@echo ">>> setup: installing Poetry dependencies"
	poetry install
	@echo ">>> setup: creating output directories"
	@mkdir -p data/outputs/graphs data/outputs/analysis data/outputs/discrepancies results .cache
	@echo "<<< setup: done"

check:  ## run scripts/check_setup.py
	@echo ">>> check: running environment verification"
	$(PYTHON) scripts/check_setup.py
	@echo "<<< check: done"

test:  ## run pytest on tests/
	@echo ">>> test: running pytest"
	$(PYTEST)
	@echo "<<< test: done"

extract:  ## run full extraction (teacher + both students, all 6 cases)
	@echo ">>> extract: teacher + gpt5 + qwen3_4b on all 6 cases"
	$(PYTHON) scripts/run_extraction.py
	@echo "<<< extract: done"

extract-teacher:  ## teacher only
	@echo ">>> extract-teacher"
	$(PYTHON) scripts/run_extraction.py --teacher
	@echo "<<< extract-teacher: done"

extract-gpt5:  ## GPT-5 only
	@echo ">>> extract-gpt5"
	$(PYTHON) scripts/run_extraction.py --gpt5
	@echo "<<< extract-gpt5: done"

extract-small:  ## small model only (qwen3_4b)
	@echo ">>> extract-small"
	$(PYTHON) scripts/run_extraction.py --qwen
	@echo "<<< extract-small: done"

breakdown:  ## run the node-type breakdown diagnostic
	@echo ">>> breakdown: computing F/I/R/A/C/O totals per graph"
	$(PYTHON) scripts/breakdown.py
	@echo "<<< breakdown: done"

clean:  ## remove .cache/ and data/outputs/graphs/*.json
	@echo ">>> clean: removing cache and extracted graphs"
	rm -rf .cache
	rm -f data/outputs/graphs/*.json
	@echo "<<< clean: done"

clean-all:  ## remove .cache, all generated files, and __pycache__
	@echo ">>> clean-all: removing cache, outputs, and __pycache__"
	rm -rf .cache
	rm -rf data/outputs/graphs/*.json
	rm -rf data/outputs/analysis/*
	rm -rf data/outputs/discrepancies/*
	rm -rf results/*
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name .pytest_cache -prune -exec rm -rf {} +
	@echo "<<< clean-all: done"

lint:  ## run ruff on src/ and scripts/
	@echo ">>> lint: running ruff"
	poetry run ruff check src scripts tests
	@echo "<<< lint: done"

format:  ## run black on src/ and scripts/
	@echo ">>> format: running black"
	poetry run black src scripts tests
	@echo "<<< format: done"
