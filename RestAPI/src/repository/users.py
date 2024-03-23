from datetime import datetime, timedelta

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import or_

from src.entity.models import User
from src.schemas.user import UserSchema


async def get_users(limit: int, offset: int, db: AsyncSession):
    stmt = select(User).offset(offset).limit(limit)
    users = await db.execute(stmt)
    return users.scalars().all()


async def get_user(user_id: int, db: AsyncSession):
    stmt = select(User).filter_by(id=user_id)
    user = await db.execute(stmt)
    return user.scalar_one_or_none()


async def search_user(user_query: str, db: AsyncSession):
    stmt = select(User).filter(
        or_(User.name.ilike(f"%{user_query}%"), User.surname.ilike(f"%{user_query}%"),
            User.email.ilike(f"%{user_query}")))
    users = await db.execute(stmt)
    return users.scalars().all()


async def users_upcoming_birthdays(db: AsyncSession):
    today = datetime.now().date()
    week_later = today + timedelta(days=7)

    stmt = select(User).filter(func.date_part('month', User.birthday) == today.month,
                               func.date_part('day', User.birthday) >= today.day,
                               func.date_part('day', User.birthday) <= week_later.day).order_by(User.birthday)

    users = await db.execute(stmt)
    return users.scalars().all()


async def create_user(body: UserSchema, db: AsyncSession):
    user = User(**body.model_dump(exclude_unset=True))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(user_id: int, body: UserSchema, db: AsyncSession):
    stmt = select(User).filter_by(id=user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        user.name = body.name
        user.surname = body.surname
        user.email = body.email
        user.phone = body.phone
        user.birthday = body.birthday
        user.description = body.description
        await db.commit()
        await db.refresh(user)
    return user


async def delete_user(user_id: int, db: AsyncSession):
    stmt = select(User).filter_by(id=user_id)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    if user:
        await db.delete(user)
        await db.commit()
    return user
