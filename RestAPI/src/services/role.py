from fastapi import Request, Depends, HTTPException, status

from src.entity.models import Role, User
from src.services.auth import auth_service


class RoleAccess:
    def __init__(self, allowed_roles: list[Role]):
        """
        The __init__ function is called when the class is instantiated.
            It sets up the instance of the class with a list of allowed roles.
        
        :param self: Represent the instance of the class
        :param allowed_roles: list[Role]: Pass a list of role objects to the decorator
        :return: Nothing
        """
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, user: User = Depends(auth_service.get_current_user)):
        """
        The __call__ function is a decorator that checks if the user has the correct role to access this endpoint.
            If they do not, it raises an HTTPException with status code 403.
            
        
        :param self: Access the class attributes
        :param request: Request: Pass the request object to the function
        :param user: User: Get the user object from the auth_service
        :return: A function that has the same signature as the decorated function
        """
        if user.role not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")