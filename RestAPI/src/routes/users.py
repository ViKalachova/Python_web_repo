from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import users as repositories_users
from src.schemas.user import UserSchema, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
async def get_users(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                    db: AsyncSession = Depends(get_db)):
    users = await repositories_users.get_users(limit, offset, db)
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await repositories_users.get_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/search/{user_query}", response_model=list[UserResponse])
async def search_users(user_query: str = Path(..., min_length=3), db: AsyncSession = Depends(get_db)):
    return await repositories_users.search_user(user_query, db)


@router.get("/search/upcoming_birthdays/", response_model=list[UserResponse])
async def search_upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    return await repositories_users.users_upcoming_birthdays(db)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    user = await repositories_users.create_user(body, db)
    return user


@router.put("/{user_id}")
async def update_user(body: UserSchema, user_id: int, db: AsyncSession = Depends(get_db)):
    user = await repositories_users.update_user(user_id, body, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await repositories_users.delete_user(user_id, db)
    return user
