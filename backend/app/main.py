import asyncio
from contextlib import asynccontextmanager
import logging
import os
import sys

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import api_router
from app.bot.client import bot
from app.core.config import settings
from app.core.database import engine, init_db

logger = logging.getLogger("main")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

bot_task: asyncio.Task = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global bot_task
    logger.info("🚀 Starting up DevUpward Showcase API & Bot Engine...")

    # 1. Initialize DB tables
    await init_db()
    logger.info("💾 Database verified.")

    # 2. Launch Discord Bot in background task if token is set
    token = settings.DISCORD_BOT_TOKEN
    placeholder_tokens = ["", "your_bot_token_here", "your_discord_bot_token"]

    if token and token not in placeholder_tokens:
        logger.info("🤖 Starting Discord Bot background worker...")
        bot_task = asyncio.create_task(bot.start(token))
    else:
        logger.warning("⚠️ DISCORD_BOT_TOKEN is not configured or using placeholder. Running in API-only mode.")

    yield

    # Shutdown sequence
    logger.info("🛑 Shutting down DevUpward Showcase application...")
    if bot and not bot.is_closed():
        await bot.close()
    if bot_task and not bot_task.done():
        bot_task.cancel()
    await engine.dispose()
    logger.info("👋 Shutdown complete.")


app = FastAPI(
    title="DevUpward Showcase Bot & Dashboard API",
    version="1.0.0",
    description="Unified backend REST API and Discord Bot engine for the DevUpward hackathon team.",
    lifespan=lifespan,
)

# Enable CORS for frontend dashboard (both localhost:3000 and production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API v1 router
app.include_router(api_router)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint exposing API and Bot status."""
    return {
        "status": "healthy",
        "service": "DevUpward API",
        "version": "1.0.0",
        "bot_telemetry": bot.get_telemetry(),
    }


# Serve React SPA in production if built
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/dist"))
if os.path.exists(frontend_dist):
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        # Exclude API endpoints, docs, and health from catch-all
        if full_path.startswith(("api", "health", "docs", "openapi.json")):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Not Found")

        index_file = os.path.join(frontend_dist, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Frontend build index.html not found")



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=False,
    )

