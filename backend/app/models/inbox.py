from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field


class ContactSubmissionBase(SQLModel):
    sender_name: str = Field(max_length=120)
    email: Optional[str] = Field(default=None, max_length=150)
    organization: Optional[str] = Field(default=None, max_length=150)
    discord_tag: Optional[str] = Field(default=None, max_length=100)
    message: str = Field(max_length=2000)
    status: str = Field(default="unread", max_length=30)  # "unread", "reviewed", "archived"


class ContactSubmission(ContactSubmissionBase, table=True):
    __tablename__ = "contact_submissions"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ContactSubmissionCreate(ContactSubmissionBase):
    pass


class ContactSubmissionUpdate(SQLModel):
    status: Optional[str] = None


class ContactSubmissionRead(ContactSubmissionBase):
    id: int
    created_at: datetime
