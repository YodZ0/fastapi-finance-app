from fastapi import FastAPI
from src.apps.healthcheck.router import router as healthcheck_router
from src.apps.users.router import router as users_router


def apply_routes(app: FastAPI) -> FastAPI:
    app.include_router(healthcheck_router)
    app.include_router(users_router)
    return app
