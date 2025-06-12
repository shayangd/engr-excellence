# Frontend Testing Guide

This guide covers how to run tests for the frontend application both locally and inside Docker containers.

## Table of Contents

- [Local Testing](#local-testing)
- [Docker Testing](#docker-testing)
- [Test Structure](#test-structure)
- [Coverage Reports](#coverage-reports)
- [Troubleshooting](#troubleshooting)

## Local Testing

### Prerequisites

- Node.js 18+ installed
- npm or yarn package manager

### Setup

1. Install dependencies:

```bash
npm install
```

2. Run tests:

```bash
# Run all tests once
npm test

# Run tests in watch mode (for development)
npm run test:watch

# Run tests with coverage report
npm run test:coverage
```

### Available Test Scripts

| Command                 | Description                    |
| ----------------------- | ------------------------------ |
| `npm test`              | Run all tests once             |
| `npm run test:watch`    | Run tests in watch mode        |
| `npm run test:coverage` | Run tests with coverage report |

## Docker Testing

### Quick Start with Helper Scripts

We provide several convenient ways to run tests in Docker:

#### Using the Test Script (Recommended)

```bash
# Make the script executable (first time only)
chmod +x scripts/test-docker.sh

# Run all tests
./scripts/test-docker.sh test

# Run tests with coverage
./scripts/test-docker.sh test-coverage

# Run tests in watch mode
./scripts/test-docker.sh test-watch

# Run specific test file
./scripts/test-docker.sh test-file user-form.test.tsx
```

#### Using Makefile

```bash
# Run all tests
make test

# Run tests with coverage
make test-coverage

# Run tests in watch mode
make test-watch

# Run specific test file
make test-file FILE=user-form.test.tsx

# Show all available commands
make help
```

### Method 1: Using Docker Compose (Recommended)

This method uses the existing Docker Compose setup and runs tests inside the frontend container.

#### Prerequisites

- Docker and Docker Compose installed
- Frontend service defined in `docker-compose.yml`

#### Running Tests

1. **Start the frontend container:**

```bash
# From the project root
docker-compose up frontend -d
```

2. **Run tests inside the container:**

```bash
# Run all tests
docker-compose exec frontend npm test

# Run tests in watch mode (useful for development)
docker-compose exec frontend npm run test:watch

# Run tests with coverage
docker-compose exec frontend npm run test:coverage
```

3. **Run tests without starting services:**

```bash
# Run tests in a temporary container
docker-compose run --rm frontend npm test

# Run tests with coverage in a temporary container
docker-compose run --rm frontend npm run test:coverage
```

#### Example Output

```bash
$ docker-compose exec frontend npm test

> user-management-frontend@0.1.0 test
> jest

Test Suites: 10 passed, 10 total
Tests:       110 passed, 110 total
Snapshots:   0 total
Time:        2.673 s
Ran all test suites.
```

### Method 2: Using Docker Run Commands

If you prefer to run tests without Docker Compose:

#### Build the Image

```bash
# From the frontend directory
docker build -t frontend-tests .
```

#### Run Tests

```bash
# Run all tests
docker run --rm frontend-tests npm test

# Run tests with coverage
docker run --rm frontend-tests npm run test:coverage

# Run tests interactively (for debugging)
docker run --rm -it frontend-tests npm test
```

### Method 3: Docker Compose Override for Testing

Create a `docker-compose.test.yml` file:

```yaml
version: "3.8"
services:
  frontend-test:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm test
    environment:
      - CI=true
```

Run tests:

```bash
docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm frontend-test
```

## Docker Configuration Files

### Available Docker Files

| File                      | Purpose                                  |
| ------------------------- | ---------------------------------------- |
| `Dockerfile`              | Main Dockerfile (used for testing too)   |
| `docker-compose.test.yml` | Docker Compose configuration for testing |

### Available Scripts

| Script                   | Purpose                                            |
| ------------------------ | -------------------------------------------------- |
| `scripts/test-docker.sh` | Comprehensive testing script with multiple options |
| `Makefile`               | Make targets for common testing tasks              |

### Docker Compose Services

| Service                  | Command                 | Purpose                 |
| ------------------------ | ----------------------- | ----------------------- |
| `frontend-test`          | `npm test`              | Run all tests once      |
| `frontend-test-coverage` | `npm run test:coverage` | Run tests with coverage |
| `frontend-test-watch`    | `npm run test:watch`    | Run tests in watch mode |
| `frontend-test-file`     | Custom                  | Run specific test files |

## Test Structure

Our test suite includes:

### Test Categories

- **Unit Tests**: Individual functions and components
- **Integration Tests**: Component interactions
- **API Tests**: HTTP client functionality
- **UI Component Tests**: Reusable UI components

### Test Files

```
frontend/src/__tests__/
├── components/
│   ├── user-form.test.tsx
│   ├── user-list.test.tsx
│   └── ui/
│       ├── button.test.tsx
│       ├── input.test.tsx
│       ├── card.test.tsx
│       ├── loading.test.tsx
│       └── error.test.tsx
├── lib/
│   ├── api.test.ts
│   ├── utils.test.ts
│   └── validations.test.ts
└── setup/
    └── test-setup.ts
```

### Test Coverage

- **110 tests** across 10 test suites
- **60%+ overall coverage**
- **90%+ coverage** on core business logic

## Coverage Reports

### Viewing Coverage in Docker

1. **Generate coverage report:**

```bash
docker-compose exec frontend npm run test:coverage
```

2. **Copy coverage report to host (optional):**

```bash
# Copy HTML coverage report
docker cp $(docker-compose ps -q frontend):/app/coverage ./coverage
```

3. **View coverage report:**

```bash
# Open coverage/lcov-report/index.html in your browser
open coverage/lcov-report/index.html
```

### Coverage Thresholds

Our Jest configuration enforces these coverage thresholds:

- **Statements**: 80%
- **Branches**: 80%
- **Functions**: 80%
- **Lines**: 80%

## Troubleshooting

### Common Issues

#### 1. Tests Fail in Docker but Pass Locally

```bash
# Check Node.js version consistency
docker-compose exec frontend node --version

# Ensure dependencies are properly installed
docker-compose exec frontend npm ci
```

#### 2. Permission Issues with Coverage Reports

```bash
# Fix file permissions
docker-compose exec frontend chown -R $(id -u):$(id -g) coverage/
```

#### 3. Out of Memory Errors

```bash
# Increase memory limit for the container
docker-compose exec frontend npm test -- --maxWorkers=2
```

#### 4. Watch Mode Not Working in Docker

```bash
# Use polling for file watching in containers
docker-compose exec frontend npm test -- --watchAll --watchman=false
```

### Debug Mode

Run tests in debug mode:

```bash
# Interactive debugging
docker-compose run --rm -it frontend npm test -- --verbose

# Debug specific test file
docker-compose exec frontend npm test -- user-form.test.tsx --verbose
```

### Environment Variables

Set testing environment variables:

```bash
# Run with specific environment
docker-compose exec -e NODE_ENV=test frontend npm test

# Run with CI mode
docker-compose exec -e CI=true frontend npm test
```

## Best Practices

1. **Use CI mode in automated environments:**

   ```bash
   docker-compose run --rm -e CI=true frontend npm test
   ```

2. **Run tests before building production images:**

   ```bash
   docker-compose run --rm frontend npm test && docker-compose build frontend
   ```

3. **Use specific test commands for different scenarios:**

   ```bash
   # Quick smoke test
   docker-compose run --rm frontend npm test -- --passWithNoTests

   # Full test suite with coverage
   docker-compose run --rm frontend npm run test:coverage
   ```

4. **Clean up test containers:**
   ```bash
   # Remove test containers after running
   docker-compose run --rm frontend npm test
   ```

## Integration with CI/CD

Example GitHub Actions workflow:

```yaml
name: Frontend Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests in Docker
        run: |
          docker-compose run --rm -e CI=true frontend npm test
          docker-compose run --rm -e CI=true frontend npm run test:coverage
```

For more information about the test suite structure and individual test files, see the test files in `src/__tests__/`.
