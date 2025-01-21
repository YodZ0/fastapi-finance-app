import uuid
from typing import Protocol

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User
from ..schemas import UserCreateDTO


class UsersRepositoryProtocol(Protocol):
    async def create(self, user_data: UserCreateDTO): ...

    async def get(self, user_id: uuid.UUID): ...

    async def upd(self, user_id: uuid.UUID, new_values: dict): ...

    async def delete(self, user_id: uuid.UUID) -> None: ...


class UsersRepositoryImpl:
    model = User

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_data: UserCreateDTO):
        async with self.session as s:
            stmt = (
                insert(self.model)
                .values(**user_data.model_dump())
                .returning(self.model.id)
            )
            res = await s.execute(stmt)
            await s.commit()
            return res.scalar()

    async def get(self, user_id: uuid.UUID):
        async with self.session as s:
            query = select(self.model).filter_by(id=user_id)
            res = await s.execute(query)
            return res.scalar()

    async def upd(self, user_id: uuid.UUID, new_values: dict):
        async with self.session as s:
            stmt = update(self.model).filter_by(id=user_id).values(**new_values)
            res = await s.execute(stmt)
            await s.commit()
            return res.scalar()

    async def delete(self, user_id: uuid.UUID) -> None:
        async with self.session as s:
            stmt = delete(self.model).filter_by(id=user_id)
            await s.execute(stmt)
            await s.commit()
