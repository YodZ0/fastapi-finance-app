import uuid
from pydantic import BaseModel
from typing import Self, Protocol, TypeVar, Iterable, Any

from sqlalchemy import select, insert, update, delete
from sqlalchemy.sql import Select
from sqlalchemy.sql.elements import UnaryExpression
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import Base
from ..schemas import (
    CreateBaseModel,
    UpdateBaseModel,
    PaginationSchema,
    PaginationResultSchema,
)
from ..exceptions import (
    ModelNotFoundException,
    FilteringFieldNotFoundError,
    SortingFieldNotFoundError,
)


ModelType = TypeVar("ModelType", bound=Base, covariant=True)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=CreateBaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=UpdateBaseModel)


class BaseRepositoryProtocol(
    Protocol[
        ModelType,
        ReadSchemaType,
        CreateSchemaType,
        UpdateSchemaType,
    ]
):
    async def get_one(self: Self, id_: uuid.UUID | int) -> ReadSchemaType: ...

    async def get_all(self: Self) -> list[ReadSchemaType]: ...

    async def create(self: Self, create_object: CreateSchemaType) -> ReadSchemaType: ...

    async def update(self: Self, update_object: UpdateSchemaType) -> ReadSchemaType: ...

    async def delete(self: Self, id_: uuid.UUID | int) -> bool: ...

    async def query_all(
        self: Self,
        filters: dict[str, Any] = None,
        sorting: Iterable[str] = None,
        pagination: PaginationSchema = None,
    ) -> PaginationResultSchema[ReadSchemaType]: ...

    async def _filter(
        self: Self,
        statement: Select,
        filters: dict[str, Any],
    ) -> Select: ...

    async def _paginate(
        self: Self,
        statement: Select,
        pagination: PaginationSchema,
    ) -> Select: ...

    async def _sort(
        self: Self,
        statement: Select,
        sorting: Iterable[str],
    ) -> Select: ...


class BaseRepositoryImpl(
    BaseRepositoryProtocol[
        ModelType,
        ReadSchemaType,
        CreateSchemaType,
        UpdateSchemaType,
    ]
):
    model_type: type[ModelType]
    read_schema_type: type[ReadSchemaType]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_one(self: Self, id_: uuid.UUID | int) -> ReadSchemaType:
        async with self.session as s:
            statement = select(self.model_type).where(self.model_type.id == id_)
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                raise ModelNotFoundException(self.model_type, id_)
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def get_all(self: Self) -> list[ReadSchemaType]:
        async with self.session as s:
            statement = select(self.model_type)
            models = (await s.execute(statement)).scalars().all()
            return [
                self.read_schema_type.model_validate(model, from_attributes=True)
                for model in models
            ]

    async def create(self: Self, create_object: CreateSchemaType) -> ReadSchemaType:
        async with self.session as s, s.begin():
            statement = (
                insert(self.model_type)
                .values(**create_object.model_dump(exclude={"id"}))
                .returning(self.model_type)
            )
            model = (await s.execute(statement)).scalar_one()
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def update(self: Self, update_object: UpdateSchemaType) -> ReadSchemaType:
        async with self.session as s, s.begin():
            pk = update_object.id
            statement = (
                update(self.model_type)
                .where(self.model_type.id == pk)
                .values(update_object.model_dump(exclude={"id"}, exclude_unset=True))
                .returning(self.model_type)
            )
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                raise ModelNotFoundException(self.model_type, update_object.id)
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def delete(self: Self, id_: uuid.UUID | int) -> bool:
        async with self.session as s, s.begin():
            statement = delete(self.model_type).where(self.model_type.id == id_)
            await s.execute(statement)
            return True

    async def query_all(
        self: Self,
        filters: dict[str, Any] = None,
        sorting: Iterable[str] = None,
        pagination: PaginationSchema = None,
    ) -> PaginationResultSchema[ReadSchemaType]:
        async with self.session as s:
            statement = select(self.model_type)

            statement = await self._filter(statement, filters)
            statement = await self._sort(statement, sorting)
            statement = await self._paginate(statement, pagination)

            models = (await s.execute(statement)).scalars().all()
            objects = [
                self.read_schema_type.model_validate(model, from_attributes=True)
                for model in models
            ]

            count_statement = select(func.count()).select_from(statement.subquery())
            count = (await s.execute(count_statement)).scalar_one()

            return PaginationResultSchema(count=count, objects=objects)

    async def _filter(
        self: Self,
        statement: Select,
        filters: dict[str, Any],
    ) -> Select:
        if filters:
            for field, value in filters.items():
                if hasattr(self.model_type, field):
                    statement = statement.where(
                        getattr(self.model_type, field) == value
                    )
                else:
                    raise FilteringFieldNotFoundError(field)
        return statement

    async def _paginate(
        self: Self,
        statement: Select,
        pagination: PaginationSchema,
    ) -> Select:
        if pagination:
            statement = statement.limit(pagination.limit).offset(pagination.offset)
        return statement

    async def _sort(
        self: Self,
        statement: Select,
        sorting: Iterable[str],
    ) -> Select:
        if sorting:
            order_by_expr = self.get_order_by_expr(sorting)
            statement = statement.order_by(*order_by_expr)
        return statement

    def get_order_by_expr(self: Self, sorting: Iterable[str]) -> list[UnaryExpression]:
        order_by_expr: list[UnaryExpression] = []
        for st in sorting:
            try:
                if st[0] == "-":
                    order_by_expr.append(getattr(self.model_type, st[1:]).desc())
                else:
                    order_by_expr.append(getattr(self.model_type, st))
            except AttributeError as attribute_error:
                raise SortingFieldNotFoundError(st) from attribute_error
        return order_by_expr
