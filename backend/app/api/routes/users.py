from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from ...crud.user import UserCRUD
from ...schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from ..deps import get_user_crud
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    user_crud: UserCRUD = Depends(get_user_crud)
):
    """Create a new user"""
    try:
        user = await user_crud.create_user(user_data)
        return UserResponse(
            id=str(user.id),
            name=user.name,
            email=user.email
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=UserListResponse)
async def get_users(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    user_crud: UserCRUD = Depends(get_user_crud)
):
    """Get list of users with pagination"""
    try:
        skip = (page - 1) * size
        users = await user_crud.get_users(skip=skip, limit=size)
        total = await user_crud.get_users_count()
        
        user_responses = [
            UserResponse(id=str(user.id), name=user.name, email=user.email)
            for user in users
        ]
        
        return UserListResponse(
            users=user_responses,
            total=total,
            page=page,
            size=size
        )
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    user_crud: UserCRUD = Depends(get_user_crud)
):
    """Get user by ID"""
    try:
        user = await user_crud.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserResponse(
            id=str(user.id),
            name=user.name,
            email=user.email
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    user_crud: UserCRUD = Depends(get_user_crud)
):
    """Update user by ID"""
    try:
        user = await user_crud.update_user(user_id, user_data)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserResponse(
            id=str(user.id),
            name=user.name,
            email=user.email
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: str,
    user_crud: UserCRUD = Depends(get_user_crud)
):
    """Delete user by ID"""
    try:
        deleted = await user_crud.delete_user(user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
