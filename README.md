# Engineering Excellence
engineering excellence

### Open Hands: (openhands-fastapi)

Prompt 1
> create basic fast api project following all best practice. The project contains 4 crud apis of user. User model contain name id and email only.

### Augment Code: (dev)

Prompt 1:
> create folder named backend inside which create basic fast api project following all best practice. The project contains 4 crud apis of user. User model contain name id and email only. Use Mongo Db as database. use docker to do complete setup. i will only need to run 1 command docker compose up to run the project

Prompt 2:
> write unit tests for fast api

=======

# Engineering Excellence

A FastAPI backend project with MongoDB, designed for engineering excellence with standardized development environments using dev containers.

## 🚀 Quick Start with Dev Container

This project uses VS Code Dev Containers to provide a consistent, reproducible development environment across different machines and operating systems.

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed and running
- [VS Code](https://code.visualstudio.com/) with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Getting Started

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd engr-excellence
   ```

2. **Open in Dev Container:**

   - Open VS Code
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Dev Containers: Reopen in Container"
   - Select the command and wait for the container to build

3. **Start developing:**
   The dev container will automatically:
   - Install all Python dependencies
   - Set up pre-commit hooks
   - Configure the development environment
   - Start MongoDB and other services

### Development Commands

Once inside the dev container, you can use these convenient commands:

```bash
# Start the FastAPI development server
./dev.sh server
# or
dev-server

# Run tests
./dev.sh test
# or
dev-test

# Run tests in watch mode
./dev.sh test-watch
# or
dev-test-watch

# Format code (black + isort)
./dev.sh format
# or
dev-format

# Lint code (flake8 + mypy)
./dev.sh lint
# or
dev-lint

# Run full check (format + lint + test)
./dev.sh check
# or
dev-check

# Reset development database
./dev.sh reset-db
# or
dev-reset-db

# Show all available commands
./dev.sh help
```

### Services Available

When the dev container is running, these services are available:

- **FastAPI Application**: http://localhost:8000
  - API documentation: http://localhost:8000/docs
  - Alternative docs: http://localhost:8000/redoc
- **MongoDB**: localhost:27017
- **Mongo Express** (Database UI): http://localhost:8081
  - Username: `admin`
  - Password: `admin123`
- **Mailhog** (Email testing): http://localhost:8025
- **Redis**: localhost:6379

### VS Code Features

The dev container comes pre-configured with:

- **Extensions**: Python, Docker, MongoDB, Git, and productivity extensions
- **Debugging**: Pre-configured debug configurations for FastAPI
- **Testing**: Integrated pytest with coverage reporting
- **Code Quality**: Black formatting, isort, flake8 linting, mypy type checking
- **Tasks**: Pre-defined VS Code tasks for common operations

### Project Structure

```
engr-excellence/
├── .devcontainer/          # Dev container configuration
│   ├── devcontainer.json   # Main dev container config
│   ├── Dockerfile.dev      # Development Dockerfile
│   ├── docker-compose.dev.yml  # Development services
│   └── setup.sh           # Post-creation setup script
├── .vscode/               # VS Code workspace settings
│   ├── settings.json      # Editor and Python settings
│   ├── launch.json        # Debug configurations
│   ├── tasks.json         # Build and test tasks
│   └── extensions.json    # Recommended extensions
├── backend/               # FastAPI application
│   ├── app/              # Application code
│   ├── tests/            # Test files
│   ├── requirements.txt  # Production dependencies
│   ├── requirements-dev.txt  # Development dependencies
│   └── .pre-commit-config.yaml  # Code quality hooks
└── dev*.sh               # Development helper scripts
```

## 🛠️ Development Workflow

### Code Quality

The project enforces code quality through:

1. **Pre-commit hooks**: Automatically run on every commit

   - Code formatting (Black, isort)
   - Linting (flake8, mypy)
   - Security checks (bandit)
   - YAML/JSON validation

2. **Continuous testing**: Run tests frequently during development

   ```bash
   # Run tests in watch mode for immediate feedback
   dev-test-watch
   ```

3. **Type checking**: Full mypy type checking enabled
   ```bash
   # Check types
   mypy backend/app/
   ```

### Debugging

The dev container supports multiple debugging approaches:

1. **VS Code Debugger**: Use the pre-configured debug configurations

   - "FastAPI: Debug Server" - Debug the running server
   - "Python: Current File" - Debug the current Python file
   - "Python: Pytest Current File" - Debug current test file

2. **Remote Debugging**: Attach to a running container

   ```bash
   # Start server with debugpy
   python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m uvicorn app.main:app --reload
   ```

3. **Interactive Debugging**: Use ipdb for breakpoint debugging
   ```python
   import ipdb; ipdb.set_trace()
   ```

### Testing Strategy

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test API endpoints and database interactions
- **Coverage Reports**: Maintain high test coverage
- **Continuous Testing**: Use watch mode during development

```bash
# Run specific test file
pytest tests/test_specific.py -v

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run tests matching a pattern
pytest -k "test_user" -v
```

## 🐳 Alternative: Traditional Docker Setup

If you prefer not to use dev containers, you can still use the traditional Docker setup:

```bash
# Navigate to backend directory
cd backend

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔧 Troubleshooting

### Common Issues

1. **Container won't start**:

   - Ensure Docker is running
   - Check if ports 8000, 27017, 8081 are available
   - Try rebuilding: "Dev Containers: Rebuild Container"

2. **Python dependencies issues**:

   - Rebuild the container to get fresh dependencies
   - Check if requirements files are properly formatted

3. **Database connection issues**:

   - Ensure MongoDB container is running
   - Check the connection string in environment variables
   - Try resetting the database: `dev-reset-db`

4. **VS Code extensions not working**:
   - Reload the window: "Developer: Reload Window"
   - Check if extensions are installed in the container

### Performance Tips

- Use volume mounts for better file system performance
- Exclude unnecessary files from Docker context
- Use multi-stage builds for production images
- Keep containers running to avoid rebuild time

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/remote/containers)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [Python Testing with pytest](https://docs.pytest.org/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes in the dev container
4. Run the full check: `dev-check`
5. Commit your changes (pre-commit hooks will run)
6. Push to your fork and create a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
