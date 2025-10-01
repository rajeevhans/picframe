# PicFrame Development Makefile
# Provides convenient commands for common development tasks

.PHONY: help install install-dev test test-unit test-integration test-coverage
.PHONY: lint format type-check security-check clean build docs
.PHONY: setup-dev setup-hooks run-debug run-version

# Default target
help:
	@echo "PicFrame Development Commands:"
	@echo ""
	@echo "Setup Commands:"
	@echo "  setup-dev      - Set up development environment"
	@echo "  setup-hooks    - Install pre-commit hooks"
	@echo "  install        - Install PicFrame in development mode"
	@echo "  install-dev    - Install development dependencies"
	@echo ""
	@echo "Code Quality Commands:"
	@echo "  format         - Format code with Black and isort"
	@echo "  lint           - Run linting with flake8 and pylint"
	@echo "  type-check     - Run type checking with mypy"
	@echo "  security-check - Run security checks with bandit"
	@echo "  check-all      - Run all code quality checks"
	@echo ""
	@echo "Testing Commands:"
	@echo "  test           - Run all tests"
	@echo "  test-unit      - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-coverage  - Run tests with coverage report"
	@echo "  test-fast      - Run tests excluding slow ones"
	@echo ""
	@echo "Development Commands:"
	@echo "  run-debug      - Run PicFrame in debug mode"
	@echo "  run-version    - Show version and dependency info"
	@echo "  docs           - Generate documentation"
	@echo "  clean          - Clean build artifacts and cache"
	@echo "  build          - Build distribution packages"

# Setup commands
setup-dev: install install-dev setup-hooks
	@echo "Development environment setup complete!"

setup-hooks:
	@echo "Installing pre-commit hooks..."
	pre-commit install
	@echo "Pre-commit hooks installed!"

install:
	@echo "Installing PicFrame in development mode..."
	pip install -e .

install-dev:
	@echo "Installing development dependencies..."
	pip install -r requirements-dev.txt

# Code quality commands
format:
	@echo "Formatting code with Black..."
	black src/ test/
	@echo "Sorting imports with isort..."
	isort src/ test/
	@echo "Code formatting complete!"

lint:
	@echo "Running flake8..."
	flake8 src/ test/
	@echo "Running pylint..."
	pylint src/picframe/
	@echo "Linting complete!"

type-check:
	@echo "Running mypy type checking..."
	mypy src/
	@echo "Type checking complete!"

security-check:
	@echo "Running bandit security checks..."
	bandit -r src/
	@echo "Security check complete!"

check-all: format lint type-check security-check
	@echo "All code quality checks complete!"

# Testing commands
test:
	@echo "Running all tests..."
	pytest

test-unit:
	@echo "Running unit tests..."
	pytest test/unit/ -v

test-integration:
	@echo "Running integration tests..."
	pytest test/integration/ -v

test-coverage:
	@echo "Running tests with coverage..."
	pytest --cov=src/picframe --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/"

test-fast:
	@echo "Running fast tests (excluding slow ones)..."
	pytest -m "not slow"

# Development commands
run-debug:
	@echo "Running PicFrame in debug mode..."
	python -m picframe.start test/fixtures/configs/debug_config.yaml

run-version:
	@echo "Checking PicFrame version and dependencies..."
	python -m picframe.start -v

docs:
	@echo "Generating documentation..."
	cd docs && make html
	@echo "Documentation generated in docs/_build/html/"

clean:
	@echo "Cleaning build artifacts and cache..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Clean complete!"

build:
	@echo "Building distribution packages..."
	python -m build
	@echo "Build complete! Packages in dist/"

# Development workflow helpers
dev-check: format lint type-check test-fast
	@echo "Development checks complete!"

ci-check: format lint type-check security-check test-coverage
	@echo "CI checks complete!"

# Quick development commands
quick-test:
	@echo "Running quick tests..."
	pytest test/unit/ -x --tb=short

watch-test:
	@echo "Watching for changes and running tests..."
	pytest-watch test/unit/

# Release helpers
check-release: clean ci-check build
	@echo "Release checks complete!"

# Platform-specific helpers
setup-rpi:
	@echo "Setting up Raspberry Pi specific dependencies..."
	sudo apt update
	sudo apt install -y python3-dev libgl1-mesa-dev libgles2-mesa-dev
	pip install -e .
	pip install -r requirements-dev.txt

# Docker helpers (if using Docker for development)
docker-build:
	@echo "Building Docker development image..."
	docker build -t picframe-dev -f Dockerfile.dev .

docker-run:
	@echo "Running PicFrame in Docker container..."
	docker run -it --rm -v $(PWD):/app picframe-dev

# Database/cache management
reset-cache:
	@echo "Resetting image cache..."
	rm -rf ~/.picframe/cache/*
	@echo "Cache reset complete!"

# Dependency management
update-deps:
	@echo "Updating dependencies..."
	pip-compile requirements.in
	pip-compile requirements-dev.in
	@echo "Dependencies updated!"

freeze-deps:
	@echo "Freezing current dependencies..."
	pip freeze > requirements-frozen.txt
	@echo "Dependencies frozen to requirements-frozen.txt"