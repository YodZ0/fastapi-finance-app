from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.router import apply_routes
from src.middleware import apply_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(">>> Start app")
    await init_db()
    yield
    print("<<< Dispose app")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Finance accounting",
        description="Take control of your finance!",
        lifespan=lifespan,
    )
    app = apply_middleware(app)
    app = apply_routes(app)
    return app
