# User Management API

A FastAPI-based REST API for user management with full CRUD operations.

## Features

- **Create** new users
- **Read** user information (single user or list all users)
- **Update** existing users
- **Delete** users
- Email uniqueness validation
- Automatic API documentation with Swagger UI
- SQLite database with SQLAlchemy ORM
- Pydantic models for request/response validation

## Project Structure

```
app/
├── __init__.py
├── main.py              # FastAPI application entry point
├── api/
│   ├── __init__.py
│   └── users.py         # User API endpoints
├── core/
│   ├── __init__.py
│   └── config.py        # Application configuration
├── crud/
│   ├── __init__.py
│   └── user.py          # Database operations
├── db/
│   ├── __init__.py
│   └── database.py      # Database connection and session
├── models/
│   ├── __init__.py
│   └── user.py          # SQLAlchemy models
└── schemas/
    ├── __init__.py
    └── user.py          # Pydantic schemas
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

The API will be available at `http://localhost:12000`

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: `http://localhost:12000/docs`
- **ReDoc**: `http://localhost:12000/redoc`
- **OpenAPI JSON**: `http://localhost:12000/openapi.json`

## API Endpoints

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/users/` | Create a new user |
| GET | `/api/v1/users/` | Get all users (with pagination) |
| GET | `/api/v1/users/{user_id}` | Get a specific user |
| PUT | `/api/v1/users/{user_id}` | Update a user |
| DELETE | `/api/v1/users/{user_id}` | Delete a user |

### User Model

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

## Example Usage

### Create a user
```bash
curl -X POST "http://localhost:12000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "email": "john@example.com"}'
```

### Get all users
```bash
curl -X GET "http://localhost:12000/api/v1/users/"
```

### Get a specific user
```bash
curl -X GET "http://localhost:12000/api/v1/users/1"
```

### Update a user
```bash
curl -X PUT "http://localhost:12000/api/v1/users/1" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Updated", "email": "john.updated@example.com"}'
```

### Delete a user
```bash
curl -X DELETE "http://localhost:12000/api/v1/users/1"
```

## Configuration

The application can be configured using environment variables or the `.env` file:

- `APP_NAME`: Application name (default: "User Management API")
- `DEBUG`: Debug mode (default: true)
- `DATABASE_URL`: Database connection string (default: "sqlite:///./users.db")

## Best Practices Implemented

1. **Separation of Concerns**: Clear separation between API routes, business logic, and data access
2. **Dependency Injection**: Using FastAPI's dependency injection for database sessions
3. **Pydantic Models**: Strong typing and validation for request/response data
4. **Error Handling**: Proper HTTP status codes and error messages
5. **Database Abstraction**: Using SQLAlchemy ORM for database operations
6. **Configuration Management**: Centralized configuration with environment variables
7. **API Documentation**: Automatic OpenAPI/Swagger documentation
8. **CORS Support**: Configured for cross-origin requests
9. **Modular Structure**: Organized code structure following FastAPI best practices
