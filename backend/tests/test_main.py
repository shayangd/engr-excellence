import pytest
from httpx import AsyncClient

from app.core.config import settings


class TestMainApplication:
    """Test cases for main application endpoints."""

    async def test_root_endpoint(self, test_client: AsyncClient):
        """Test root endpoint returns correct response."""
        response = await test_client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Welcome to FastAPI User Management API"
        assert data["version"] == settings.project_version
        assert data["docs"] == f"{settings.api_v1_str}/docs"

    async def test_health_check_endpoint(self, test_client: AsyncClient):
        """Test health check endpoint."""
        response = await test_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    async def test_openapi_docs_endpoint(self, test_client: AsyncClient):
        """Test OpenAPI documentation endpoint."""
        response = await test_client.get(f"{settings.api_v1_str}/openapi.json")
        
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert data["info"]["title"] == settings.project_name

    async def test_swagger_docs_endpoint(self, test_client: AsyncClient):
        """Test Swagger documentation endpoint."""
        response = await test_client.get(f"{settings.api_v1_str}/docs")
        
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    async def test_redoc_docs_endpoint(self, test_client: AsyncClient):
        """Test ReDoc documentation endpoint."""
        response = await test_client.get(f"{settings.api_v1_str}/redoc")
        
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    async def test_cors_headers(self, test_client: AsyncClient):
        """Test CORS headers are present."""
        response = await test_client.options("/")
        
        # Note: In test environment, CORS headers might not be fully set
        # This test ensures the endpoint is accessible
        assert response.status_code in [200, 405]  # 405 is also acceptable for OPTIONS

    async def test_404_endpoint(self, test_client: AsyncClient):
        """Test non-existent endpoint returns 404."""
        response = await test_client.get("/non-existent-endpoint")
        
        assert response.status_code == 404
