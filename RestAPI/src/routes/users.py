import pickle

import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, HTTPException, Depends, status, Path, Query, UploadFile, File
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.entity.models import User
from src.schemas.user import UserResponse
from src.services.auth import auth_service
from src.conf.config import config
from src.repository import users as repository_users

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
    """
    The get_current_user function is a dependency that will be injected into the
        get_current_user endpoint. It uses the auth_service to retrieve the current user,
        and returns it if found.
    
    :param user: User: Get the user object
    :return: The user object
    """
    return user


@router.patch('/avatar', response_model=UserResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: AsyncSession = Depends(get_db)):
    """
    The update_avatar_user function updates the avatar of a user.
        Args:
            file (UploadFile): The image to be uploaded.
            current_user (User): The user whose avatar is being updated.
            db (AsyncSession): An async session for database access.
    
    :param file: UploadFile: The image to be uploaded
    :param current_user: User: The user whose avatar is being updated
    :param db: AsyncSession: Connect to the database
    :return: The user object
    """
    cloudinary.config(
        cloud_name=config.CLOUDINARY_NAME,
        api_key=config.CLOUDINARY_API_KEY,
        api_secret=config.CLOUDINARY_API_SECRET,
        secure=True
    )

    public_id = f'ContactsApp/{current_user.email}'
    r = cloudinary.uploader.upload(file.file, public_id=public_id, overwrite=True)
    src_url = cloudinary.CloudinaryImage(public_id).build_url(width=250, height=250, crop='fill',
                                                              version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    auth_service.cache.set(user.email, pickle.dumps(user))
    auth_service.cache.expire(user.email, 300)
    return user
