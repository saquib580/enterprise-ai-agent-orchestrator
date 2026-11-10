PYTHON ?= python3
VENV := backend/.venv
BIN := $(VENV)/bin

.PHONY: install install-dev run test lint format typecheck check clean

install:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/python -m pip install --upgrade pip
	$(BIN)/pip install -r backend/requirements/base.txt

install-dev:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/python -m pip install --upgrade pip
	$(BIN)/pip install -r backend/requirements/dev.txt

run:
	cd backend && ../$(BIN)/uvicorn main:app --host 127.0.0.1 --port 8000 --reload

test:
	cd backend && ../$(BIN)/pytest -v

lint:
	cd backend && ../$(BIN)/ruff check .

format:
	cd backend && ../$(BIN)/ruff format .

typecheck:
	cd backend && ../$(BIN)/mypy app main.py

check: lint typecheck test

clean:
	rm -rf $(VENV) backend/.pytest_cache backend/.mypy_cache backend/.ruff_cache
	find backend -type d -name __pycache__ -prune -exec rm -rf {} +
