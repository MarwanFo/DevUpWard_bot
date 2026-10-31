from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Discord Bot Credentials
    DISCORD_BOT_TOKEN: str = ""
    DISCORD_CLIENT_ID: str = ""
    DISCORD_GUILD_ID: Optional[str] = None

    # Automated Channels
    DISCORD_WELCOME_CHANNEL_ID: Optional[str] = None
    DISCORD_INBOX_CHANNEL_ID: Optional[str] = None
    DISCORD_VOICE_CHANNEL_ID: Optional[str] = None

    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_SECRET_KEY: str = "dev_secret_key"
    ADMIN_API_KEY: str = "dev_admin_key_12345"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/showcase.db"

    # Team Branding Defaults
    TEAM_NAME: str = "DevUpward"
    TEAM_MOTTO: str = "Building the future, one hackathon at a time"
    BRAND_COLOR: str = "#5865F2"

    # Cloudinary Image Storage
    CLOUDINARY_CLOUD_NAME: Optional[str] = None
    CLOUDINARY_API_KEY: Optional[str] = None
    CLOUDINARY_API_SECRET: Optional[str] = None



settings = Settings()

