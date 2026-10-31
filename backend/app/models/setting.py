from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field


class BotSetting(SQLModel, table=True):
    __tablename__ = "bot_settings"

    key: str = Field(primary_key=True, max_length=100)
    value: str = Field(max_length=2000)
    description: Optional[str] = Field(default=None, max_length=255)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)}
    )


class BotSettingUpdate(SQLModel):
    value: str
    description: Optional[str] = None


class BotSettingRead(SQLModel):
    key: str
    value: str
    description: Optional[str] = None
    updated_at: datetime
