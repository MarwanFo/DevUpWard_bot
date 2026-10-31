from typing import List
import discord
from discord import app_commands
from discord.ext import commands
from sqlmodel import select
from app.bot.utils import create_base_embed, get_brand_color
from app.core.database import async_session_factory
from app.models.project import Project


def build_project_embed(project: Project, color: discord.Color) -> discord.Embed:
    """Creates a presentation spotlight embed for a project."""
    embed = create_base_embed(
        title=f"💡 {project.title}",
        description=f"**_{project.tagline}_**\n\n{project.description}",
        color=color,
    )

    embed.add_field(name="🏛️ Hackathon", value=f"{project.hackathon_name} ({project.hackathon_year})", inline=True)
    embed.add_field(name="🏷️ Category", value=f"`{project.category}`", inline=True)

    if project.awards_won:
        embed.add_field(name="🏆 Recognition", value=f"**{project.awards_won}**", inline=False)

    if project.banner_url:
        embed.set_image(url=project.banner_url)

    return embed


class ProjectLinksView(discord.ui.View):
    """Buttons linking to live project demo, GitHub repo, and Devpost."""
    def __init__(self, project: Project):
        super().__init__(timeout=180)
        if project.demo_url:
            self.add_item(discord.ui.Button(label="Live Demo", url=project.demo_url, style=discord.ButtonStyle.link, emoji="🚀"))
        if project.repo_url:
            self.add_item(discord.ui.Button(label="Source Code", url=project.repo_url, style=discord.ButtonStyle.link, emoji="💻"))
        if project.devpost_url:
            self.add_item(discord.ui.Button(label="Devpost", url=project.devpost_url, style=discord.ButtonStyle.link, emoji="🏆"))


class ProjectSelect(discord.ui.Select):
    """Dropdown menu to browse projects in /projects."""
    def __init__(self, projects: List[Project], brand_color: discord.Color):
        self.projects_map = {str(p.id): p for p in projects}
        self.brand_color = brand_color

        options = [
            discord.SelectOption(
                label=p.title[:100],
                value=str(p.id),
                description=f"[{p.category}] {p.tagline}"[:100],
                emoji="💡",
            )
            for p in projects[:25]
        ]
        super().__init__(
            placeholder="Select a project to inspect live demo & specs...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        selected_id = self.values[0]
        project = self.projects_map.get(selected_id)
        if not project:
            await interaction.response.send_message("Project not found.", ephemeral=True)
            return

        embed = build_project_embed(project, self.brand_color)
        view = ProjectLinksView(project)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class ProjectShowroomView(discord.ui.View):
    def __init__(self, projects: List[Project], brand_color: discord.Color):
        super().__init__(timeout=180)
        self.add_item(ProjectSelect(projects, brand_color))


async def project_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    """Autocomplete for /project command."""
    async with async_session_factory() as session:
        statement = select(Project)
        projects = (await session.exec(statement)).all()

    choices = []
    current_lower = current.lower()
    for p in projects:
        if current_lower in p.title.lower() or current_lower in p.category.lower():
            choices.append(app_commands.Choice(name=f"{p.title} ({p.hackathon_name})", value=p.title))
        if len(choices) >= 25:
            break
    return choices


class ProjectsCog(commands.Cog, name="Project Showroom"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="projects", description="Explore our catalog of hackathon prototypes and products.")
    async def projects_command(self, interaction: discord.Interaction):
        """Displays interactive project catalog."""
        await interaction.response.defer()
        brand_color = await get_brand_color()

        async with async_session_factory() as session:
            statement = select(Project).order_by(Project.display_order.asc(), Project.id.desc())
            projects = (await session.exec(statement)).all()

        if not projects:
            await interaction.followup.send("No projects currently in the showroom.")
            return

        embed = create_base_embed(
            title="💡 DevUpward Project Showroom",
            description="Explore the prototypes and platforms we have engineered during 48-hour competitions. Select any project from the menu below for screenshots, architecture, and live links.",
            color=brand_color,
        )

        for p in projects:
            awards_badge = f"\n_{p.awards_won}_" if p.awards_won else ""
            embed.add_field(
                name=f"• {p.title} [`{p.category}`]",
                value=f"{p.tagline}{awards_badge}\n🏛️ _{p.hackathon_name}_",
                inline=False,
            )

        view = ProjectShowroomView(projects, brand_color)
        await interaction.followup.send(embed=embed, view=view)

    @app_commands.command(name="project", description="Spotlight a specific project by name.")
    @app_commands.autocomplete(name=project_autocomplete)
    async def project_command(self, interaction: discord.Interaction, name: str):
        """Lookup an individual project spotlight."""
        await interaction.response.defer()
        brand_color = await get_brand_color()

        async with async_session_factory() as session:
            statement = select(Project).where(Project.title.ilike(f"%{name}%"))
            result = await session.exec(statement)
            project = result.first()

        if not project:
            await interaction.followup.send(f"❌ Project '{name}' not found. Use `/projects` to browse the catalog.", ephemeral=True)
            return

        embed = build_project_embed(project, brand_color)
        view = ProjectLinksView(project)
        await interaction.followup.send(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(ProjectsCog(bot))

