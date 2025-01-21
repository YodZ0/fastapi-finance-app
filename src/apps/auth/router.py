from fastapi import APIRouter

from src.apps.users.schemas import UserCreateSchema
from .depends import RegisterUseCase, LoginUseCase

__all__ = ("router",)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register")
async def register(
    new_user: UserCreateSchema,
    uc: RegisterUseCase,
):
    new_user_id = await uc(new_user)
    return {"msg": "success", "id": new_user_id}


@router.post("/login")
async def login(uc: LoginUseCase):
    return {"msg": "login"}


@router.post("/logout")
async def logout():
    return {"msg": "logout"}


@router.post("/refresh")
async def refresh():
    return {"msg": "refresh"}
