from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field


class TeamQuoteBase(SQLModel):
    quote: str = Field(max_length=500)
    author: str = Field(max_length=100)
    context: Optional[str] = Field(default=None, max_length=255)  # e.g., "3 AM at HackMIT"


class TeamQuote(TeamQuoteBase, table=True):
    __tablename__ = "team_quotes"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TeamQuoteCreate(TeamQuoteBase):
    pass


class TeamQuoteRead(TeamQuoteBase):
    id: int
    created_at: datetime
