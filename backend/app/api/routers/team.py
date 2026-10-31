from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session
from app.core.security import verify_admin_key
from app.models.team import (
    TeamMember,
    TeamMemberCreate,
    TeamMemberRead,
    TeamMemberUpdate,
)

router = APIRouter(prefix="/team", tags=["Team Roster"])


@router.get("", response_model=List[TeamMemberRead])
async def list_team_members(session: AsyncSession = Depends(get_session)):
    """Get all team members ordered by display_order."""
    statement = select(TeamMember).order_by(TeamMember.display_order.asc(), TeamMember.id.asc())
    result = await session.exec(statement)
    return result.all()


@router.get("/{member_id}", response_model=TeamMemberRead)
async def get_team_member(member_id: int, session: AsyncSession = Depends(get_session)):
    """Get a specific team member by ID."""
    member = await session.get(TeamMember, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Team member not found")
    return member


@router.post("", response_model=TeamMemberRead, status_code=status.HTTP_201_CREATED)
async def create_team_member(
    payload: TeamMemberCreate,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(verify_admin_key),
):
    """Create a new team member (Admin only)."""
    member = TeamMember.model_validate(payload)
    session.add(member)
    await session.commit()
    await session.refresh(member)
    return member


@router.put("/{member_id}", response_model=TeamMemberRead)
async def update_team_member(
    member_id: int,
    payload: TeamMemberUpdate,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(verify_admin_key),
):
    """Update a team member's profile (Admin only)."""
    member = await session.get(TeamMember, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Team member not found")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(member, key, value)

    session.add(member)
    await session.commit()
    await session.refresh(member)
    return member


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team_member(
    member_id: int,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(verify_admin_key),
):
    """Delete a team member (Admin only)."""
    member = await session.get(TeamMember, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Team member not found")

    await session.delete(member)
    await session.commit()
    return None

