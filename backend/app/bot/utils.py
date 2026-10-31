from datetime import datetime, timezone
from typing import Optional
import discord
from sqlmodel import select
from app.core.config import settings
from app.core.database import async_session_factory
from app.models.setting import BotSetting


async def get_setting(key: str, default: str = "") -> str:
    """Helper to fetch a setting from DB with fallback to settings or default."""
    try:
        async with async_session_factory() as session:
            result = await session.exec(select(BotSetting).where(BotSetting.key == key))
            item = result.first()
            if item and item.value:
                return item.value
    except Exception:
        pass

    # Fallbacks from pydantic config
    config_fallbacks = {
        "team_name": settings.TEAM_NAME,
        "team_motto": settings.TEAM_MOTTO,
        "brand_color": settings.BRAND_COLOR,
    }
    return config_fallbacks.get(key, default)


async def get_brand_color() -> discord.Color:
    """Get the team brand color as a discord.Color object."""
    hex_color = await get_setting("brand_color", settings.BRAND_COLOR or "#5865F2")
    try:
        clean_hex = hex_color.replace("#", "")
        return discord.Color(int(clean_hex, 16))
    except Exception:
        return discord.Color.blurple()


def create_base_embed(
    title: str,
    description: Optional[str] = None,
    color: Optional[discord.Color] = None,
) -> discord.Embed:
    """Create a standardized embed following team design guidelines."""
    embed = discord.Embed(
        title=title,
        description=description,
        color=color or discord.Color.blurple(),
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_footer(text=f"{settings.TEAM_NAME} • Official Showcase", icon_url=None)
    return embed

