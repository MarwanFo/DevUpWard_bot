import logging
import random
import discord
from discord import app_commands
from discord.ext import commands
from sqlmodel import select
from app.bot.utils import create_base_embed, get_brand_color, get_setting
from app.core.config import settings
from app.core.database import async_session_factory
from app.models.inbox import ContactSubmission
from app.models.quote import TeamQuote

logger = logging.getLogger("cogs.hospitality")


class ContactModal(discord.ui.Modal, title="Contact DevUpward Squad"):
    sender_name = discord.ui.TextInput(
        label="Your Name",
        placeholder="e.g. Alex Smith",
        min_length=2,
        max_length=100,
        required=True,
    )
    email = discord.ui.TextInput(
        label="Email or Contact Handle",
        placeholder="alex@company.com or @alex_smith",
        min_length=3,
        max_length=120,
        required=True,
    )
    organization = discord.ui.TextInput(
        label="Company / Event / Hackathon",
        placeholder="e.g. TechStars, HackMIT, Angel Sponsor (Optional)",
        max_length=120,
        required=False,
    )
    message = discord.ui.TextInput(
        label="Message or Collaboration Proposal",
        style=discord.TextStyle.paragraph,
        placeholder="Tell us about the opportunity, invitation, or project you'd like to discuss...",
        min_length=10,
        max_length=1500,
        required=True,
    )

    def __init__(self, bot: commands.Bot, brand_color: discord.Color):
        super().__init__()
        self.bot = bot
        self.brand_color = brand_color

    async def on_submit(self, interaction: discord.Interaction):
        # 1. Save to database
        submission = ContactSubmission(
            sender_name=self.sender_name.value.strip(),
            email=self.email.value.strip(),
            organization=self.organization.value.strip() if self.organization.value else None,
            discord_tag=str(interaction.user),
            message=self.message.value.strip(),
            status="unread",
        )

        async with async_session_factory() as session:
            session.add(submission)
            await session.commit()
            await session.refresh(submission)

        # 2. Confirm to user ephemerally
        confirm_embed = create_base_embed(
            title="✅ Message Delivered to DevUpward!",
            description="Thank you for getting in touch. Your message has been routed to our core team inbox. We'll follow up with you promptly.",
            color=discord.Color.green(),
        )
        confirm_embed.add_field(name="Reference ID", value=f"#{submission.id}", inline=True)
        await interaction.response.send_message(embed=confirm_embed, ephemeral=True)

        # 3. Dispatch alert to internal team channel
        inbox_channel_id = await get_setting("inbox_channel_id", settings.DISCORD_INBOX_CHANNEL_ID or "")
        if inbox_channel_id and inbox_channel_id.isdigit():
            try:
                channel = self.bot.get_channel(int(inbox_channel_id))
                if not channel:
                    channel = await self.bot.fetch_channel(int(inbox_channel_id))

                if isinstance(channel, discord.TextChannel):
                    alert_embed = create_base_embed(
                        title="📬 New Visitor Inquiry Submitted via /contact",
                        description=submission.message,
                        color=self.brand_color,
                    )
                    alert_embed.add_field(name="From", value=submission.sender_name, inline=True)
                    alert_embed.add_field(name="Contact", value=submission.email or "N/A", inline=True)
                    if submission.organization:
                        alert_embed.add_field(name="Organization", value=submission.organization, inline=True)
                    alert_embed.add_field(name="Discord User", value=interaction.user.mention, inline=True)
                    alert_embed.set_footer(text=f"Inquiry #{submission.id} • Showcase Bot")

                    await channel.send(content="🔔 **New incoming collaboration inquiry!**", embed=alert_embed)
            except Exception as e:
                logger.error(f"Failed to dispatch inbox alert to channel {inbox_channel_id}: {e}")


class HospitalityCog(commands.Cog, name="Hospitality"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Automated VIP onboarding greeting new visitors."""
        if member.bot:
            return

        welcome_channel_id = await get_setting("welcome_channel_id", settings.DISCORD_WELCOME_CHANNEL_ID or "")
        if not welcome_channel_id or not welcome_channel_id.isdigit():
            return

        try:
            channel = member.guild.get_channel(int(welcome_channel_id))
            if not channel:
                channel = await self.bot.fetch_channel(int(welcome_channel_id))

            if isinstance(channel, discord.TextChannel):
                team_name = await get_setting("team_name", "DevUpward")
                brand_color = await get_brand_color()

                embed = create_base_embed(
                    title=f"👋 Welcome to the {team_name} Server, {member.display_name}!",
                    description=f"Thanks for visiting our official team hub! We're an active hackathon team building products at the edge of AI and modern tech.",
                    color=brand_color,
                )
                embed.set_thumbnail(url=member.display_avatar.url)
                embed.add_field(
                    name="🧭 Quick Navigation",
                    value="• `/about` — Meet our team and read our story\n• `/team` — Interactive member directory\n• `/projects` — Browse our hackathon showroom\n• `/awards` — View our trophies & palmarès\n• `/contact` — Propose a collaboration or invite us",
                    inline=False,
                )
                await channel.send(content=f"Welcome {member.mention}! 🎉", embed=embed)
        except Exception as e:
            logger.error(f"Failed to send welcome onboarding message: {e}")

    @app_commands.command(name="contact", description="Get in touch with the team for collaborations, invitations, or inquiries.")
    async def contact_command(self, interaction: discord.Interaction):
        """Opens interactive modal contact form."""
        brand_color = await get_brand_color()
        modal = ContactModal(bot=self.bot, brand_color=brand_color)
        await interaction.response.send_modal(modal)

    @app_commands.command(name="quote", description="Get an authentic quote or inside joke from our late-night hackathon sessions.")
    async def quote_command(self, interaction: discord.Interaction):
        """Shares a random team quote or memorable moment."""
        brand_color = await get_brand_color()

        async with async_session_factory() as session:
            statement = select(TeamQuote)
            quotes = (await session.exec(statement)).all()

        if not quotes:
            await interaction.response.send_message("No team quotes recorded yet!", ephemeral=True)
            return

        selected = random.choice(quotes)
        context_str = f"\n— *{selected.context}*" if selected.context else ""

        embed = create_base_embed(
            title="💬 Hackathon War Room Quote",
            description=f"**\"{selected.quote}\"**\n\n— **{selected.author}**{context_str}",
            color=brand_color,
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(HospitalityCog(bot))
