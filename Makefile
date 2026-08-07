.PHONY: test lint format-check validate

test:
	python -m pytest

lint:
	python -m ruff check .

format-check:
	python -m ruff format --check .

validate:
	python scripts/validate_catalog.py
