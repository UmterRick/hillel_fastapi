from contextlib import asynccontextmanager
from sys import prefix

import uvicorn
from fastapi import FastAPI

from src.base_settings import base_settings
from src.common.databases.postgres import postgres
from general.views import router as status_router
from src.catalogue.views import product_router
from src.authentication.views import router as auth_router
from src.users.views import router as users_router

@asynccontextmanager
async def lifespan(application: FastAPI):
    postgres.connect(base_settings.postgres.url)
    include_routers(application)
    yield
    await postgres.disconnect()


def include_routers(application: FastAPI) -> None:
    application.include_router(router=status_router)
    application.include_router(
        router=product_router,
        prefix="/catalogue",
        tags=['Catalogue'],
    )
    application.include_router(
        router=users_router,
        prefix="/account",
        tags=["Account"]
    )
    application.include_router(
        router=auth_router,
        prefix="/auth",
        tags=["Authentication"]
    )

def get_application():
    application = FastAPI(
        debug=True,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="localhost",
        port=5000,
        # reload=True,
    )