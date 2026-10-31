import discord
from discord import app_commands
from discord.ext import commands
from sqlmodel import select
from app.bot.utils import create_base_embed, get_brand_color, get_setting
from app.core.database import async_session_factory
from app.models.award import Award
from app.models.project import Project
from app.models.team import TeamMember


class AwardsCog(commands.Cog, name="Hall of Fame"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="awards", description="View our hackathon track record, podium finishes, and honors.")
    async def awards_command(self, interaction: discord.Interaction):
        """Displays chronological trophy room."""
        await interaction.response.defer()
        brand_color = await get_brand_color()

        async with async_session_factory() as session:
            statement = select(Award).order_by(Award.year.desc(), Award.id.desc())
            awards = (await session.exec(statement)).all()

        if not awards:
            await interaction.followup.send("No awards recorded yet.")
            return

        embed = create_base_embed(
            title="🏆 Hackathon Hall of Fame (Palmarès)",
            description="A chronological record of our competition wins, category prizes, and jury recognitions.",
            color=brand_color,
        )

        for a in awards:
            placement_badge = a.icon or "🏆"
            prize = f" • _{a.prize_description}_" if a.prize_description else ""
            category_tag = f" `[{a.category}]`" if a.category else ""

            embed.add_field(
                name=f"{placement_badge} {a.award_title}{category_tag}",
                value=f"🏛️ **{a.hackathon_name}** ({a.year}){prize}",
                inline=False,
            )

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="stats", description="Review our team lifetime statistics and metrics.")
    async def stats_command(self, interaction: discord.Interaction):
        """Displays aggregate team statistics."""
        await interaction.response.defer()
        brand_color = await get_brand_color()

        async with async_session_factory() as session:
            members = (await session.exec(select(TeamMember).where(TeamMember.is_active == True))).all()  # noqa: E712
            projects = (await session.exec(select(Project))).all()
            awards = (await session.exec(select(Award))).all()

        hackathon_names = {p.hackathon_name for p in projects} | {a.hackathon_name for a in awards}
        first_places = sum(1 for a in awards if a.placement == 1)
        podiums = sum(1 for a in awards if a.placement in [1, 2, 3])
        coffee = await get_setting("coffee_cups_consumed", "420")

        embed = create_base_embed(
            title="📊 DevUpward Team Analytics",
            description="Cumulative statistics from our competitive hackathon career.",
            color=brand_color,
        )

        embed.add_field(name="🏛️ Hackathons Attended", value=f"**{len(hackathon_names)}** Events", inline=True)
        embed.add_field(name="💡 Projects Shipped", value=f"**{len(projects)}** Prototypes", inline=True)
        embed.add_field(name="🏆 Awards & Honors", value=f"**{len(awards)}** Trophies", inline=True)

        embed.add_field(name="🥇 1st Place Wins", value=f"**{first_places}** Grand Prizes", inline=True)
        embed.add_field(name="🏅 Podium Finishes", value=f"**{podiums}** Top 3 Placements", inline=True)
        embed.add_field(name="☕ Coffee Consumed", value=f"**~{coffee}** Cups", inline=True)

        embed.add_field(
            name="👥 Squad Roster",
            value=f"**{len(members)}** Core active developers & designers.",
            inline=False,
        )

        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(AwardsCog(bot))

