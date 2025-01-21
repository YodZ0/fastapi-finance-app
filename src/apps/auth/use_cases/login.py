from typing import Protocol

from ..services.security import SecurityServiceProtocol
from ..services.tokens import TokenServiceProtocol


class LoginUseCaseProtocol(Protocol): ...


class LoginUseCaseImpl:
    def __init__(
        self,
        security_service: SecurityServiceProtocol,
        token_service: TokenServiceProtocol,
    ):
        self.security_service = security_service
        self.token_service = token_service

    async def __call__(self, *args, **kwargs): ...
