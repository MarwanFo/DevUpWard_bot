import logging
from typing import Literal, Optional
import discord
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger("cogs.admin")

COGS_LIST = [
    "app.bot.cogs.identity",
    "app.bot.cogs.roster",
    "app.bot.cogs.projects",
    "app.bot.cogs.awards",
    "app.bot.cogs.hospitality",
    "app.bot.cogs.voice",
    "app.bot.cogs.admin",
]


class AdminCog(commands.Cog, name="Admin"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="sync", description="Synchronize slash commands with Discord (Admin only).")
    @app_commands.default_permissions(administrator=True)
    async def sync_command(
        self,
        interaction: discord.Interaction,
        scope: Literal["Current Guild", "Global"] = "Current Guild",
    ):
        """Force sync slash commands to Discord."""
        await interaction.response.defer(ephemeral=True)

        try:
            if scope == "Current Guild" and interaction.guild:
                self.bot.tree.copy_global_to(guild=interaction.guild)
                synced = await self.bot.tree.sync(guild=interaction.guild)
                await interaction.followup.send(f"✅ Successfully synced **{len(synced)}** command(s) to guild **{interaction.guild.name}**.", ephemeral=True)
            else:
                synced = await self.bot.tree.sync()
                await interaction.followup.send(f"✅ Successfully synced **{len(synced)}** command(s) globally.", ephemeral=True)
        except Exception as e:
            logger.error(f"Sync error: {e}")
            await interaction.followup.send(f"❌ Failed to sync commands: {e}", ephemeral=True)

    @app_commands.command(name="reload_cogs", description="Hot reload all bot cogs (Admin only).")
    @app_commands.default_permissions(administrator=True)
    async def reload_command(self, interaction: discord.Interaction):
        """Hot-reloads all extension cogs."""
        await interaction.response.defer(ephemeral=True)
        reloaded = []
        errors = []

        for cog in COGS_LIST:
            try:
                await self.bot.reload_extension(cog)
                reloaded.append(cog.split(".")[-1])
            except Exception as e:
                errors.append(f"{cog}: {e}")

        msg = f"🔄 Reloaded {len(reloaded)} cogs: `{', '.join(reloaded)}`"
        if errors:
            msg += f"\n⚠️ Errors:\n" + "\n".join(errors)
        await interaction.followup.send(msg, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCog(bot))

