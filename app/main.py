from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.database import engine
from app.models import user
from app.api.users import router as users_router

# Create database tables
user.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])


@app.get("/")
def read_root():
    return {"message": "Welcome to User Management API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}