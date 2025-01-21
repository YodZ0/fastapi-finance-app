from typing import Protocol

from src.apps.users.services import UsersServiceProtocol
from src.apps.users.schemas import UserCreateSchema, UserCreateDTO

from ..services.security import SecurityServiceProtocol


class RegisterUseCaseProtocol(Protocol):

    async def __call__(self, new_user: UserCreateSchema): ...


class RegisterUseCaseImpl:
    def __init__(
        self,
        security_service: SecurityServiceProtocol,
        users_service: UsersServiceProtocol,
    ):
        self.security_service = security_service
        self.users_service = users_service

    async def __call__(self, new_user: UserCreateSchema):
        hashed_password = await self.security_service.encode_password(new_user.password)
        new_user_data = UserCreateDTO(
            username=new_user.username,
            email=new_user.email,
            hashed_password=hashed_password,
        )
        new_user_id = await self.users_service.create_user(new_user_data)
        return new_user_id
