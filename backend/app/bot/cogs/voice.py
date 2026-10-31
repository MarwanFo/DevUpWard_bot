import asyncio
import logging
from typing import Dict, Optional
import discord
from discord import app_commands
from discord.ext import commands, tasks
from app.bot.utils import create_base_embed, get_brand_color
from app.core.config import settings

logger = logging.getLogger("cogs.voice")


class Voice(commands.Cog, name="Voice 24/7"):
    """Cog for persistent 24/7 voice channel connectivity and management."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Maps guild_id -> target voice channel_id for 24/7 persistence
        self.persistent_channels: Dict[int, int] = {}
        self.voice_reconnect_loop.start()

    def cog_unload(self):
        self.voice_reconnect_loop.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        """Auto-join configured voice channel from settings on bot ready."""
        await self._check_initial_voice_join()

    async def _check_initial_voice_join(self):
        """Connect to default DISCORD_VOICE_CHANNEL_ID if configured."""
        if not settings.DISCORD_VOICE_CHANNEL_ID or not str(settings.DISCORD_VOICE_CHANNEL_ID).isdigit():
            return

        channel_id = int(settings.DISCORD_VOICE_CHANNEL_ID)
        await self.bot.wait_until_ready()
        try:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                channel = await self.bot.fetch_channel(channel_id)

            if isinstance(channel, discord.VoiceChannel):
                self.persistent_channels[channel.guild.id] = channel.id
                await self._ensure_connected(channel)
                logger.info(f"🔊 Auto-joined 24/7 voice channel: {channel.name} in {channel.guild.name}")
        except Exception as e:
            logger.error(f"Failed to auto-join initial voice channel {channel_id}: {e}")

    async def _ensure_connected(self, channel: discord.VoiceChannel) -> Optional[discord.VoiceClient]:
        """Ensure bot is connected to the specified voice channel."""
        try:
            guild = channel.guild
            vc: Optional[discord.VoiceClient] = getattr(guild, "voice_client", None)

            if vc is not None:
                if vc.channel and vc.channel.id != channel.id:
                    await vc.move_to(channel)
                return vc
            else:
                return await channel.connect(self_deaf=True)
        except Exception as e:
            logger.error(f"Error ensuring connection to voice channel {channel.id}: {e}")
            return None

    @tasks.loop(seconds=20)
    async def voice_reconnect_loop(self):
        """Keep-alive watchdog: ensures the bot stays in the 24/7 voice channel."""
        if not self.bot.is_ready():
            return

        for guild_id, channel_id in list(self.persistent_channels.items()):
            try:
                guild = self.bot.get_guild(guild_id)
                if not guild:
                    continue

                vc: Optional[discord.VoiceClient] = getattr(guild, "voice_client", None)
                if vc is None or not vc.is_connected() or vc.channel is None or vc.channel.id != channel_id:
                    channel = guild.get_channel(channel_id)
                    if isinstance(channel, discord.VoiceChannel):
                        logger.info(f"🔄 Reconnecting to 24/7 voice channel: {channel.name}")
                        await self._ensure_connected(channel)
            except Exception as e:
                logger.warning(f"Voice watchdog error for guild {guild_id}: {e}")

    @voice_reconnect_loop.before_loop
    async def before_reconnect_loop(self):
        try:
            await self.bot.wait_until_ready()
        except (RuntimeError, asyncio.CancelledError):
            pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """Immediately trigger reconnect if bot is disconnected while 24/7 is active."""
        if self.bot.user and member.id == self.bot.user.id:
            guild_id = member.guild.id
            target_channel_id = self.persistent_channels.get(guild_id)
            if target_channel_id and (after.channel is None or after.channel.id != target_channel_id):
                # Bot was moved or disconnected; wait 2s and reconnect
                await asyncio.sleep(2)
                channel = member.guild.get_channel(target_channel_id)
                if isinstance(channel, discord.VoiceChannel):
                    logger.info(f"⚡ Instant reconnect triggered for 24/7 voice: {channel.name}")
                    await self._ensure_connected(channel)

    @app_commands.command(name="join", description="Join a voice channel and maintain 24/7 presence")
    @app_commands.describe(channel="The voice channel to join (optional - defaults to your current channel)")
    async def join(self, interaction: discord.Interaction, channel: Optional[discord.VoiceChannel] = None):
        """Join a voice channel and enable 24/7 keep-alive mode."""
        await interaction.response.defer(ephemeral=False)
        brand_color = await get_brand_color()

        target_channel: Optional[discord.VoiceChannel] = channel
        if not target_channel:
            if isinstance(interaction.user, discord.Member) and interaction.user.voice and interaction.user.voice.channel:
                if isinstance(interaction.user.voice.channel, discord.VoiceChannel):
                    target_channel = interaction.user.voice.channel

        if not target_channel:
            embed = create_base_embed(
                title="❌ Voice Channel Required",
                description="Please either **specify a voice channel** in the command or **join a voice channel** first!",
                color=discord.Color.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        try:
            vc = await self._ensure_connected(target_channel)
            if not vc:
                embed = create_base_embed(
                    title="❌ Connection Failed",
                    description=f"Could not connect to {target_channel.mention}. Please check bot permissions (`Connect`, `Speak`).",
                    color=discord.Color.red(),
                )
                await interaction.followup.send(embed=embed)
                return

            # Activate 24/7 tracking for this guild
            if interaction.guild_id:
                self.persistent_channels[interaction.guild_id] = target_channel.id

            embed = create_base_embed(
                title="🔊 Connected to Voice Channel",
                description=f"Successfully joined **{target_channel.mention}** with **24/7 Keep-Alive Mode Active**!",
                color=brand_color,
            )
            embed.add_field(name="Channel", value=target_channel.name, inline=True)
            embed.add_field(name="Bitrate", value=f"{target_channel.bitrate // 1000} kbps", inline=True)
            embed.add_field(name="24/7 Mode", value="🟢 **Enabled** (Auto-Reconnect ON)", inline=True)
            embed.add_field(name="Self Deafen", value="🎧 Enabled (Bandwidth Optimized)", inline=True)
            embed.set_footer(text="DevUpward Showcase • 24/7 Voice Presence")

            await interaction.followup.send(embed=embed)
        except Exception as e:
            logger.error(f"Error in /join command: {e}")
            embed = create_base_embed(
                title="❌ Error Joining Voice",
                description=f"An unexpected error occurred: `{str(e)}`",
                color=discord.Color.red(),
            )
            await interaction.followup.send(embed=embed)

    @app_commands.command(name="leave", description="Disconnect the bot from voice and disable 24/7 mode")
    async def leave(self, interaction: discord.Interaction):
        """Disconnect the bot from voice and stop 24/7 mode."""
        await interaction.response.defer(ephemeral=False)
        brand_color = await get_brand_color()

        if not interaction.guild:
            await interaction.followup.send("This command can only be used in a server.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        # Stop 24/7 monitoring
        self.persistent_channels.pop(guild_id, None)

        vc: Optional[discord.VoiceClient] = getattr(interaction.guild, "voice_client", None)
        if vc and vc.is_connected():
            channel_name = vc.channel.name if vc.channel else "Voice Channel"
            await vc.disconnect(force=True)
            embed = create_base_embed(
                title="👋 Disconnected from Voice",
                description=f"Disconnected from **{channel_name}**. 24/7 keep-alive mode disabled.",
                color=brand_color,
            )
        else:
            embed = create_base_embed(
                title="ℹ️ Not in Voice",
                description="I am not currently connected to any voice channel in this server.",
                color=brand_color,
            )

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="voice_status", description="Check the current 24/7 voice connection status")
    async def voice_status(self, interaction: discord.Interaction):
        """Check voice connection telemetry."""
        brand_color = await get_brand_color()
        if not interaction.guild:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        vc: Optional[discord.VoiceClient] = getattr(interaction.guild, "voice_client", None)
        is_247 = guild_id in self.persistent_channels

        embed = create_base_embed(
            title="🎙️ Voice System Telemetry",
            color=brand_color,
        )

        if vc and vc.is_connected() and vc.channel:
            embed.add_field(name="Status", value="🟢 **Connected**", inline=True)
            embed.add_field(name="Current Channel", value=vc.channel.name, inline=True)
            latency_ms = round(vc.latency * 1000, 1) if hasattr(vc, "latency") else "N/A"
            embed.add_field(name="Voice Latency", value=f"{latency_ms} ms", inline=True)
            embed.add_field(name="24/7 Keep-Alive", value="🟢 **Active**" if is_247 else "⚪ Inactive", inline=True)
            embed.add_field(name="Bitrate", value=f"{vc.channel.bitrate // 1000} kbps" if hasattr(vc.channel, "bitrate") else "N/A", inline=True)
        else:
            embed.add_field(name="Status", value="⚪ **Disconnected**", inline=True)
            target_id = self.persistent_channels.get(guild_id)
            target_name = f"<#{target_id}>" if target_id else "None"
            embed.add_field(name="24/7 Target Channel", value=target_name, inline=True)
            embed.add_field(name="Action", value="Use `/join` to start 24/7 voice presence.", inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Voice(bot))
