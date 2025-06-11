#!/bin/bash

# Post-creation setup script for dev container
set -e

echo "🚀 Setting up development environment..."

# Navigate to workspace
cd /workspace

# Install Python dependencies
echo "📦 Installing Python dependencies..."
if [ -f "backend/requirements-dev.txt" ]; then
    pip install --user -r backend/requirements-dev.txt
    echo "✅ Development dependencies installed"
else
    echo "⚠️  requirements-dev.txt not found, installing basic requirements..."
    if [ -f "backend/requirements.txt" ]; then
        pip install --user -r backend/requirements.txt
    fi
fi

# Set up pre-commit hooks
echo "🔧 Setting up pre-commit hooks..."
if command -v pre-commit &> /dev/null; then
    cd backend
    if [ -f ".pre-commit-config.yaml" ]; then
        pre-commit install
        echo "✅ Pre-commit hooks installed"
    else
        echo "⚠️  .pre-commit-config.yaml not found, skipping pre-commit setup"
    fi
    cd ..
else
    echo "⚠️  pre-commit not available, skipping pre-commit setup"
fi

# Create useful development scripts
echo "📝 Creating development scripts..."

# Create a script to run the FastAPI server
cat > /workspace/dev-server.sh << 'EOF'
#!/bin/bash
cd /workspace/backend
echo "🚀 Starting FastAPI development server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
EOF
chmod +x /workspace/dev-server.sh

# Create a script to run tests
cat > /workspace/dev-test.sh << 'EOF'
#!/bin/bash
cd /workspace/backend
echo "🧪 Running tests..."
python -m pytest tests/ -v --cov=app --cov-report=html --cov-report=term
EOF
chmod +x /workspace/dev-test.sh

# Create a script to run tests with watch
cat > /workspace/dev-test-watch.sh << 'EOF'
#!/bin/bash
cd /workspace/backend
echo "👀 Running tests in watch mode..."
ptw tests/ -- -v --cov=app --cov-report=term
EOF
chmod +x /workspace/dev-test-watch.sh

# Create a script to format code
cat > /workspace/dev-format.sh << 'EOF'
#!/bin/bash
cd /workspace/backend
echo "🎨 Formatting code..."
black app/ tests/
isort app/ tests/
echo "✅ Code formatted"
EOF
chmod +x /workspace/dev-format.sh

# Create a script to lint code
cat > /workspace/dev-lint.sh << 'EOF'
#!/bin/bash
cd /workspace/backend
echo "🔍 Linting code..."
flake8 app/ tests/
mypy app/
echo "✅ Linting complete"
EOF
chmod +x /workspace/dev-lint.sh

# Create a script to reset database
cat > /workspace/dev-reset-db.sh << 'EOF'
#!/bin/bash
echo "🗑️  Resetting development database..."
docker-compose -f .devcontainer/docker-compose.dev.yml exec mongo mongosh fastapi_db_dev --eval "db.dropDatabase()"
echo "✅ Database reset complete"
EOF
chmod +x /workspace/dev-reset-db.sh

# Create a comprehensive development script
cat > /workspace/dev.sh << 'EOF'
#!/bin/bash

# Development helper script
case "$1" in
    "server"|"run")
        ./dev-server.sh
        ;;
    "test")
        ./dev-test.sh
        ;;
    "test-watch"|"tw")
        ./dev-test-watch.sh
        ;;
    "format"|"fmt")
        ./dev-format.sh
        ;;
    "lint")
        ./dev-lint.sh
        ;;
    "reset-db")
        ./dev-reset-db.sh
        ;;
    "check")
        echo "🔍 Running full code check..."
        ./dev-format.sh
        ./dev-lint.sh
        ./dev-test.sh
        ;;
    "help"|*)
        echo "🛠️  Development helper script"
        echo ""
        echo "Usage: ./dev.sh [command]"
        echo ""
        echo "Commands:"
        echo "  server, run     Start the FastAPI development server"
        echo "  test            Run tests once"
        echo "  test-watch, tw  Run tests in watch mode"
        echo "  format, fmt     Format code with black and isort"
        echo "  lint            Run linting with flake8 and mypy"
        echo "  reset-db        Reset the development database"
        echo "  check           Run format, lint, and test"
        echo "  help            Show this help message"
        ;;
esac
EOF
chmod +x /workspace/dev.sh

# Set up shell aliases
echo "🐚 Setting up shell aliases..."
cat >> ~/.bashrc << 'EOF'

# Development aliases
alias dev-server='cd /workspace && ./dev-server.sh'
alias dev-test='cd /workspace && ./dev-test.sh'
alias dev-test-watch='cd /workspace && ./dev-test-watch.sh'
alias dev-format='cd /workspace && ./dev-format.sh'
alias dev-lint='cd /workspace && ./dev-lint.sh'
alias dev-check='cd /workspace && ./dev.sh check'
alias dev-reset-db='cd /workspace && ./dev-reset-db.sh'

# Quick navigation
alias backend='cd /workspace/backend'
alias tests='cd /workspace/backend/tests'

# Git aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline'
alias gb='git branch'
alias gco='git checkout'
EOF

# Copy aliases to zshrc as well
cat >> ~/.zshrc << 'EOF'

# Development aliases
alias dev-server='cd /workspace && ./dev-server.sh'
alias dev-test='cd /workspace && ./dev-test.sh'
alias dev-test-watch='cd /workspace && ./dev-test-watch.sh'
alias dev-format='cd /workspace && ./dev-format.sh'
alias dev-lint='cd /workspace && ./dev-lint.sh'
alias dev-check='cd /workspace && ./dev.sh check'
alias dev-reset-db='cd /workspace && ./dev-reset-db.sh'

# Quick navigation
alias backend='cd /workspace/backend'
alias tests='cd /workspace/backend/tests'

# Git aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline'
alias gb='git branch'
alias gco='git checkout'
EOF

# Create .env.dev file if it doesn't exist
if [ ! -f "/workspace/backend/.env.dev" ]; then
    echo "📄 Creating development environment file..."
    cat > /workspace/backend/.env.dev << 'EOF'
# Development environment variables
DEBUG=True
MONGODB_URL=mongodb://mongo:27017
DATABASE_NAME=fastapi_db_dev
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis (if using)
REDIS_URL=redis://redis:6379

# Email (using Mailhog for development)
SMTP_HOST=mailhog
SMTP_PORT=1025
SMTP_USER=
SMTP_PASSWORD=
SMTP_TLS=False
SMTP_SSL=False

# Logging
LOG_LEVEL=DEBUG
EOF
    echo "✅ Development environment file created"
fi

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "📚 Quick start commands:"
echo "  ./dev.sh server     - Start the FastAPI server"
echo "  ./dev.sh test       - Run tests"
echo "  ./dev.sh check      - Format, lint, and test"
echo "  ./dev.sh help       - Show all available commands"
echo ""
echo "🌐 Services will be available at:"
echo "  FastAPI:      http://localhost:8000"
echo "  Mongo Express: http://localhost:8081"
echo "  Mailhog:      http://localhost:8025"
echo ""
echo "Happy coding! 🚀"
