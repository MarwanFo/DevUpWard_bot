import asyncio
import json
import os
import sys

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

# Set UTF-8 encoding for Windows terminals
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from sqlmodel import select
from app.core.database import async_session_factory, init_db
from app.models import (
    Award,
    BotSetting,
    Project,
    TeamMember,
    TeamQuote,
)


async def export_data(filepath: str = "portfolio_backup.json"):
    """Export all showcase data into a standalone JSON file."""
    print(f"📦 Exporting portfolio data to '{filepath}'...")
    await init_db()

    async with async_session_factory() as session:
        members = (await session.exec(select(TeamMember))).all()
        projects = (await session.exec(select(Project))).all()
        awards = (await session.exec(select(Award))).all()
        settings = (await session.exec(select(BotSetting))).all()
        quotes = (await session.exec(select(TeamQuote))).all()

        backup = {
            "version": "1.0",
            "members": [m.model_dump(mode="json") for m in members],
            "projects": [p.model_dump(mode="json") for p in projects],
            "awards": [a.model_dump(mode="json") for a in awards],
            "settings": [s.model_dump(mode="json") for s in settings],
            "quotes": [q.model_dump(mode="json") for q in quotes],
        }

    parent_dir = os.path.dirname(filepath)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(backup, f, indent=2, ensure_ascii=False)


    print(f"✅ Export completed! {len(members)} members, {len(projects)} projects, {len(awards)} awards saved.")


async def import_data(filepath: str = "portfolio_backup.json"):
    """Restore portfolio data from a JSON backup file."""
    if not os.path.exists(filepath):
        print(f"❌ Backup file '{filepath}' does not exist.")
        return

    print(f"📥 Importing portfolio data from '{filepath}'...")
    await init_db()

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    async with async_session_factory() as session:
        # Import members
        for m_data in data.get("members", []):
            m_data.pop("id", None)
            m_data.pop("created_at", None)
            session.add(TeamMember(**m_data))

        # Import projects
        project_map = {}
        for p_data in data.get("projects", []):
            old_id = p_data.pop("id", None)
            p_data.pop("created_at", None)
            proj = Project(**p_data)
            session.add(proj)
            await session.flush()
            if old_id:
                project_map[old_id] = proj.id

        # Import awards
        for a_data in data.get("awards", []):
            a_data.pop("id", None)
            a_data.pop("created_at", None)
            if a_data.get("project_id") in project_map:
                a_data["project_id"] = project_map[a_data["project_id"]]
            session.add(Award(**a_data))

        # Import settings
        for s_data in data.get("settings", []):
            s_data.pop("updated_at", None)
            existing = await session.get(BotSetting, s_data["key"])
            if existing:
                existing.value = s_data["value"]
                existing.description = s_data.get("description")
                session.add(existing)
            else:
                session.add(BotSetting(**s_data))

        # Import quotes
        for q_data in data.get("quotes", []):
            q_data.pop("id", None)
            q_data.pop("created_at", None)
            session.add(TeamQuote(**q_data))

        await session.commit()
    print("✅ Restore completed successfully!")


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "export"
    path = sys.argv[2] if len(sys.argv) > 2 else "portfolio_backup.json"

    if action == "export":
        asyncio.run(export_data(path))
    elif action == "import":
        asyncio.run(import_data(path))
    else:
        print("Usage: python backup.py [export|import] [filepath]")
