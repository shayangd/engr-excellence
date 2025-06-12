#!/bin/bash

# Frontend Docker Testing Script
# This script provides convenient commands for running tests in Docker containers

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Frontend Docker Testing Script"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  test                Run all tests once"
    echo "  test-watch          Run tests in watch mode"
    echo "  test-coverage       Run tests with coverage report"
    echo "  test-file [FILE]    Run specific test file"
    echo "  test-ci             Run tests in CI mode"
    echo "  build-test          Build test Docker image"
    echo "  clean               Clean up test containers and images"
    echo "  help                Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 test                                    # Run all tests"
    echo "  $0 test-coverage                           # Run with coverage"
    echo "  $0 test-file user-form.test.tsx          # Run specific test"
    echo "  $0 test-watch                             # Run in watch mode"
    echo ""
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to build test image
build_test_image() {
    print_status "Building test Docker image..."
    docker build -t frontend-test .
    print_success "Test image built successfully"
}

# Function to run all tests
run_tests() {
    print_status "Running all tests in Docker..."
    docker run --rm \
        -v "$(pwd):/app" \
        -v "/app/node_modules" \
        -e CI=true \
        frontend-test npm test
    print_success "All tests completed"
}

# Function to run tests with coverage
run_tests_coverage() {
    print_status "Running tests with coverage in Docker..."
    docker run --rm \
        -v "$(pwd):/app" \
        -v "/app/node_modules" \
        -v "$(pwd)/coverage:/app/coverage" \
        -e CI=true \
        frontend-test npm run test:coverage
    print_success "Tests with coverage completed"
    print_status "Coverage report available in ./coverage/lcov-report/index.html"
}

# Function to run tests in watch mode
run_tests_watch() {
    print_status "Running tests in watch mode..."
    print_warning "Press Ctrl+C to exit watch mode"
    docker run --rm -it \
        -v "$(pwd):/app" \
        -v "/app/node_modules" \
        -e CI=false \
        frontend-test npm run test:watch
}

# Function to run specific test file
run_test_file() {
    local test_file="$1"
    if [ -z "$test_file" ]; then
        print_error "Please specify a test file"
        echo "Usage: $0 test-file [FILE]"
        exit 1
    fi
    
    print_status "Running test file: $test_file"
    docker run --rm \
        -v "$(pwd):/app" \
        -v "/app/node_modules" \
        -e CI=true \
        frontend-test npm test -- "$test_file"
    print_success "Test file completed: $test_file"
}

# Function to run tests in CI mode
run_tests_ci() {
    print_status "Running tests in CI mode..."
    docker run --rm \
        -v "$(pwd):/app" \
        -v "/app/node_modules" \
        -e CI=true \
        -e NODE_OPTIONS="--max-old-space-size=4096" \
        frontend-test npm test -- --ci --coverage --watchAll=false --passWithNoTests
    print_success "CI tests completed"
}

# Function to clean up Docker resources
clean_docker() {
    print_status "Cleaning up Docker test resources..."
    
    # Remove test containers
    docker ps -a --filter "ancestor=frontend-test" --format "{{.ID}}" | xargs -r docker rm -f
    
    # Remove test image
    docker rmi frontend-test 2>/dev/null || true
    
    # Clean up dangling images
    docker image prune -f
    
    print_success "Docker cleanup completed"
}

# Function to run using Docker Compose
run_with_compose() {
    local service="$1"
    local command="$2"
    
    print_status "Running tests using Docker Compose..."
    
    if [ -n "$command" ]; then
        docker-compose -f docker-compose.test.yml run --rm "$service" $command
    else
        docker-compose -f docker-compose.test.yml run --rm "$service"
    fi
}

# Main script logic
main() {
    # Check if Docker is available
    check_docker
    
    # Parse command line arguments
    case "${1:-help}" in
        "test")
            build_test_image
            run_tests
            ;;
        "test-watch")
            build_test_image
            run_tests_watch
            ;;
        "test-coverage")
            build_test_image
            run_tests_coverage
            ;;
        "test-file")
            build_test_image
            run_test_file "$2"
            ;;
        "test-ci")
            build_test_image
            run_tests_ci
            ;;
        "build-test")
            build_test_image
            ;;
        "clean")
            clean_docker
            ;;
        "compose-test")
            run_with_compose "frontend-test"
            ;;
        "compose-coverage")
            run_with_compose "frontend-test-coverage"
            ;;
        "compose-watch")
            run_with_compose "frontend-test-watch"
            ;;
        "help"|"--help"|"-h")
            show_usage
            ;;
        *)
            print_error "Unknown command: $1"
            echo ""
            show_usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
