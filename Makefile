.PHONY: lint test

lint:
	.venv/bin/ruff check rescue_debootstrap/ tests/ --fix

test:
	.venv/bin/pytest
