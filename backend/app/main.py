import asyncio
import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.agent.checkpoint import close_checkpointer, init_checkpointer
from app.api.v1.router import api_router
from app.core.database import init_db
from app.engine.parser import get_converter


def create_app() -> FastAPI:
    app = FastAPI(title="Docling Audit Agent")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.on_event("startup")
    async def preload_models() -> None:
        init_db()
        if os.environ.get("SKIP_DOCLING_INIT") != "1":
            get_converter()
        await init_checkpointer()

    @app.on_event("shutdown")
    async def shutdown_services() -> None:
        await close_checkpointer()

    app.include_router(api_router, prefix="/api/v1")
    return app


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = create_app()
