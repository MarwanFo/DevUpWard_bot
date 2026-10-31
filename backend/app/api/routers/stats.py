from collections import Counter
from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session
from app.models.award import Award
from app.models.project import Project
from app.models.team import TeamMember
from app.models.setting import BotSetting

router = APIRouter(prefix="/stats", tags=["Team Statistics"])


@router.get("", response_model=Dict[str, Any])
async def get_team_stats(session: AsyncSession = Depends(get_session)):
    """Calculate aggregated track record statistics for the team."""
    # Fetch all records
    members = (await session.exec(select(TeamMember).where(TeamMember.is_active == True))).all()  # noqa: E712
    projects = (await session.exec(select(Project))).all()
    awards = (await session.exec(select(Award))).all()

    # Unique hackathons participated in (across projects & awards)
    hackathon_names = {p.hackathon_name for p in projects} | {a.hackathon_name for a in awards}

    # First places & podium finishes
    first_places = sum(1 for a in awards if a.placement == 1)
    podium_finishes = sum(1 for a in awards if a.placement in [1, 2, 3])

    # Category distribution
    categories = Counter(p.category for p in projects)

    # Coffee stat from settings
    coffee_setting = (await session.exec(select(BotSetting).where(BotSetting.key == "coffee_cups_consumed"))).first()
    coffee_cups = int(coffee_setting.value) if coffee_setting and coffee_setting.value.isdigit() else 420

    return {
        "total_members": len(members),
        "total_projects": len(projects),
        "total_awards": len(awards),
        "total_hackathons": len(hackathon_names),
        "first_place_wins": first_places,
        "podium_finishes": podium_finishes,
        "coffee_cups_consumed": coffee_cups,
        "categories_breakdown": dict(categories),
    }

