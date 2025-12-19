.PHONY: install

install:
	cd backend && uv venv --python 3.12
	cd backend && uv pip install -e .

.PHONY: verify

verify:
	cd backend && uv run python -c "import sys; assert sys.version_info[:2] == (3, 12)"
	cd backend && uv run ruff check .
	cd backend && uv run pytest
