.PHONY: install run-backend test lint format clean

install:
	pip install -r backend/requirements.txt
	cd frontend && npm install

run-backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	cd backend && python -m pytest tests/

lint:
	ruff check backend/app
	mypy --config-file pyproject.toml backend/app

format:
	black backend/app backend/tests
	isort backend/app backend/tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.py[co]" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
