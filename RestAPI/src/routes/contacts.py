from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.entity.models import User, Role
from src.repository import contacts as repositories_contacts
from src.schemas.contacts import ContactSchema, ContactResponse
from src.services.auth import auth_service
from src.services.role import RoleAccess

router = APIRouter(prefix="/contacts", tags=["contacts"])
access_to_route_all = RoleAccess([Role.admin])


@router.get("/", response_model=list[ContactResponse], dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                       db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function returns a list of contacts for the current user.
        The limit and offset parameters are used to paginate the results.
    
    
    :param limit: int: Limit the number of contacts returned
    :param ge: Specify the minimum value that limit can have
    :param le: Limit the maximum number of contacts that can be returned
    :param offset: int: Skip a certain number of contacts
    :param ge: Set a minimum value for the limit parameter
    :param db: AsyncSession: Pass the database session to the repository layer
    :param user: User: Get the current user
    :return: A list of contacts
    """
    contacts = await repositories_contacts.get_contacts(limit, offset, db, user)
    return contacts


@router.get("/all", response_model=list[ContactResponse], dependencies=[Depends(access_to_route_all)])
async def get_all_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                           db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    """
    The get_all_contacts function returns a list of contacts.
        The limit and offset parameters are used to paginate the results.
        
    
    :param limit: int: Limit the number of contacts returned by the function
    :param ge: Set a minimum value for the limit parameter
    :param le: Limit the maximum number of contacts returned
    :param offset: int: Set the offset of the query
    :param ge: Specify the minimum value of the limit parameter
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Get the current user from the auth_service
    :return: A list of contacts
    """
    contacts = await repositories_contacts.get_all_contacts(limit, offset, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db),
                      user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function returns a contact by id.
        If the user is not logged in, an HTTP 401 Unauthorized error will be returned.
        If the contact does not exist, an HTTP 404 Not Found error will be returned.
    
    :param contact_id: int: Get the contact id from the url
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Get the current user from the auth_service
    :return: A contact object
    """
    contact = await repositories_contacts.get_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/search/{contact_query}", response_model=list[ContactResponse],
            dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def search_contacts(contact_query: str = Path(..., min_length=3), db: AsyncSession = Depends(get_db),
                          user: User = Depends(auth_service.get_current_user)):
    """
    The search_contacts function searches contacts by contact_query in the database.
    
    :param contact_query: str: The search query to use when searching for contacts
    :param min_length: Ensure that the contact_query string is at least 3 characters long
    :param db: AsyncSession: Get the database session from the dependency injection
    :param user: User: Get the current user from the database
    :return: A list of contacts
    """
    return await repositories_contacts.search_contact(contact_query, db, user)


@router.get("/search/upcoming_birthdays/", response_model=list[ContactResponse],
            dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def search_upcoming_birthdays(db: AsyncSession = Depends(get_db),
                                    user: User = Depends(auth_service.get_current_user)):
    """
    The search_upcoming_birthdays function searches for contacts with upcoming birthdays.
        
    
    :param db: AsyncSession: Pass in the database session
    :param user: User: Get the current user from the database
    :return: A list of contacts with upcoming birthdays
    """
    return await repositories_contacts.contacts_upcoming_birthdays(db, user)


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.
        The function takes in a ContactSchema object, which is validated by pydantic.
        If the validation fails, an error will be thrown and caught by FastAPI's exception handler.
        If it passes validation, then we create a new contact using our repository layer.
    
    :param body: ContactSchema: Validate the request body against the contactschema schema
    :param db: AsyncSession: Pass the database session to the repository layer
    :param user: User: Get the current user from the database
    :return: A contactschema object
    """
    contact = await repositories_contacts.create_contact(body, db, user)
    return contact


@router.put("/{contact_id}")
async def update_contact(body: ContactSchema, contact_id: int, db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
    
    :param body: ContactSchema: A ContactSchema object containing the new values for the contact
    :param contact_id: int: Get the contact id from the url
    :param db: AsyncSession: Pass the database session to the repository
    :param user: User: Get the current user from the database
    :return: A contact object
    """
    contact = await repositories_contacts.update_contact(contact_id, body, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    """
    The delete_contact function deletes a contact from the database.
    
    :param contact_id: int: The id of the contact to delete
    :param db: AsyncSession: Pass the database session to the repository
    :param user: User: Get the current user from the database
    :return: A contact object
    """
    contact = await repositories_contacts.delete_contact(contact_id, db, user)
    return contact
