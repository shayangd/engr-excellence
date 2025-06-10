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

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/users/` | Create a new user |
| GET | `/api/v1/users/` | Get all users (with pagination) |
| GET | `/api/v1/users/{user_id}` | Get user by ID |
| PUT | `/api/v1/users/{user_id}` | Update user by ID |
| DELETE | `/api/v1/users/{user_id}` | Delete user by ID |

### System Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |

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

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database for data storage
- **Motor**: Async MongoDB driver for Python
- **Pydantic**: Data validation using Python type annotations
- **Docker**: Containerization platform
- **Uvicorn**: ASGI server for running FastAPI applications
