from typing import Protocol


class UserInfoUseCaseProtocol(Protocol):
    async def __call__(self, *args, **kwargs): ...


class UserInfoUseCaseImpl:
    def __init__(self):
        pass

    async def __call__(self, *args, **kwargs): ...
