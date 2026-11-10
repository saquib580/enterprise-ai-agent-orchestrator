"""FastAPI application factory and operational endpoints."""

import logging
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.agents import router as agents_router
from app.core.config import get_settings
from app.db.session import dispose_engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Initialize logging and release database resources on shutdown."""
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    logger.info("Starting %s", settings.app_name)
    try:
        yield
    finally:
        await dispose_engine()
        logger.info("Stopped %s", settings.app_name)


def create_app() -> FastAPI:
    """Build the configured FastAPI application."""
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        description="Multi-tenant enterprise AI agent orchestration foundation.",
        version="0.1.0",
        debug=settings.debug,
        lifespan=lifespan,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type", "X-Tenant-ID"],
        expose_headers=["X-Process-Time"],
    )

    @application.middleware("http")
    async def process_time_middleware(request: Request, call_next: Any) -> Any:
        """Attach processing duration to HTTP responses."""
        started = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Process-Time"] = f"{time.perf_counter() - started:.6f}"
        return response

    @application.get("/health", tags=["Operations"])
    async def health() -> dict[str, str]:
        """Report process liveness, not database readiness."""
        return {
            "status": "healthy",
            "application": settings.app_name,
            "environment": settings.app_env,
        }

    application.include_router(agents_router, prefix=settings.api_v1_prefix)
    return application


app = create_app()
