.PHONY: install

install:
	cd backend && uv venv --python 3.12
	cd backend && uv pip install -e .
