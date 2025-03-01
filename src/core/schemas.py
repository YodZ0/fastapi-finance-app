import uuid
from typing import Generic, TypeVar
from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class RequestSchema(BaseModel):
    """
    Request API schema.
    """

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
        )
    )


class ResponseSchema(BaseModel):
    """
    Response API schema.
    """

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=to_camel,
        )
    )


class CreateBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UpdateBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID | int


class PaginationSchema(BaseModel):
    limit: int
    offset: int


T = TypeVar("T")


class PaginationResultSchema(BaseModel, Generic[T]):
    objects: list[T]
    count: int
