from fastapi import APIRouter
from app.api.routers.team import router as team_router
from app.api.routers.projects import router as projects_router
from app.api.routers.awards import router as awards_router
from app.api.routers.stats import router as stats_router
from app.api.routers.settings import router as settings_router
from app.api.routers.bot import router as bot_router
from app.api.routers.inbox import router as inbox_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(team_router)
api_router.include_router(projects_router)
api_router.include_router(awards_router)
api_router.include_router(stats_router)
api_router.include_router(settings_router)
api_router.include_router(bot_router)
api_router.include_router(inbox_router)

__all__ = ["api_router"]

