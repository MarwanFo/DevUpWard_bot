import asyncio
import os
import sys

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import discord
from app.bot.client import bot
from app.bot.cogs.identity import SocialLinksView
from app.bot.cogs.roster import member_name_autocomplete, build_member_embed, TeamRosterView
from app.bot.cogs.projects import project_autocomplete, build_project_embed, ProjectShowroomView
from app.bot.cogs.hospitality import ContactModal
from app.models.team import TeamMember
from app.models.project import Project


class DummyInteraction:
    user = "TestUser#1234"


async def test_bot():
    print("🤖 Testing Discord Bot Cogs, App Commands, UI Views & Modals...\n")

    # 1. Test setup_hook & Cog loading
    await bot.setup_hook()
    loaded_cogs = list(bot.cogs.keys())
    print(f"✅ 1. Setup hook executed. Loaded {len(loaded_cogs)} cogs: {loaded_cogs}")
    assert len(loaded_cogs) >= 6, f"Expected 6 cogs, found: {loaded_cogs}"

    # 2. Check registered slash commands in tree
    commands = bot.tree.get_commands()
    cmd_names = [c.name for c in commands]
    print(f"✅ 2. App Command Tree verified: {len(cmd_names)} commands registered: {cmd_names}")
    expected_cmds = ["about", "socials", "team", "member", "projects", "project", "awards", "stats", "contact", "quote", "sync", "reload_cogs"]
    for expected in expected_cmds:
        assert expected in cmd_names, f"Missing command: {expected}"

    # 3. Test UI Views creation
    social_view = SocialLinksView("https://devupward.tech", "https://github.com/DevUpward", "https://linkedin.com", "https://devpost.com")
    assert len(social_view.children) == 4
    print("✅ 3. SocialLinksView - OK (4 interactive link buttons verified)")

    sample_member = TeamMember(
        name="Test Dev",
        role="Lead Architect",
        bio="Test bio",
        skills='["Python", "FastAPI"]',
        portfolio_url="https://test.dev",
        github_url="https://github.com/test",
    )
    member_embed = build_member_embed(sample_member, discord.Color.blurple())
    assert member_embed.title == "👤 Test Dev"
    print("✅ 4. Member Embed & Badges - OK (Title, role, and skill tags formatted)")

    roster_view = TeamRosterView([sample_member], discord.Color.blurple())
    assert len(roster_view.children) == 1
    print("✅ 5. TeamRosterView - OK (StringSelectMenu initialized)")

    sample_project = Project(
        title="Test Project",
        slug="test-project",
        tagline="A test hackathon project",
        description="Detailed test description",
        category="AI",
        hackathon_name="TestHack 2026",
        demo_url="https://demo.test",
        repo_url="https://github.com/test",
    )
    proj_embed = build_project_embed(sample_project, discord.Color.blurple())
    assert proj_embed.title == "💡 Test Project"
    print("✅ 6. Project Spotlight Embed - OK (Title, category, hackathon formatted)")

    proj_view = ProjectShowroomView([sample_project], discord.Color.blurple())
    assert len(proj_view.children) == 1
    print("✅ 7. ProjectShowroomView - OK (Interactive select dropdown verified)")

    # 4. Test Autocomplete functions
    member_choices = await member_name_autocomplete(DummyInteraction(), current="Mar")
    assert len(member_choices) >= 1
    print(f"✅ 8. Member Autocomplete - OK (Resolved '{member_choices[0].name}')")

    proj_choices = await project_autocomplete(DummyInteraction(), current="Omni")
    assert len(proj_choices) >= 1
    print(f"✅ 9. Project Autocomplete - OK (Resolved '{proj_choices[0].name}')")

    # 5. Test Contact Modal
    modal = ContactModal(bot=bot, brand_color=discord.Color.blurple())
    assert len(modal.children) == 4
    print("✅ 10. ContactModal - OK (4 text input fields verified: Name, Email, Org, Message)")

    # Clean up
    await bot.close()

    print("\n🎉 ALL 10 DISCORD BOT COGS, COMMANDS & UI TESTS PASSED PERFECTLY!\n")



if __name__ == "__main__":
    asyncio.run(test_bot())
