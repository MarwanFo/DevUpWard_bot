from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field


class AwardBase(SQLModel):
    hackathon_name: str = Field(index=True, max_length=150)
    award_title: str = Field(max_length=150)
    placement: int = Field(default=1)  # 1: 1st place, 2: 2nd place, 3: 3rd place, 0: Category/Special prize
    category: Optional[str] = Field(default=None, max_length=100)
    prize_description: Optional[str] = Field(default=None, max_length=255)
    year: int = Field(default=2026)
    project_id: Optional[int] = Field(default=None, foreign_key="projects.id")
    icon: str = Field(default="🏆", max_length=10)


class Award(AwardBase, table=True):
    __tablename__ = "awards"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AwardCreate(AwardBase):
    pass


class AwardUpdate(SQLModel):
    hackathon_name: Optional[str] = None
    award_title: Optional[str] = None
    placement: Optional[int] = None
    category: Optional[str] = None
    prize_description: Optional[str] = None
    year: Optional[int] = None
    project_id: Optional[int] = None
    icon: Optional[str] = None


class AwardRead(AwardBase):
    id: int
    created_at: datetime
