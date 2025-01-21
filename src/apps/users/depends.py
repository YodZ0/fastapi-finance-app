from typing import Annotated
from fastapi import Depends

from src.core.database import Session

from .repositories import UsersRepositoryProtocol, UsersRepositoryImpl
from .services import UsersServiceProtocol, UsersServiceImpl
from .use_cases.user_info import UserInfoUseCaseProtocol, UserInfoUseCaseImpl


# --- REPOSITORIES ---
def get_users_repository(session: Session) -> UsersRepositoryProtocol:
    return UsersRepositoryImpl(session=session)


UsersRepository = Annotated[UsersRepositoryProtocol, Depends(get_users_repository)]


# --- SERVICES ---
def get_users_service(users_repository: UsersRepository) -> UsersServiceProtocol:
    return UsersServiceImpl(
        users_repository=users_repository,
    )


UsersService = Annotated[UsersServiceProtocol, Depends(get_users_service)]


# --- USE_CASES ---
def get_user_info_use_case() -> UserInfoUseCaseProtocol:
    return UserInfoUseCaseImpl()


UserInfoUseCase = Annotated[UserInfoUseCaseProtocol, Depends(get_user_info_use_case)]
