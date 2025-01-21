import uuid
from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str


class UserCreateDTO(BaseModel):
    username: str
    email: str
    hashed_password: bytes


class UserReadSchema(BaseModel):
    id: uuid.UUID
    username: str
    email: str
