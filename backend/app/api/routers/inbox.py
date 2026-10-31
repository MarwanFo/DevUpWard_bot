from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.bot.client import bot
from app.core.database import get_session
from app.core.security import verify_admin_key
from app.models.inbox import (
    ContactSubmission,
    ContactSubmissionCreate,
    ContactSubmissionRead,
    ContactSubmissionUpdate,
)

router = APIRouter(prefix="/inbox", tags=["Visitor Inquiries"])


@router.post("", response_model=ContactSubmissionRead, status_code=status.HTTP_201_CREATED)
async def submit_inquiry(
    payload: ContactSubmissionCreate,
    session: AsyncSession = Depends(get_session),
):
    """Public endpoint for external visitors, mentors, or recruiters to get in touch."""
    submission = ContactSubmission.model_validate(payload)
    session.add(submission)
    await session.commit()
    await session.refresh(submission)

    # In-memory bridge: dispatch alert to Discord team inbox channel if bot is ready
    await bot.send_inbox_notification(submission)

    return submission


@router.get("", response_model=List[ContactSubmissionRead])
async def list_inquiries(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by unread, reviewed, archived"),
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(verify_admin_key),
):
    """List all contact submissions (Admin only)."""
    statement = select(ContactSubmission)
    if status_filter:
        statement = statement.where(ContactSubmission.status == status_filter)

    statement = statement.order_by(ContactSubmission.created_at.desc())
    result = await session.exec(statement)
    return result.all()


@router.patch("/{submission_id}/status", response_model=ContactSubmissionRead)
async def update_inquiry_status(
    submission_id: int,
    payload: ContactSubmissionUpdate,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(verify_admin_key),
):
    """Update inquiry workflow status (Admin only)."""
    submission = await session.get(ContactSubmission, submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    if payload.status:
        submission.status = payload.status

    session.add(submission)
    await session.commit()
    await session.refresh(submission)
    return submission


@router.delete("/{submission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inquiry(
    submission_id: int,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(verify_admin_key),
):
    """Delete an inquiry (Admin only)."""
    submission = await session.get(ContactSubmission, submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    await session.delete(submission)
    await session.commit()
    return None

