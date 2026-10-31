from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session
from app.core.security import verify_admin_key
from app.models.project import (
    Project,
    ProjectCreate,
    ProjectRead,
    ProjectUpdate,
)

router = APIRouter(prefix="/projects", tags=["Project Showroom"])


@router.get("", response_model=List[ProjectRead])
async def list_projects(
    category: Optional[str] = Query(None, description="Filter by category (e.g. AI, Web3)"),
    featured_only: Optional[bool] = Query(None, description="Filter to only featured projects"),
    session: AsyncSession = Depends(get_session),
):
    """List all showroom projects with optional category and featured filters."""
    statement = select(Project)
    if category:
        statement = statement.where(Project.category.ilike(f"%{category}%"))
    if featured_only is not None:
        statement = statement.where(Project.is_featured == featured_only)

    statement = statement.order_by(Project.display_order.asc(), Project.id.desc())
    result = await session.exec(statement)
    return result.all()


@router.get("/{identifier}", response_model=ProjectRead)
async def get_project(identifier: str, session: AsyncSession = Depends(get_session)):
    """Get a project by numeric ID or URL slug."""
    if identifier.isdigit():
        project = await session.get(Project, int(identifier))
    else:
        statement = select(Project).where(Project.slug == identifier)
        result = await session.exec(statement)
        project = result.first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreate,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(verify_admin_key),
):
    """Create a new project in the showroom (Admin only)."""
    # Check slug uniqueness
    existing = (await session.exec(select(Project).where(Project.slug == payload.slug))).first()
    if existing:
        raise HTTPException(status_code=400, detail="A project with this slug already exists")

    project = Project.model_validate(payload)
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


@router.put("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: int,
    payload: ProjectUpdate,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(verify_admin_key),
):
    """Update a project's details (Admin only)."""
    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = payload.model_dump(exclude_unset=True)
    if "slug" in update_data and update_data["slug"] != project.slug:
        existing = (await session.exec(select(Project).where(Project.slug == update_data["slug"]))).first()
        if existing:
            raise HTTPException(status_code=400, detail="Slug already in use")

    for key, value in update_data.items():
        setattr(project, key, value)

    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(verify_admin_key),
):
    """Delete a project from the showroom (Admin only)."""
    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    await session.delete(project)
    await session.commit()
    return None
