from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session
from app.core.security import verify_admin_key
from app.models.setting import BotSetting, BotSettingRead, BotSettingUpdate

router = APIRouter(prefix="/settings", tags=["Bot & Team Settings"])


@router.get("", response_model=List[BotSettingRead])
async def list_settings(session: AsyncSession = Depends(get_session)):
    """List all bot and team configuration settings."""
    result = await session.exec(select(BotSetting))
    return result.all()


@router.get("/dict", response_model=Dict[str, str])
async def get_settings_dict(session: AsyncSession = Depends(get_session)):
    """Get all settings as a flat key-value dictionary for easy frontend access."""
    result = await session.exec(select(BotSetting))
    return {s.key: s.value for s in result.all()}


@router.put("/{key}", response_model=BotSettingRead)
async def update_setting(
    key: str,
    payload: BotSettingUpdate,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(verify_admin_key),
):
    """Update a specific configuration setting (Admin only)."""
    setting = await session.get(BotSetting, key)
    if not setting:
        # Create if doesn't exist
        setting = BotSetting(key=key, value=payload.value, description=payload.description)
    else:
        setting.value = payload.value
        if payload.description is not None:
            setting.description = payload.description

    session.add(setting)
    await session.commit()
    await session.refresh(setting)
    return setting
