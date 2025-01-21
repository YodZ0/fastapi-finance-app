from fastapi import APIRouter


__all__ = ("router",)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me")
async def me():
    return {"msg": "me"}
