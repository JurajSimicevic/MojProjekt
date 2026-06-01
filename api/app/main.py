import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.errors import AppError, app_error_handler
from app.core.logging import setup_logging
from app.routers.auth import router as auth_router
from app.routers.health import router as health_router
from app.routers.menu import router as menu_router
from app.routers.orders import router as orders_router
from app.routers.restaurants import router as restaurants_router
from app.routers.users import router as users_router

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title="Food Delivery API",
        version="0.1.0",
        description="Sustav za upravljanje dostavom hrane",
        docs_url="/docs" if settings.ENV == "dev" else None,
        redoc_url=None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(AppError, app_error_handler)

    app.include_router(health_router, prefix="/health", tags=["health"])
    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    app.include_router(restaurants_router, prefix="/restaurants", tags=["restaurants"])
    app.include_router(users_router, prefix="/users", tags=["users"])
    app.include_router(menu_router, prefix="/menu", tags=["menu"])
    app.include_router(orders_router, prefix="/orders", tags=["orders"])

    logger.info("Aplikacija kreirana (env=%s)", settings.ENV)
    return app


app = create_app()
