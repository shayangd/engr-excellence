from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional


class UserCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com"
            }
        }
    )

    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")


class UserUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "email": "jane.doe@example.com"
            }
        }
    )

    name: Optional[str] = Field(None, min_length=1, max_length=100, description="User's full name")
    email: Optional[EmailStr] = Field(None, description="User's email address")


class UserResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "name": "John Doe",
                "email": "john.doe@example.com"
            }
        }
    )

    id: str = Field(..., description="User's unique identifier")
    name: str = Field(..., description="User's full name")
    email: str = Field(..., description="User's email address")


class UserListResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "users": [
                    {
                        "id": "507f1f77bcf86cd799439011",
                        "name": "John Doe",
                        "email": "john.doe@example.com"
                    }
                ],
                "total": 1,
                "page": 1,
                "size": 10
            }
        }
    )

    users: list[UserResponse]
    total: int
    page: int
    size: int
