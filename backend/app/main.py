from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import init_db
from .routers import assets, content, decisions, exports, health, instagram, projects, settings, trend_pack


def create_app() -> FastAPI:
    app = FastAPI(title="Local Creator Studio", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(projects.router)
    app.include_router(assets.router)
    app.include_router(content.router)
    app.include_router(decisions.router)
    app.include_router(exports.router)
    app.include_router(instagram.router)
    app.include_router(settings.router)
    app.include_router(trend_pack.router)

    @app.on_event("startup")
    def on_startup() -> None:
        init_db()

    return app


app = create_app()
