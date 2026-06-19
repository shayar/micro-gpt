from contextlib import asynccontextmanager

from fastapi import FastAPI

from microgpt.api.auth.security import ensure_dev_user_file
from microgpt.api.config import get_settings
from microgpt.api.routers import admin, auth, chat, health, metrics
from microgpt.platform.microlake.events import event_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_dev_user_file()
    event_store.append("audit_events", {"action": "app_startup"})
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0-phase1",
        description="MicroGPT Phase 1: secure local skeleton with safety and MicroLake events.",
        lifespan=lifespan,
    )
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(chat.router)
    app.include_router(admin.router)
    app.include_router(metrics.router)
    return app


app = create_app()
