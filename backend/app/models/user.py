from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from typing import Optional
from bson import ObjectId


class UserModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com"
            }
        }
    )

    id: str = Field(default="", alias="_id")
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(...)

    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v


class UserUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "email": "jane.doe@example.com"
            }
        }
    )

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
