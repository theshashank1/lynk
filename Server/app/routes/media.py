# At the top of your file, add this comment to disable specific flake8 warnings:
# flake8: noqa: F401, B008, E722

import os
from datetime import datetime
from typing import Annotated

from database import Session, get_db_session
from dependencies import get_supabase_client
from fastapi import (  # noqa: F401
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from models import media
from schemas.media import VideoUpload
from utils.aws import get_aws_client, get_aws_session
from utils.generator import generate_unique_id
from utils.supabase import Client, get_user

# Rest of your original code remains exactly the same...

router = APIRouter(prefix="/media", tags=["Media"])

VALID_VIDEO_EXTENSIONS = {".mp4", ".mpg", ".mkv"}
VALID_VIDEO_MIME_TYPES = {"video/mp4", "video/mpeg", "video/x-matroska"}

VALID_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}
VALID_IMAGE_MIME_TYPES = {"image/png", "image/jpeg"}

SessionDep = Annotated[Session, Depends(get_db_session)]
SupabaseDep = Annotated[Client, Depends(get_supabase_client)]


@router.post("/upload")
async def upload_video(
    video_file: UploadFile = File(..., description="Video file (mp4/mpg/mkv)"),
    thumbnail_file: UploadFile = File(
        ..., description="Thumbnail image (png/jpg/jpeg)"
    ),
    session: SessionDep = Depends(get_db_session),
    supabase: SupabaseDep = Depends(get_supabase_client),
    metadata: VideoUpload = Depends(VideoUpload.as_form),
):  # type: ignore[call-arg]
    user = get_user(supabase)

    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Validate files
    video_ext = os.path.splitext(video_file.filename)[1].lower()
    if (
        video_ext not in VALID_VIDEO_EXTENSIONS
        or video_file.content_type not in VALID_VIDEO_MIME_TYPES
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid video format. Supported formats: MP4, MPG, MKV",
        )

    thumb_ext = os.path.splitext(thumbnail_file.filename)[1].lower()
    if (
        thumb_ext not in VALID_IMAGE_EXTENSIONS
        or thumbnail_file.content_type not in VALID_IMAGE_MIME_TYPES
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid thumbnail format. Supported formats: PNG, JPG, JPEG",
        )

    # Setup AWS
    s3 = get_aws_client(get_aws_session(), "s3")
    bucket = os.getenv("AWS_BUCKET_NAME")
    media_key = generate_unique_id(length=8)

    # Upload files
    try:
        s3.upload_fileobj(
            video_file.file,
            bucket,
            f"media/videos/{media_key}{video_ext}",
            ExtraArgs={"ContentType": video_file.content_type},
        )
        s3.upload_fileobj(
            thumbnail_file.file,
            bucket,
            f"media/thumbnails/{media_key}{thumb_ext}",
            ExtraArgs={"ContentType": thumbnail_file.content_type},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload files: {str(e)}")

    # Generate URLs
    video_url = f"https://{bucket}.s3.amazonaws.com/media/videos/{media_key}{video_ext}"
    thumbnail_url = (
        f"https://{bucket}.s3.amazonaws.com/media/thumbnails/{media_key}{thumb_ext}"
    )

    # Create and save video record
    try:
        video = media.Video(
            id=media_key,
            user_id=user.id,
            title=metadata.title
            or os.path.splitext(video_file.filename)[
                0
            ],  # Use filename if no title provided
            description=metadata.description,
            media_url=video_url,
            thumbnail_url=thumbnail_url,
            media_type=metadata.media_type.value,  # Use .value for enum
            status=metadata.status.value,  # Use .value for enum
            tags=metadata.tags,
            views=0,
            created_at=datetime.utcnow(),
            updated_at=None,
        )

        session.add(video)
        session.commit()
        session.refresh(video)

        return {
            "id": video.id,
            "title": video.title,
            "video_url": video_url,
            "thumbnail_url": thumbnail_url,
            "status": video.status,
        }

    except Exception as e:
        # Try to clean up uploaded files if database operation fails
        try:
            s3.delete_object(Bucket=bucket, Key=f"media/videos/{media_key}{video_ext}")
            s3.delete_object(
                Bucket=bucket, Key=f"media/thumbnails/{media_key}{thumb_ext}"
            )
        except:
            pass
        raise HTTPException(
            status_code=500, detail=f"Failed to save video metadata: {str(e)}"
        )
