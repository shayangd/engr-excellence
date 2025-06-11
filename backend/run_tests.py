#!/usr/bin/env python3
"""
Test runner script for FastAPI User Management API.

This script provides different ways to run tests:
- All tests
- Unit tests only
- Integration tests only
- Specific test files
- With coverage reporting
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command: list[str]) -> int:
    """Run a command and return the exit code."""
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command)
    return result.returncode


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run tests for FastAPI User Management API")
    parser.add_argument(
        "--type",
        choices=["all", "unit", "integration"],
        default="all",
        help="Type of tests to run (default: all)"
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Run tests with coverage reporting"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--file",
        help="Run specific test file"
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run tests in parallel"
    )
    
    args = parser.parse_args()
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add verbosity
    if args.verbose:
        cmd.append("-v")
    
    # Add parallel execution
    if args.parallel:
        cmd.extend(["-n", "auto"])
    
    # Add coverage if requested
    if args.coverage:
        cmd.extend([
            "--cov=app",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-fail-under=80"
        ])
    
    # Determine what tests to run
    if args.file:
        cmd.append(args.file)
    elif args.type == "unit":
        cmd.extend(["-m", "unit", "tests/unit/"])
    elif args.type == "integration":
        cmd.extend(["-m", "integration", "tests/integration/"])
    else:
        cmd.append("tests/")
    
    # Run the tests
    exit_code = run_command(cmd)
    
    if args.coverage and exit_code == 0:
        print("\nCoverage report generated in htmlcov/index.html")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
