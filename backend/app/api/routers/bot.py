from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.bot.client import bot
from app.core.database import get_session
from app.core.security import verify_admin_key
from app.models.setting import BotSetting

router = APIRouter(prefix="/bot", tags=["Bot Controls & Telemetry"])


class PresenceUpdateRequest(BaseModel):
    status_text: str = Field(..., max_length=120)
    activity_type: str = Field(default="watching")  # playing, watching, listening, competing


class CommandSyncRequest(BaseModel):
    guild_id: Optional[int] = None


@router.get("/status")
async def get_bot_status():
    """Retrieve real-time bot connectivity, latency, and uptime."""
    return bot.get_telemetry()


@router.post("/presence")
async def update_bot_presence(
    payload: PresenceUpdateRequest,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(verify_admin_key),
):
    """Update Discord rich presence live and persist to settings (Admin only)."""
    # 1. Update live bot in memory
    await bot.set_presence(status_text=payload.status_text, activity_type=payload.activity_type)

    # 2. Persist in database
    status_setting = await session.get(BotSetting, "presence_status")
    if status_setting:
        status_setting.value = payload.status_text
    else:
        status_setting = BotSetting(key="presence_status", value=payload.status_text)
    session.add(status_setting)

    activity_setting = await session.get(BotSetting, "presence_activity_type")
    if activity_setting:
        activity_setting.value = payload.activity_type
    else:
        activity_setting = BotSetting(key="presence_activity_type", value=payload.activity_type)
    session.add(activity_setting)

    await session.commit()

    return {
        "success": True,
        "message": f"Bot presence updated to: {payload.activity_type} '{payload.status_text}'",
        "bot_online": bot.is_ready(),
    }


@router.post("/sync")
async def sync_slash_commands(
    payload: Optional[CommandSyncRequest] = None,
    _: bool = Depends(verify_admin_key),
):
    """Trigger slash command synchronization with Discord (Admin only)."""
    if not bot.is_ready():
        raise HTTPException(status_code=503, detail="Bot is not currently connected to Discord Gateway")

    guild_id = payload.guild_id if payload else None
    count = await bot.sync_app_commands(guild_id=guild_id)
    return {
        "success": True,
        "synced_count": count,
        "scope": f"guild {guild_id}" if guild_id else "global",
    }

