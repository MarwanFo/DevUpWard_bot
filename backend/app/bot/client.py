import asyncio
import logging
import time
from typing import Optional
import discord
from discord.ext import commands
from app.core.config import settings
from app.models.inbox import ContactSubmission

logger = logging.getLogger("bot")
logging.basicConfig(level=logging.INFO)


class ShowcaseBot(commands.Bot):
    def __init__(self):
        # Configure intents: default + members (for welcome onboarding)
        intents = discord.Intents.default()
        intents.members = True

        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,
        )
        self.start_time: float = time.time()
        self.is_connected_to_gateway: bool = False

    async def setup_hook(self) -> None:
        """Called automatically before the bot connects to Discord Gateway."""
        logger.info("🤖 Bot setup hook triggered. Loading extensions...")
        cogs_to_load = [
            "app.bot.cogs.identity",
            "app.bot.cogs.roster",
            "app.bot.cogs.projects",
            "app.bot.cogs.awards",
            "app.bot.cogs.hospitality",
            "app.bot.cogs.admin",
        ]
        for cog in cogs_to_load:
            try:
                await self.load_extension(cog)
                logger.info(f"  ✓ Loaded cog extension: {cog}")
            except Exception as e:
                logger.error(f"  ✗ Failed to load cog {cog}: {e}")


    async def on_ready(self) -> None:
        self.is_connected_to_gateway = True
        logger.info(f"✅ Discord Bot logged in as {self.user} (ID: {self.user.id})")
        logger.info(f"🌐 Connected to {len(self.guilds)} guild(s)")

        # Set initial presence from settings or default
        await self.set_presence(
            status_text=settings.TEAM_MOTTO or "🏆 Preparing for Hackathons",
            activity_type="watching"
        )

    async def set_presence(self, status_text: str, activity_type: str = "watching") -> None:
        """Update the bot's dynamic rich presence."""
        if not self.is_ready():
            return

        type_map = {
            "playing": discord.ActivityType.playing,
            "watching": discord.ActivityType.watching,
            "listening": discord.ActivityType.listening,
            "competing": discord.ActivityType.competing,
        }
        activity = discord.Activity(
            type=type_map.get(activity_type.lower(), discord.ActivityType.watching),
            name=status_text,
        )
        await self.change_presence(status=discord.Status.online, activity=activity)
        logger.info(f"🔄 Bot presence updated: {activity_type} '{status_text}'")

    async def sync_app_commands(self, guild_id: Optional[int] = None) -> int:
        """Sync application slash commands with Discord."""
        if not self.is_ready():
            logger.warning("Bot is not ready. Cannot sync commands.")
            return 0

        if guild_id:
            guild = discord.Object(id=guild_id)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            logger.info(f"⚡ Synced {len(synced)} command(s) to guild {guild_id}")
            return len(synced)
        else:
            synced = await self.tree.sync()
            logger.info(f"⚡ Synced {len(synced)} global command(s)")
            return len(synced)

    async def send_inbox_notification(self, submission: ContactSubmission) -> bool:
        """Send an embed notification to the configured Discord inbox channel."""
        if not self.is_ready() or not settings.DISCORD_INBOX_CHANNEL_ID:
            return False

        try:
            channel_id = int(settings.DISCORD_INBOX_CHANNEL_ID)
            channel = self.get_channel(channel_id)
            if not channel:
                channel = await self.fetch_channel(channel_id)

            if isinstance(channel, discord.TextChannel):
                embed = discord.Embed(
                    title="📬 New Visitor Inquiry Received!",
                    description=submission.message,
                    color=discord.Color.from_str(settings.BRAND_COLOR or "#5865F2"),
                )
                embed.add_field(name="Sender", value=submission.sender_name, inline=True)
                if submission.email:
                    embed.add_field(name="Email", value=submission.email, inline=True)
                if submission.organization:
                    embed.add_field(name="Organization", value=submission.organization, inline=True)
                if submission.discord_tag:
                    embed.add_field(name="Discord Tag", value=submission.discord_tag, inline=True)
                embed.set_footer(text=f"Submission #{submission.id} • Showcase Bot Bridge")

                await channel.send(embed=embed)
                return True
        except Exception as e:
            logger.error(f"Failed to dispatch inbox notification to Discord: {e}")
            return False

    def get_telemetry(self) -> dict:
        """Get live telemetry stats for the React dashboard."""
        is_ready = self.is_ready()
        uptime_seconds = int(time.time() - self.start_time) if is_ready else 0

        return {
            "is_online": is_ready,
            "bot_user": str(self.user) if self.user else None,
            "bot_id": str(self.user.id) if self.user else None,
            "latency_ms": round(self.latency * 1000, 2) if is_ready and self.latency != float("inf") else 0,
            "guild_count": len(self.guilds) if is_ready else 0,
            "uptime_seconds": uptime_seconds,
        }


# Global singleton instance of the bot
bot = ShowcaseBot()

