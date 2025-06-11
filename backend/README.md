# FastAPI User Management API

A modern, fast, and scalable REST API built with FastAPI and MongoDB for user management operations.

## Features

- ✅ **CRUD Operations**: Create, Read, Update, Delete users
- ✅ **MongoDB Integration**: Async MongoDB operations with Motor
- ✅ **Data Validation**: Pydantic models for request/response validation
- ✅ **API Documentation**: Auto-generated OpenAPI/Swagger docs
- ✅ **Docker Support**: Complete containerization with Docker Compose
- ✅ **Error Handling**: Comprehensive error handling and logging
- ✅ **Pagination**: Built-in pagination for user listings
- ✅ **Email Validation**: Email format validation
- ✅ **Database Indexing**: Optimized database queries

## Quick Start

### Prerequisites

- Docker and Docker Compose installed on your system

### Running the Application

1. **Clone and navigate to the backend directory**:

   ```bash
   cd backend
   ```

2. **Start the application**:
   ```bash
   docker-compose up
   ```

That's it! The application will be available at:

- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/v1/docs
- **MongoDB Express** (Database UI): http://localhost:8081 (admin/admin123)

## API Endpoints

### User Management

| Method | Endpoint                  | Description                     |
| ------ | ------------------------- | ------------------------------- |
| POST   | `/api/v1/users/`          | Create a new user               |
| GET    | `/api/v1/users/`          | Get all users (with pagination) |
| GET    | `/api/v1/users/{user_id}` | Get user by ID                  |
| PUT    | `/api/v1/users/{user_id}` | Update user by ID               |
| DELETE | `/api/v1/users/{user_id}` | Delete user by ID               |

### System Endpoints

| Method | Endpoint  | Description   |
| ------ | --------- | ------------- |
| GET    | `/`       | Root endpoint |
| GET    | `/health` | Health check  |

## User Model

```json
{
  "id": "string",
  "name": "string",
  "email": "string"
}
```

## Example API Usage

### Create User

```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john.doe@example.com"
     }'
```

### Get All Users

```bash
curl "http://localhost:8000/api/v1/users/?page=1&size=10"
```

### Get User by ID

```bash
curl "http://localhost:8000/api/v1/users/{user_id}"
```

### Update User

```bash
curl -X PUT "http://localhost:8000/api/v1/users/{user_id}" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Jane Doe",
       "email": "jane.doe@example.com"
     }'
```

### Delete User

```bash
curl -X DELETE "http://localhost:8000/api/v1/users/{user_id}"
```

## Development

### Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   └── database.py        # Database connection
│   ├── models/
│   │   └── user.py            # Pydantic models
│   ├── schemas/
│   │   └── user.py            # Request/Response schemas
│   ├── crud/
│   │   └── user.py            # Database operations
│   └── api/
│       ├── deps.py            # Dependencies
│       └── routes/
│           └── users.py       # API routes
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env
```

### Environment Variables

The application uses the following environment variables (configured in `.env`):

- `MONGODB_URL`: MongoDB connection string
- `DATABASE_NAME`: Database name
- `API_V1_STR`: API version prefix
- `PROJECT_NAME`: Project name
- `DEBUG`: Debug mode

### Stopping the Application

```bash
docker-compose down
```

To remove volumes (database data):

```bash
docker-compose down -v
```

## Testing

The project includes comprehensive unit and integration tests.

### Running Tests

**Important**: Tests are designed to run inside Docker containers where all dependencies are installed.

#### Using Make (Recommended)

```bash
# Run all tests
cd backend
make test

# Run unit tests only
make test-unit

# Run integration tests only
make test-integration

# Run tests with coverage report
make test-coverage
```

#### Using Docker Compose directly

```bash
# Run single test
docker compose exec api python -m pytest tests/unit/api/test_users.py::TestUsersAPI::test_create_user_invalid_email -v --asyncio-mode=auto

# Run all tests
docker compose exec api python -m pytest tests/ -v --asyncio-mode=auto

# Run unit tests only
docker compose exec api python -m pytest tests/unit/ -v --asyncio-mode=auto

# Run integration tests only
docker compose exec api python -m pytest tests/integration/ -v --asyncio-mode=auto -m integration

# Run with coverage
docker compose exec api python -m pytest tests/ --cov=app --cov-report=html --cov-report=term-missing --asyncio-mode=auto
```

#### Running Tests Locally (Optional)

If you want to run tests locally, you need to install all dependencies:

```bash
# Install all dependencies (including test and development dependencies)
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/ -v --asyncio-mode=auto
```

#### Using the test runner script

```bash
# Run all tests
python run_tests.py

# Run unit tests with coverage
python run_tests.py --type unit --coverage

# Run specific test file
python run_tests.py --file tests/unit/api/test_users.py
```

### Test Structure

```
tests/
├── conftest.py              # Test configuration and fixtures
├── test_main.py             # Main application tests
├── unit/                    # Unit tests
│   ├── api/
│   │   └── test_users.py    # API endpoint tests
│   ├── crud/
│   │   └── test_user.py     # CRUD operation tests
│   ├── models/
│   │   └── test_user.py     # Model validation tests
│   └── schemas/
│       └── test_user.py     # Schema validation tests
└── integration/             # Integration tests
    └── test_user_workflow.py # End-to-end workflow tests
```

### Test Coverage

The test suite includes:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test complete workflows and interactions
- **API Tests**: Test all CRUD endpoints with various scenarios
- **Model Tests**: Test data validation and serialization
- **Error Handling**: Test error scenarios and edge cases

Target coverage: 80%+

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database for data storage
- **Motor**: Async MongoDB driver for Python
- **Pydantic**: Data validation using Python type annotations
- **Docker**: Containerization platform
- **Uvicorn**: ASGI server for running FastAPI applications
- **Pytest**: Testing framework with async support
- **Faker**: Generate fake data for testing
- **HTTPX**: Async HTTP client for testing
