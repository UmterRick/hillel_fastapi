from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from sqladmin import Admin
from sqlalchemy import create_engine

from src.base_settings import base_settings
from src.common.databases.postgres import postgres
from src.general.views import router as status_router
from src.catalogue.views import product_router
from src.admin import register_admin_views


sync_engine = create_engine(
    url=base_settings.postgres.sync_url,
    echo=True,
)


def include_routers(application: FastAPI) -> None:
    application.include_router(router=status_router)
    application.include_router(
        router=product_router,
        prefix="/catalogue",
        tags=["Catalogue"],
    )


def include_admin(application: FastAPI) -> None:
    admin = Admin(app=application, engine=sync_engine)
    register_admin_views(admin)


@asynccontextmanager
async def lifespan(application: FastAPI):
    postgres.connect(base_settings.postgres.url)  # async engine
    include_routers(application)
    include_admin(application)
    yield
    await postgres.disconnect()


def get_application() -> FastAPI:
    application = FastAPI(
        debug=True,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    return application


app = get_application()


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
