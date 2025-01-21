from typing import Annotated
from fastapi import Depends

from .services.security import SecurityServiceProtocol, SecurityServiceImpl
from .services.tokens import TokenServiceProtocol, TokenServiceImpl

from .use_cases.register import RegisterUseCaseProtocol, RegisterUseCaseImpl
from .use_cases.login import LoginUseCaseProtocol, LoginUseCaseImpl

from src.apps.users.depends import UsersService

# --- REPOSITORIES ---


# --- SERVICES ---
def get_security_service() -> SecurityServiceProtocol:
    return SecurityServiceImpl()


def get_token_service() -> TokenServiceProtocol:
    # TODO: add tokens repository
    return TokenServiceImpl()


SecurityService = Annotated[SecurityServiceProtocol, Depends(get_security_service)]
TokenService = Annotated[TokenServiceProtocol, Depends(get_token_service)]


# --- USE_CASES ---
def get_register_use_case(
    security_service: SecurityService,
    users_service: UsersService,
) -> RegisterUseCaseProtocol:
    return RegisterUseCaseImpl(
        security_service=security_service,
        users_service=users_service,
    )


def get_login_use_case(
    security_service: SecurityService,
    token_service: TokenService,
) -> LoginUseCaseProtocol:
    return LoginUseCaseImpl(
        security_service=security_service,
        token_service=token_service,
    )


RegisterUseCase = Annotated[RegisterUseCaseProtocol, Depends(get_register_use_case)]
LoginUseCase = Annotated[LoginUseCaseProtocol, Depends(get_login_use_case)]
