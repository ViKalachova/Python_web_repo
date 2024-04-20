from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from src.database.db import get_db
from src.entity.models import User
from src.schemas.user import UserSchema


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """
    The get_user_by_email function returns a user object from the database based on the email address provided.
    
    :param email: str: The email address of the user to be retrieved
    :param db: AsyncSession: Get the database session
    :return: A user object or none if no user is found
    """
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    """
    The create_user function creates a new user in the database.
        It takes an email, username, and password as input.
        The function then hashes the password using bcrypt and stores it in the database.
    
    :param body: UserSchema: Validate the input data
    :param db: AsyncSession: Pass the database session to the function
    :return: A user object
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print(err)

    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession):
    """
    The update_token function updates the refresh token for a user.
    
    :param user: User: Get the current user from the database
    :param token: str | None: Check if the token is a string or none
    :param db: AsyncSession: Pass the database connection to the function
    :return: None
    """
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    The confirmed_email function marks a user as confirmed in the database.
    
    :param email: str: Get the email of the user
    :param db: AsyncSession: Pass the database session to the function
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def update_avatar(email: str, url: str | None, db: AsyncSession) -> User:
    """
    The update_avatar function updates the avatar of a user.
    
    :param email: str: The email address of the user to update
    :param url: str | None: The URL to set as the new avatar for this user, or None if no change is desired
    :param db: AsyncSession: Pass in the database session
    :return: A user object
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user
