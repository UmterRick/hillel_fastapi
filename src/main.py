from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.base_settings import base_settings
from src.common.databases.postgres import postgres
from general.views import router as status_router
from src.catalogue.views import product_router
from sqladmin import Admin
from src.catalogue.admin.basket import BasketAdmin, BasketLineAdmin, OrderLineAdmin
from src.catalogue.admin.order import OrderAdmin

admin = Admin(app, engine)
admin.add_view(BasketAdmin)
admin.add_view(BasketLineAdmin)
admin.add_view(OrderLineAdmin)
admin.add_view(OrderAdmin)

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