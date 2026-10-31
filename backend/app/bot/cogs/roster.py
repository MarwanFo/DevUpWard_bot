import json
from typing import List, Optional
import discord
from discord import app_commands
from discord.ext import commands
from sqlmodel import select
from app.bot.utils import create_base_embed, get_brand_color
from app.core.database import async_session_factory
from app.models.team import TeamMember


def build_member_embed(member: TeamMember, color: discord.Color) -> discord.Embed:
    """Builds a polished profile card for a team member."""
    embed = create_base_embed(
        title=f"👤 {member.name}",
        description=f"**{member.role}**\n\n{member.bio}",
        color=color,
    )

    if member.avatar_url:
        embed.set_thumbnail(url=member.avatar_url)

    # Parse and format skills badges
    try:
        skills_list = json.loads(member.skills) if member.skills else []
        if skills_list:
            formatted_skills = " • ".join(f"`{s}`" for s in skills_list)
            embed.add_field(name="🛠️ Skills & Specialties", value=formatted_skills, inline=False)
    except Exception:
        pass

    if member.discord_id:
        embed.add_field(name="💬 Discord", value=f"<@{member.discord_id}>", inline=True)

    return embed


class MemberLinksView(discord.ui.View):
    """Buttons linking to a member's personal portfolio, GitHub, LinkedIn."""
    def __init__(self, member: TeamMember):
        super().__init__(timeout=180)
        if member.portfolio_url:
            self.add_item(discord.ui.Button(label="Portfolio", url=member.portfolio_url, style=discord.ButtonStyle.link, emoji="🔗"))
        if member.github_url:
            self.add_item(discord.ui.Button(label="GitHub", url=member.github_url, style=discord.ButtonStyle.link, emoji="💻"))
        if member.linkedin_url:
            self.add_item(discord.ui.Button(label="LinkedIn", url=member.linkedin_url, style=discord.ButtonStyle.link, emoji="💼"))


class TeamRosterSelect(discord.ui.Select):
    """Dropdown menu allowing users to inspect any member directly from /team."""
    def __init__(self, members: List[TeamMember], brand_color: discord.Color):
        self.members_map = {str(m.id): m for m in members}
        self.brand_color = brand_color

        options = [
            discord.SelectOption(
                label=m.name,
                value=str(m.id),
                description=m.role[:100],
                emoji="👤",
            )
            for m in members[:25]  # Discord limit for select options
        ]
        super().__init__(
            placeholder="Select a squad member to view their profile...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        selected_id = self.values[0]
        member = self.members_map.get(selected_id)
        if not member:
            await interaction.response.send_message("Member not found.", ephemeral=True)
            return

        embed = build_member_embed(member, self.brand_color)
        view = MemberLinksView(member)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class TeamRosterView(discord.ui.View):
    def __init__(self, members: List[TeamMember], brand_color: discord.Color):
        super().__init__(timeout=180)
        self.add_item(TeamRosterSelect(members, brand_color))


async def member_name_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    """Autocomplete helper for /member command."""
    async with async_session_factory() as session:
        statement = select(TeamMember).where(TeamMember.is_active == True)  # noqa: E712
        members = (await session.exec(statement)).all()

    choices = []
    current_lower = current.lower()
    for m in members:
        if current_lower in m.name.lower() or current_lower in m.role.lower():
            choices.append(app_commands.Choice(name=f"{m.name} ({m.role})", value=m.name))
        if len(choices) >= 25:
            break
    return choices


class RosterCog(commands.Cog, name="Team Roster"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="team", description="Browse our hackathon squad roster and core roles.")
    async def team_command(self, interaction: discord.Interaction):
        """Displays full roster with interactive member select menu."""
        await interaction.response.defer()
        brand_color = await get_brand_color()

        async with async_session_factory() as session:
            statement = select(TeamMember).where(TeamMember.is_active == True).order_by(TeamMember.display_order.asc())  # noqa: E712
            members = (await session.exec(statement)).all()

        if not members:
            await interaction.followup.send("No active team members found.")
            return

        embed = create_base_embed(
            title="👥 The DevUpward Squad",
            description="Meet the builders, designers, and strategists behind our hackathon projects. Select any member below to inspect their bio and personal links.",
            color=brand_color,
        )

        for m in members:
            embed.add_field(
                name=f"• {m.name}",
                value=f"_{m.role}_\n{m.bio[:120]}...",
                inline=True,
            )

        view = TeamRosterView(members, brand_color)
        await interaction.followup.send(embed=embed, view=view)

    @app_commands.command(name="member", description="View a specific team member's full profile and specialties.")
    @app_commands.autocomplete(name=member_name_autocomplete)
    async def member_command(self, interaction: discord.Interaction, name: str):
        """Lookup an individual member profile."""
        await interaction.response.defer()
        brand_color = await get_brand_color()

        async with async_session_factory() as session:
            statement = select(TeamMember).where(TeamMember.name.ilike(f"%{name}%"))
            result = await session.exec(statement)
            member = result.first()

        if not member:
            await interaction.followup.send(f"❌ Could not find a team member matching '{name}'. Use `/team` to see the full roster.", ephemeral=True)
            return

        embed = build_member_embed(member, brand_color)
        view = MemberLinksView(member)
        await interaction.followup.send(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(RosterCog(bot))

