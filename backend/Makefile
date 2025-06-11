.PHONY: test test-unit test-integration test-coverage test-watch install-dev lint format clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  test              - Run all tests"
	@echo "  test-unit         - Run unit tests only"
	@echo "  test-integration  - Run integration tests only"
	@echo "  test-coverage     - Run tests with coverage report"
	@echo "  test-watch        - Run tests in watch mode"
	@echo "  install-dev       - Install development dependencies"
	@echo "  lint              - Run linting checks"
	@echo "  format            - Format code"
	@echo "  clean             - Clean up generated files"

# Install development dependencies
install-dev:
	pip install -r requirements.txt

# Run all tests
test:
	cd .. && docker compose exec backend python -m pytest tests/ -v --asyncio-mode=auto

# Run unit tests only
test-unit:
	cd .. && docker compose exec backend python -m pytest tests/unit/ -v --asyncio-mode=auto

# Run integration tests only
test-integration:
	cd .. && docker compose exec backend python -m pytest tests/integration/ -v --asyncio-mode=auto -m integration

# Run tests with coverage
test-coverage:
	cd .. && docker compose exec backend python -m pytest tests/ --cov=app --cov-report=html --cov-report=term-missing --cov-fail-under=80 --asyncio-mode=auto

# Run tests in watch mode (requires pytest-watch)
test-watch:
	cd .. && docker compose exec backend ptw tests/ app/ --runner "python -m pytest --asyncio-mode=auto"

# Run linting checks
lint:
	cd .. && docker compose exec backend python -m flake8 app/ tests/
	cd .. && docker compose exec backend python -m mypy app/

# Format code
format:
	cd .. && docker compose exec backend python -m black app/ tests/
	cd .. && docker compose exec backend python -m isort app/ tests/

# Clean up generated files
clean:
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Docker-based testing
test-docker:
	cd .. && docker compose exec backend python -m pytest tests/ -v

test-docker-coverage:
	cd .. && docker compose exec backend python -m pytest tests/ --cov=app --cov-report=html --cov-report=term-missing
