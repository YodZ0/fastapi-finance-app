from typing import Protocol

from ..schemas.tokens import AccessToken, RefreshToken


class TokenServiceProtocol(Protocol):

    def create_access_token(self, *args, **kwargs) -> AccessToken: ...

    def create_refresh_token(self, *args, **kwargs) -> RefreshToken: ...


class TokenServiceImpl:
    def __init__(self): ...

    def create_access_token(self, *args, **kwargs) -> AccessToken: ...

    def create_refresh_token(self, *args, **kwargs) -> RefreshToken: ...
