# Makefile for Frontend Testing with Docker
# Provides convenient commands for running tests in Docker containers

.PHONY: help test test-watch test-coverage test-file test-ci build-test clean setup

# Default target
.DEFAULT_GOAL := help

# Variables
DOCKER_IMAGE_NAME := frontend-test
DOCKER_COMPOSE_FILE := docker-compose.test.yml
COVERAGE_DIR := ./coverage

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "Frontend Docker Testing Commands"
	@echo ""
	@echo "Usage: make [TARGET]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(BLUE)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "Examples:"
	@echo "  make test                    # Run all tests"
	@echo "  make test-coverage          # Run tests with coverage"
	@echo "  make test-file FILE=user-form.test.tsx  # Run specific test"
	@echo ""

setup: ## Install dependencies and setup environment
	@echo "$(BLUE)[INFO]$(NC) Setting up development environment..."
	npm install
	@echo "$(GREEN)[SUCCESS]$(NC) Environment setup complete"

build-test: ## Build Docker test image
	@echo "$(BLUE)[INFO]$(NC) Building test Docker image..."
	docker build -t $(DOCKER_IMAGE_NAME) .
	@echo "$(GREEN)[SUCCESS]$(NC) Test image built successfully"

test: build-test ## Run all tests in Docker
	@echo "$(BLUE)[INFO]$(NC) Running all tests in Docker..."
	docker run --rm \
		-v $$(pwd):/app \
		-v /app/node_modules \
		-e CI=true \
		$(DOCKER_IMAGE_NAME) npm test
	@echo "$(GREEN)[SUCCESS]$(NC) All tests completed"

test-watch: build-test ## Run tests in watch mode
	@echo "$(BLUE)[INFO]$(NC) Running tests in watch mode..."
	@echo "$(YELLOW)[WARNING]$(NC) Press Ctrl+C to exit watch mode"
	docker run --rm -it \
		-v $$(pwd):/app \
		-v /app/node_modules \
		-e CI=false \
		$(DOCKER_IMAGE_NAME) npm run test:watch

test-coverage: build-test ## Run tests with coverage report
	@echo "$(BLUE)[INFO]$(NC) Running tests with coverage..."
	docker run --rm \
		-v $$(pwd):/app \
		-v /app/node_modules \
		-v $$(pwd)/coverage:/app/coverage \
		-e CI=true \
		$(DOCKER_IMAGE_NAME) npm run test:coverage
	@echo "$(GREEN)[SUCCESS]$(NC) Tests with coverage completed"
	@echo "$(BLUE)[INFO]$(NC) Coverage report available at: $(COVERAGE_DIR)/lcov-report/index.html"

test-file: build-test ## Run specific test file (usage: make test-file FILE=filename.test.tsx)
ifndef FILE
	@echo "$(RED)[ERROR]$(NC) Please specify a test file"
	@echo "Usage: make test-file FILE=user-form.test.tsx"
	@exit 1
endif
	@echo "$(BLUE)[INFO]$(NC) Running test file: $(FILE)"
	docker run --rm \
		-v $$(pwd):/app \
		-v /app/node_modules \
		-e CI=true \
		$(DOCKER_IMAGE_NAME) npm test -- $(FILE)
	@echo "$(GREEN)[SUCCESS]$(NC) Test file completed: $(FILE)"

test-ci: build-test ## Run tests in CI mode with optimizations
	@echo "$(BLUE)[INFO]$(NC) Running tests in CI mode..."
	docker run --rm \
		-v $$(pwd):/app \
		-v /app/node_modules \
		-e CI=true \
		-e NODE_OPTIONS="--max-old-space-size=4096" \
		$(DOCKER_IMAGE_NAME) npm test -- --ci --coverage --watchAll=false --passWithNoTests
	@echo "$(GREEN)[SUCCESS]$(NC) CI tests completed"

# Docker Compose targets
compose-test: ## Run tests using Docker Compose
	@echo "$(BLUE)[INFO]$(NC) Running tests with Docker Compose..."
	docker-compose -f $(DOCKER_COMPOSE_FILE) run --rm frontend-test
	@echo "$(GREEN)[SUCCESS]$(NC) Docker Compose tests completed"

