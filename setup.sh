#!/bin/bash

# User Management System Setup Script
# This script sets up the complete full-stack application

set -e

echo "🚀 Setting up User Management System..."
echo "======================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Stop any existing containers
echo "🛑 Stopping any existing containers..."
docker-compose down --remove-orphans 2>/dev/null || true

# Build all images
echo "🔨 Building Docker images..."
docker-compose build

# Start all services
echo "🚀 Starting all services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check service health
echo "🔍 Checking service health..."

# Check backend
if curl -f http://localhost:8570/health >/dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend is not responding"
fi

# Check frontend
if curl -f http://localhost:8571/api/health >/dev/null 2>&1; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend is not responding"
fi

# Check MongoDB
if docker-compose exec -T mongo mongosh --eval "db.runCommand('ping')" >/dev/null 2>&1; then
    echo "✅ MongoDB is healthy"
else
    echo "❌ MongoDB is not responding"
fi

echo ""
echo "🎉 Setup complete!"
echo "=================="
echo ""
echo "📱 Access your applications:"
echo "   Frontend:      http://localhost:8571"
echo "   Backend API:   http://localhost:8570"
echo "   API Docs:      http://localhost:8570/api/v1/docs"
echo "   MongoDB Admin: http://localhost:8081 (admin/admin123)"
echo ""
echo "🔧 Useful commands:"
echo "   View logs:     docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart:       docker-compose restart"
echo ""
echo "📚 Check the README.md for more information!"
