from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session
from app.core.security import verify_admin_key
from app.models.award import (
    Award,
    AwardCreate,
    AwardRead,
    AwardUpdate,
)

router = APIRouter(prefix="/awards", tags=["Awards & Hall of Fame"])


@router.get("", response_model=List[AwardRead])
async def list_awards(session: AsyncSession = Depends(get_session)):
    """Get all hackathon awards ordered chronologically by year desc."""
    statement = select(Award).order_by(Award.year.desc(), Award.id.desc())
    result = await session.exec(statement)
    return result.all()


@router.get("/{award_id}", response_model=AwardRead)
async def get_award(award_id: int, session: AsyncSession = Depends(get_session)):
    """Get an award by ID."""
    award = await session.get(Award, award_id)
    if not award:
        raise HTTPException(status_code=404, detail="Award not found")
    return award


@router.post("", response_model=AwardRead, status_code=status.HTTP_201_CREATED)
async def create_award(
    payload: AwardCreate,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(verify_admin_key),
):
    """Record a new hackathon award or prize (Admin only)."""
    award = Award.model_validate(payload)
    session.add(award)
    await session.commit()
    await session.refresh(award)
    return award


@router.put("/{award_id}", response_model=AwardRead)
async def update_award(
    award_id: int,
    payload: AwardUpdate,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(verify_admin_key),
):
    """Update an award entry (Admin only)."""
    award = await session.get(Award, award_id)
    if not award:
        raise HTTPException(status_code=404, detail="Award not found")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(award, key, value)

    session.add(award)
    await session.commit()
    await session.refresh(award)
    return award


@router.delete("/{award_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_award(
    award_id: int,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(verify_admin_key),
):
    """Delete an award entry (Admin only)."""
    award = await session.get(Award, award_id)
    if not award:
        raise HTTPException(status_code=404, detail="Award not found")

    await session.delete(award)
    await session.commit()
    return None