compose-coverage: ## Run coverage tests using Docker Compose
	@echo "$(BLUE)[INFO]$(NC) Running coverage tests with Docker Compose..."
	docker-compose -f $(DOCKER_COMPOSE_FILE) run --rm frontend-test-coverage
	@echo "$(GREEN)[SUCCESS]$(NC) Docker Compose coverage tests completed"

compose-watch: ## Run tests in watch mode using Docker Compose
	@echo "$(BLUE)[INFO]$(NC) Running tests in watch mode with Docker Compose..."
	@echo "$(YELLOW)[WARNING]$(NC) Press Ctrl+C to exit watch mode"
	docker-compose -f $(DOCKER_COMPOSE_FILE) run --rm frontend-test-watch

# Utility targets
clean: ## Clean up Docker containers and images
	@echo "$(BLUE)[INFO]$(NC) Cleaning up Docker resources..."
	-docker ps -a --filter "ancestor=$(DOCKER_IMAGE_NAME)" --format "{{.ID}}" | xargs -r docker rm -f
	-docker rmi $(DOCKER_IMAGE_NAME) 2>/dev/null
	-docker image prune -f
	@echo "$(GREEN)[SUCCESS]$(NC) Docker cleanup completed"

clean-coverage: ## Remove coverage reports
	@echo "$(BLUE)[INFO]$(NC) Removing coverage reports..."
	rm -rf $(COVERAGE_DIR)
	@echo "$(GREEN)[SUCCESS]$(NC) Coverage reports removed"

lint: ## Run ESLint
	@echo "$(BLUE)[INFO]$(NC) Running ESLint..."
	npm run lint
	@echo "$(GREEN)[SUCCESS]$(NC) Linting completed"

type-check: ## Run TypeScript type checking
	@echo "$(BLUE)[INFO]$(NC) Running TypeScript type check..."
	npm run type-check
	@echo "$(GREEN)[SUCCESS]$(NC) Type checking completed"

# Development targets
dev: ## Start development server
	@echo "$(BLUE)[INFO]$(NC) Starting development server..."
	npm run dev

build: ## Build for production
	@echo "$(BLUE)[INFO]$(NC) Building for production..."
	npm run build
	@echo "$(GREEN)[SUCCESS]$(NC) Production build completed"

# Combined targets
check: lint type-check test ## Run all checks (lint, type-check, test)
	@echo "$(GREEN)[SUCCESS]$(NC) All checks completed successfully"

ci: clean build-test test-ci lint type-check ## Run full CI pipeline
	@echo "$(GREEN)[SUCCESS]$(NC) CI pipeline completed successfully"

# Docker health check
docker-check: ## Check if Docker is running
	@docker info > /dev/null 2>&1 || (echo "$(RED)[ERROR]$(NC) Docker is not running" && exit 1)
	@echo "$(GREEN)[SUCCESS]$(NC) Docker is running"

# Show test results
show-coverage: ## Open coverage report in browser (macOS/Linux)
	@if [ -f "$(COVERAGE_DIR)/lcov-report/index.html" ]; then \
		echo "$(BLUE)[INFO]$(NC) Opening coverage report..."; \
		if command -v open > /dev/null; then \
			open $(COVERAGE_DIR)/lcov-report/index.html; \
		elif command -v xdg-open > /dev/null; then \
			xdg-open $(COVERAGE_DIR)/lcov-report/index.html; \
		else \
			echo "$(YELLOW)[WARNING]$(NC) Please open $(COVERAGE_DIR)/lcov-report/index.html manually"; \
		fi; \
	else \
		echo "$(RED)[ERROR]$(NC) Coverage report not found. Run 'make test-coverage' first."; \
	fi

# Debug targets
debug-test: build-test ## Run tests with verbose output for debugging
	@echo "$(BLUE)[INFO]$(NC) Running tests in debug mode..."
	docker run --rm -it \
		-v $$(pwd):/app \
		-v /app/node_modules \
		-e CI=true \
		$(DOCKER_IMAGE_NAME) npm test -- --verbose

shell: build-test ## Open shell in test container for debugging
	@echo "$(BLUE)[INFO]$(NC) Opening shell in test container..."
	docker run --rm -it \
		-v $$(pwd):/app \
		-v /app/node_modules \
		$(DOCKER_IMAGE_NAME) /bin/sh
