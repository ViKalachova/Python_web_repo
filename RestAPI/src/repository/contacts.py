from datetime import datetime, timedelta

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import or_

from src.entity.models import Contact, User
from src.schemas.contacts import ContactSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession, user: User):
    """
    The get_contacts function returns a list of contacts for the given user.
    
    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the offset of the query
    :param db: AsyncSession: Pass in a database session to the function
    :param user: User: The current user
    :return: A list of contact objects
    """
    stmt = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_all_contacts(limit: int, offset: int, db: AsyncSession):
    """
    The get_all_contacts function returns a list of all contacts in the database.
    
    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the offset of the first row to return
    :param db: AsyncSession: Pass in the database session
    :return: A list of contact objects
    """
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, user: User):
    """
    The get_contact function returns a contact by id.
    
    :param contact_id: int: The contact id what will be returned
    :param db: AsyncSession: Pass in the database session
    :param user: User: The current user
    :return: A contact object
    """
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def search_contact(contact_query: str, db: AsyncSession, user: User):
    """
    The search_contact function searches for contacts in the database.

    :param contact_query: str: The query to search for a contact.
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: The current user
    :return: A list of contact objects
    """
    stmt = select(Contact).filter_by(user=user).filter(
        or_(Contact.name.ilike(f"%{contact_query}%"), Contact.surname.ilike(f"%{contact_query}%"),
            Contact.email.ilike(f"%{contact_query}")))
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def contacts_upcoming_birthdays(db: AsyncSession, user: User):
    """
    The contacts_upcoming_birthdays function returns a list of contacts whose birthdays are within the next week.
    The function takes in an AsyncSession object and a User object as parameters, and returns a list of Contact objects.
    
    :param db: AsyncSession: Pass in the database session
    :param user: User: The current user
    :return: A list of contact objects
    """
    today = datetime.now().date()
    week_later = today + timedelta(days=7)

    stmt = select(Contact).filter_by(user=user).filter(func.date_part('month', Contact.birthday) == today.month,
                               func.date_part('day', Contact.birthday) >= today.day,
                               func.date_part('day', Contact.birthday) <= week_later.day).order_by(Contact.birthday)

    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def create_contact(body: ContactSchema, db: AsyncSession, user: User):
    """
    The create_contact function creates a new contact in the database.
    
    :param body: ContactSchema: Validate a new contact`s data sent in the request body
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: The current user
    :return: A contact object
    """
    contact = Contact(**body.model_dump(exclude_unset=True), user=user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactSchema, db: AsyncSession, user: User):
    """
    The update_contact function updates a contact in the database.
    
    :param contact_id: int: The contact id to update
    :param body: ContactSchema: Validate new data sent in the request body
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: The current user
    :return: A contact object
    """
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.description = body.description
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession, user: User):
    """
    The delete_contact function deletes a contact from the database.
    
    :param contact_id: int: The contact id to delete
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: The current user
    :return: A contact object
    """
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
