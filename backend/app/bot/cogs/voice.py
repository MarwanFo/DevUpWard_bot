import logging
from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands
from app.bot.utils import create_base_embed, get_brand_color
from app.core.config import settings

logger = logging.getLogger("cogs.voice")


class Voice(commands.Cog, name="Voice 24/7"):
    """Cog for persistent 24/7 voice channel connectivity and management."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_unload(self) -> None:
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        """Auto-join configured voice channel on bot startup if specified in .env."""
        await self._check_initial_voice_join()

    async def _check_initial_voice_join(self):
        """Connect to default DISCORD_VOICE_CHANNEL_ID if configured on boot."""
        if not settings.DISCORD_VOICE_CHANNEL_ID or not settings.DISCORD_VOICE_CHANNEL_ID.isdigit():
            return

        channel_id = int(settings.DISCORD_VOICE_CHANNEL_ID)
        await self.bot.wait_until_ready()
        try:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                channel = await self.bot.fetch_channel(channel_id)

            if isinstance(channel, discord.VoiceChannel):
                await self._ensure_connected(channel)
                logger.info(f"🔊 Auto-joined voice channel on startup: {channel.name} in {channel.guild.name}")
        except Exception as e:
            logger.error(f"Failed to auto-join initial voice channel {channel_id}: {e}")

    async def _ensure_connected(self, channel: discord.VoiceChannel) -> tuple[Optional[discord.VoiceClient], Optional[str]]:
        """Ensure bot is connected to the specified voice channel."""
        try:
            guild = channel.guild
            vc: Optional[discord.VoiceClient] = getattr(guild, "voice_client", None)

            if vc is not None:
                if vc.channel and vc.channel.id != channel.id:
                    await vc.move_to(channel)
                return vc, None
            else:
                new_vc = await channel.connect(self_deaf=True)
                return new_vc, None
        except Exception as e:
            err_msg = str(e)
            logger.error(f"Error ensuring connection to voice channel {channel.id}: {err_msg}")
            return None, err_msg

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """Handle voice state changes for the bot."""
        if self.bot.user and member.id == self.bot.user.id:
            guild_id = member.guild.id
            if after.channel is None:
                # User or moderator disconnected the bot — respect it and stay disconnected!
                logger.info(f"🛑 Bot was disconnected from voice in guild {guild_id}. Staying disconnected.")
            elif after.channel is not None and isinstance(after.channel, discord.VoiceChannel):
                logger.info(f"🔄 Bot is in voice channel: {after.channel.name}")

    @app_commands.command(name="join", description="Join a voice channel and maintain 24/7 presence")
    @app_commands.describe(channel="The voice channel to join (optional - defaults to your current channel)")
    async def join(self, interaction: discord.Interaction, channel: Optional[discord.VoiceChannel] = None):
        """Join a voice channel and stay 24/7 until manually disconnected or /leave."""
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
            vc, err = await self._ensure_connected(target_channel)
            if not vc:
                err_detail = f"\n\n*Error details:* `{err}`" if err else ""
                embed = create_base_embed(
                    title="❌ Connection Failed",
                    description=f"Could not connect to {target_channel.mention}. Please ensure the bot has **Connect** and **Speak** permissions.{err_detail}",
                    color=discord.Color.red(),
                )
                await interaction.followup.send(embed=embed)
                return

            embed = create_base_embed(
                title="🔊 Connected to Voice Channel",
                description=f"Successfully joined **{target_channel.mention}**! Bot will stay connected 24/7 until disconnected.",
                color=brand_color,
            )
            embed.add_field(name="Channel", value=target_channel.name, inline=True)
            embed.add_field(name="Bitrate", value=f"{target_channel.bitrate // 1000} kbps", inline=True)
            embed.add_field(name="Presence", value="🟢 **24/7 Active**", inline=True)
            embed.add_field(name="Self Deafen", value="🎧 Enabled (Bandwidth Optimized)", inline=True)
            embed.set_footer(text="DevUpward Showcase • Type /leave or disconnect to remove bot")

            await interaction.followup.send(embed=embed)
        except Exception as e:
            logger.error(f"Error in /join command: {e}")
            embed = create_base_embed(
                title="❌ Error Joining Voice",
                description=f"An unexpected error occurred: `{str(e)}`",
                color=discord.Color.red(),
            )
            await interaction.followup.send(embed=embed)

    @app_commands.command(name="leave", description="Disconnect the bot from voice")
    async def leave(self, interaction: discord.Interaction):
        """Disconnect the bot from voice."""
        await interaction.response.defer(ephemeral=False)
        brand_color = await get_brand_color()

        if not interaction.guild:
            await interaction.followup.send("This command can only be used in a server.", ephemeral=True)
            return

        vc: Optional[discord.VoiceClient] = getattr(interaction.guild, "voice_client", None)
        if vc and vc.is_connected():
            channel_name = vc.channel.name if vc.channel else "Voice Channel"
            await vc.disconnect(force=True)
            embed = create_base_embed(
                title="👋 Disconnected from Voice",
                description=f"Disconnected from **{channel_name}**.",
                color=brand_color,
            )
        else:
            embed = create_base_embed(
                title="ℹ️ Not in Voice",
                description="I am not currently connected to any voice channel in this server.",
                color=brand_color,
            )

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="voice_status", description="Check the current voice connection status")
    async def voice_status(self, interaction: discord.Interaction):
        """Check voice connection telemetry."""
        brand_color = await get_brand_color()
        if not interaction.guild:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return

        vc: Optional[discord.VoiceClient] = getattr(interaction.guild, "voice_client", None)

        embed = create_base_embed(
            title="🎙️ Voice System Telemetry",
            color=brand_color,
        )

        if vc and vc.is_connected() and vc.channel:
            embed.add_field(name="Status", value="🟢 **Connected (24/7)**", inline=True)
            embed.add_field(name="Current Channel", value=vc.channel.name, inline=True)
            latency_ms = round(vc.latency * 1000, 1) if hasattr(vc, "latency") else "N/A"
            embed.add_field(name="Voice Latency", value=f"{latency_ms} ms", inline=True)
            embed.add_field(name="Bitrate", value=f"{vc.channel.bitrate // 1000} kbps" if hasattr(vc.channel, "bitrate") else "N/A", inline=True)
        else:
            embed.add_field(name="Status", value="⚪ **Disconnected**", inline=True)
            embed.add_field(name="Action", value="Use `/join` to connect the bot to voice.", inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Voice(bot))
