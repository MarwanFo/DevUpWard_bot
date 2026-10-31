from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field


class TeamMemberBase(SQLModel):
    name: str = Field(index=True, max_length=100)
    role: str = Field(max_length=100)  # e.g., "Full-Stack Architect", "AI Engineer"
    bio: str = Field(max_length=1000)
    avatar_url: Optional[str] = Field(default=None, max_length=500)
    discord_id: Optional[str] = Field(default=None, max_length=32)
    skills: str = Field(default="[]")  # JSON encoded list of strings, e.g. ["Python", "PyTorch"]
    github_url: Optional[str] = Field(default=None, max_length=300)
    linkedin_url: Optional[str] = Field(default=None, max_length=300)
    portfolio_url: Optional[str] = Field(default=None, max_length=300)
    display_order: int = Field(default=0)
    is_active: bool = Field(default=True)


class TeamMember(TeamMemberBase, table=True):
    __tablename__ = "team_members"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TeamMemberCreate(TeamMemberBase):
    pass


class TeamMemberUpdate(SQLModel):
    name: Optional[str] = None
    role: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    discord_id: Optional[str] = None
    skills: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


class TeamMemberRead(TeamMemberBase):
    id: int
    created_at: datetime
