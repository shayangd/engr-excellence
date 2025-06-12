# Engineering Excellence

### Open Hands: (openhands-fastapi)

Prompt 1
> create basic fast api project following all best practice. The project contains 4 crud apis of user. User model contain name id and email only.

### Augment Code: (dev)

Prompt 1:
> create folder named backend inside which create basic fast api project following all best practice. The project contains 4 crud apis of user. User model contain name id and email only. Use Mongo Db as database. use docker to do complete setup. i will only need to run 1 command docker compose up to run the project

Prompt 2:
> write unit tests for fast api


========================
========================
========================

A full-stack user management application with FastAPI backend and Next.js frontend, featuring complete CRUD operations and Docker containerization.

## 🚀 Features

### Backend (FastAPI)

- ✅ **RESTful API**: Complete CRUD operations for user management
- ✅ **MongoDB Integration**: Async MongoDB operations with Motor
- ✅ **Data Validation**: Pydantic models for request/response validation
- ✅ **API Documentation**: Auto-generated OpenAPI/Swagger docs
- ✅ **Error Handling**: Comprehensive error handling and logging
- ✅ **Pagination**: Built-in pagination for user listings
- ✅ **Email Validation**: Email format validation and uniqueness
- ✅ **Database Indexing**: Optimized database queries

### Frontend (Next.js)

- ✅ **Modern UI**: Built with Next.js 14 and Tailwind CSS
- ✅ **TypeScript**: Full type safety throughout the application
- ✅ **User CRUD**: Create, Read, Update, Delete users
- ✅ **Form Validation**: Client-side validation with Zod
- ✅ **API Integration**: Seamless integration with FastAPI backend
- ✅ **Responsive Design**: Mobile-first responsive design
- ✅ **Error Handling**: Comprehensive error handling and user feedback
- ✅ **Loading States**: Better UX with loading indicators
- ✅ **Pagination**: Built-in pagination for user listings

### DevOps

- ✅ **Docker Support**: Complete containerization with Docker Compose
- ✅ **Multi-service Setup**: Backend, Frontend, Database, and Admin UI
- ✅ **Health Checks**: Container health monitoring
- ✅ **Volume Persistence**: Data persistence for MongoDB

## 🛠️ Tech Stack

### Backend

- **FastAPI** - Modern, fast web framework for building APIs
- **MongoDB** - NoSQL database with Motor async driver
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - ASGI server implementation

### Frontend

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS framework
- **React Hook Form** - Form handling
- **Zod** - Schema validation
- **TanStack Query** - Data fetching and caching
- **Axios** - HTTP client

### Infrastructure

- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **MongoDB** - Database
- **Mongo Express** - Database administration UI

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. Clone the repository:

```bash
git clone <repository-url>
cd engr-excellence
```

2. Start all services:

```bash
docker-compose up --build
```

3. Access the applications:
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/api/v1/docs
   - **MongoDB Admin**: http://localhost:8081 (admin/admin123)

### Local Development

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
engr-excellence/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # API routes and dependencies
│   │   ├── core/              # Core configuration
│   │   ├── crud/              # Database operations
│   │   ├── models/            # Pydantic models
│   │   ├── schemas/           # Request/Response schemas
│   │   └── main.py            # FastAPI application
│   ├── tests/                 # Backend tests
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
├── frontend/                   # Next.js frontend
│   ├── src/
│   │   ├── app/               # Next.js App Router
│   │   ├── components/        # React components
│   │   ├── lib/               # Utilities and API client
│   │   └── types/             # TypeScript types
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml          # Complete stack orchestration
└── README.md
```

## 🔧 API Endpoints

### Users

- `GET /api/v1/users` - List users with pagination
- `POST /api/v1/users` - Create new user
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

### System

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/v1/docs` - API documentation

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Type Checking

```bash
cd frontend
npm run type-check
npm run lint
```

## 🐳 Docker Services

| Service       | Port  | Description                  |
| ------------- | ----- | ---------------------------- |
| frontend      | 3000  | Next.js frontend application |
| backend       | 8000  | FastAPI backend API          |
| mongo         | 27017 | MongoDB database             |
| mongo-express | 8081  | MongoDB administration UI    |

## 🔒 Environment Variables

### Backend (.env)

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=fastapi_db
DEBUG=True
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📝 Usage Examples

### Create a User

```bash
curl -X POST "http://localhost:8000/api/v1/users" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "email": "john@example.com"}'
```

### Get Users

```bash
curl "http://localhost:8000/api/v1/users?page=1&size=10"
```

### Update a User

```bash
curl -X PUT "http://localhost:8000/api/v1/users/{user_id}" \
     -H "Content-Type: application/json" \
     -d '{"name": "Jane Doe", "email": "jane@example.com"}'
```

### Delete a User

```bash
curl -X DELETE "http://localhost:8000/api/v1/users/{user_id}"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
