import bcrypt
from typing import Protocol


class SecurityServiceProtocol(Protocol):

    async def encode_password(self, password: str) -> bytes: ...

    async def validate_password(
        self,
        password: str,
        hashed_password: bytes,
    ) -> bool: ...


class SecurityServiceImpl:

    async def encode_password(self, password: str) -> bytes:
        """
        Hash password from string.
        """
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        return bcrypt.hashpw(password=pwd_bytes, salt=salt)

    async def validate_password(self, password: str, hashed_password: bytes) -> bool:
        """
        Compare hashed_password with password from input.
        """
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )
