import logging
from typing import Optional
import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.config import settings
from app.core.database import get_session
from app.core.security import verify_admin_key
from app.models.setting import BotSetting

logger = logging.getLogger("upload")
router = APIRouter(prefix="/upload", tags=["Media & Image Uploads"])


async def get_cloudinary_config(session: AsyncSession):
    """Retrieve Cloudinary credentials from settings or database."""
    cloud_name = settings.CLOUDINARY_CLOUD_NAME
    api_key = settings.CLOUDINARY_API_KEY
    api_secret = settings.CLOUDINARY_API_SECRET

    if not (cloud_name and api_key and api_secret):
        # Fallback to database settings
        db_settings = (await session.exec(select(BotSetting))).all()
        s_map = {s.key: s.value for s in db_settings}
        cloud_name = cloud_name or s_map.get("cloudinary_cloud_name")
        api_key = api_key or s_map.get("cloudinary_api_key")
        api_secret = api_secret or s_map.get("cloudinary_api_secret")

    return cloud_name, api_key, api_secret


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    folder: str = Form(default="showcase"),
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(verify_admin_key),
):
    """Upload an image to Cloudinary and return its CDN URL."""
    # 1. Validate content type
    allowed_types = ["image/jpeg", "image/png", "image/webp", "image/gif", "image/svg+xml"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type '{file.content_type}'. Supported: JPEG, PNG, WebP, GIF, SVG.",
        )

    # 2. Check credentials
    cloud_name, api_key, api_secret = await get_cloudinary_config(session)
    if not (cloud_name and api_key and api_secret):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cloudinary is not configured. Please set CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET in .env or Settings.",
        )

    # 3. Configure Cloudinary
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True,
    )

    try:
        # Read file contents
        contents = await file.read()
        upload_result = cloudinary.uploader.upload(
            contents,
            folder=f"devupward/{folder}",
            resource_type="image",
            overwrite=True,
        )

        return {
            "success": True,
            "url": upload_result.get("secure_url"),
            "public_id": upload_result.get("public_id"),
            "format": upload_result.get("format"),
            "width": upload_result.get("width"),
            "height": upload_result.get("height"),
            "bytes": upload_result.get("bytes"),
        }
    except Exception as e:
        logger.error(f"Cloudinary upload failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cloudinary upload failed: {str(e)}",
        )
