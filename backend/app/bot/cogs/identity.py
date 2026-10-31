import asyncio
import logging
import discord
from discord import app_commands
from discord.ext import commands, tasks
from sqlmodel import select
from app.bot.utils import create_base_embed, get_brand_color, get_setting
from app.core.database import async_session_factory
from app.models.award import Award
from app.models.project import Project
from app.models.team import TeamMember

logger = logging.getLogger("cogs.identity")


class SocialLinksView(discord.ui.View):
    def __init__(self, website: str, github: str, linkedin: str, devpost: str):
        super().__init__(timeout=None)
        if website:
            self.add_item(discord.ui.Button(label="Website", url=website, style=discord.ButtonStyle.link, emoji="🌐"))
        if github:
            self.add_item(discord.ui.Button(label="GitHub", url=github, style=discord.ButtonStyle.link, emoji="💻"))
        if linkedin:
            self.add_item(discord.ui.Button(label="LinkedIn", url=linkedin, style=discord.ButtonStyle.link, emoji="💼"))
        if devpost:
            self.add_item(discord.ui.Button(label="Devpost", url=devpost, style=discord.ButtonStyle.link, emoji="🏆"))


class IdentityCog(commands.Cog, name="Identity"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.presence_index = 0
        self.presence_rotator.start()

    def cog_unload(self):
        self.presence_rotator.cancel()

    @tasks.loop(minutes=10)
    async def presence_rotator(self):
        """Periodically cycles through team status highlights."""
        if not self.bot.is_ready():
            return

        try:
            # Check if custom status is configured
            custom_status = await get_setting("presence_status")
            async with async_session_factory() as session:
                awards_count = len((await session.exec(select(Award))).all())
                projects_count = len((await session.exec(select(Project))).all())

            statuses = [
                custom_status or "🚀 Building high-impact prototypes",
                f"🏆 {awards_count} Hackathon Awards Won",
                f"💡 {projects_count} Projects Built • /projects",
                "⚡ Type /about to meet the squad",
            ]

            selected_status = statuses[self.presence_index % len(statuses)]
            self.presence_index += 1

            activity = discord.Activity(
                type=discord.ActivityType.watching,
                name=selected_status,
            )
            await self.bot.change_presence(status=discord.Status.online, activity=activity)
        except Exception as e:
            logger.error(f"Error rotating presence: {e}")

    @presence_rotator.before_loop
    async def before_presence_rotator(self):
        try:
            await self.bot.wait_until_ready()
        except (RuntimeError, asyncio.CancelledError):
            pass


    @app_commands.command(name="about", description="Discover our hackathon team identity, mission, and focus.")
    async def about_command(self, interaction: discord.Interaction):
        """Displays the official team brand card."""
        await interaction.response.defer()

        team_name = await get_setting("team_name", "DevUpward")
        team_motto = await get_setting("team_motto", "Building the future, one hackathon at a time")
        team_about = await get_setting("team_about", "Elite hackathon squad specialized in AI and full-stack solutions.")
        brand_color = await get_brand_color()

        async with async_session_factory() as session:
            members_count = len((await session.exec(select(TeamMember).where(TeamMember.is_active == True))).all())  # noqa: E712
            projects_count = len((await session.exec(select(Project))).all())
            awards_count = len((await session.exec(select(Award))).all())

        embed = create_base_embed(
            title=f"⚡ {team_name} — Official Showcase",
            description=f"**_{team_motto}_**\n\n{team_about}",
            color=brand_color,
        )

        embed.add_field(
            name="🎯 Core Specializations",
            value="`Autonomous AI Agents` • `Full-Stack Web` • `Smart Contracts / Web3` • `Developer Tooling`",
            inline=False,
        )

        embed.add_field(
            name="📊 Squad Track Record",
            value=f"👥 **{members_count}** Core Members\n💡 **{projects_count}** Shipped Prototypes\n🏆 **{awards_count}** Hackathon Awards",
            inline=True,
        )

        embed.add_field(
            name="🧭 How to Explore",
            value="`/team` — View squad roster\n`/projects` — Interactive showroom\n`/awards` — Hall of Fame\n`/contact` — Propose collaboration",
            inline=True,
        )

        website = await get_setting("website_url", "https://devupward.tech")
        github = await get_setting("github_org_url", "https://github.com/DevUpward")
        linkedin = await get_setting("linkedin_org_url", "https://linkedin.com")
        devpost = await get_setting("devpost_url", "https://devpost.com")

        view = SocialLinksView(website=website, github=github, linkedin=linkedin, devpost=devpost)
        await interaction.followup.send(embed=embed, view=view)

    @app_commands.command(name="socials", description="Get direct links to all our official channels and platforms.")
    async def socials_command(self, interaction: discord.Interaction):
        """Displays official team links and channels."""
        brand_color = await get_brand_color()
        team_name = await get_setting("team_name", "DevUpward")

        website = await get_setting("website_url", "https://devupward.tech")
        github = await get_setting("github_org_url", "https://github.com/DevUpward")
        linkedin = await get_setting("linkedin_org_url", "https://linkedin.com")
        devpost = await get_setting("devpost_url", "https://devpost.com")

        embed = create_base_embed(
            title=f"🌐 Connect with {team_name}",
            description="Explore our repositories, read our project write-ups, or follow our hackathon journey across platforms.",
            color=brand_color,
        )

        view = SocialLinksView(website=website, github=github, linkedin=linkedin, devpost=devpost)
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(IdentityCog(bot))
