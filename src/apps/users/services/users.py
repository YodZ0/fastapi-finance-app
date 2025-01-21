import uuid
from typing import Protocol

from ..repositories import UsersRepositoryProtocol
from ..schemas import UserCreateDTO


class UsersServiceProtocol(Protocol):
    async def create_user(self, new_user_data: UserCreateDTO) -> uuid.UUID: ...


class UsersServiceImpl:
    def __init__(self, users_repository: UsersRepositoryProtocol):
        self.users_repository = users_repository

    async def create_user(self, new_user_data: UserCreateDTO) -> uuid.UUID:
        new_user_id = await self.users_repository.create(new_user_data)
        return new_user_id
