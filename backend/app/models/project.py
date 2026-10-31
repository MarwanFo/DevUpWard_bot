from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field


class ProjectBase(SQLModel):
    title: str = Field(index=True, max_length=150)
    slug: str = Field(unique=True, index=True, max_length=150)
    tagline: str = Field(max_length=255)
    description: str = Field(max_length=2500)
    category: str = Field(default="AI", index=True, max_length=50)  # e.g., AI, Web3, FinTech, Full-Stack
    hackathon_name: str = Field(max_length=150)
    hackathon_year: int = Field(default=2026)
    awards_won: Optional[str] = Field(default=None, max_length=255)
    demo_url: Optional[str] = Field(default=None, max_length=500)
    repo_url: Optional[str] = Field(default=None, max_length=500)
    devpost_url: Optional[str] = Field(default=None, max_length=500)
    banner_url: Optional[str] = Field(default=None, max_length=500)
    is_featured: bool = Field(default=False)
    display_order: int = Field(default=0)


class Project(ProjectBase, table=True):
    __tablename__ = "projects"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(SQLModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    tagline: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    hackathon_name: Optional[str] = None
    hackathon_year: Optional[int] = None
    awards_won: Optional[str] = None
    demo_url: Optional[str] = None
    repo_url: Optional[str] = None
    devpost_url: Optional[str] = None
    banner_url: Optional[str] = None
    is_featured: Optional[bool] = None
    display_order: Optional[int] = None


class ProjectRead(ProjectBase):
    id: int
    created_at: datetime

