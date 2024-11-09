.PHONY: checks, docs-serve, docs-build, fmt, config, type, tests

# Run pre-commit checks
# ------------------------------------------------------------------------------
checks:
	uvx pre-commit run --all-files

docs-serve:
	uv run mkdocs serve

docs-build:
	uv run mkdocs build

fmt:
	uv run ruff format src tests

lint:
	uv run ruff check --fix src tests

type:
	uv run mypy src --install-types --non-interactive --show-traceback

tests:
	uv run pytest --cov=aiventure --cov-report=term-missing tests/ -s -vv
