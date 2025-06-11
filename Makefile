.PHONY: help build up down logs clean install-frontend install-backend dev-frontend dev-backend test

# Default target
help:
	@echo "Available commands:"
	@echo "  build           - Build all Docker images"
	@echo "  up              - Start all services with Docker Compose"
	@echo "  down            - Stop all services"
	@echo "  logs            - Show logs from all services"
	@echo "  clean           - Clean up Docker containers and images"
	@echo "  install-frontend - Install frontend dependencies"
	@echo "  install-backend  - Install backend dependencies"
	@echo "  dev-frontend    - Start frontend in development mode"
	@echo "  dev-backend     - Start backend in development mode"
	@echo "  test            - Run backend tests"

# Docker commands
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v --rmi all --remove-orphans

# Local development commands
install-frontend:
	cd frontend && npm install

install-backend:
	cd backend && pip install -r requirements.txt

dev-frontend:
	cd frontend && npm run dev

dev-backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	cd backend && pytest

# Combined commands
install: install-frontend install-backend

dev: 
	@echo "Starting development servers..."
	@echo "Backend will be available at http://localhost:8000"
	@echo "Frontend will be available at http://localhost:3000"
	@echo "Press Ctrl+C to stop"
	@make -j2 dev-frontend dev-backend
