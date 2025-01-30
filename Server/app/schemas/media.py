from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class MediaType(str, Enum):  # Note the str, Enum inheritance
    video = "Video"
    audio = "Audio"


class Visibility(str, Enum):  # Note the str, Enum inheritance
    public = "Public"
    private = "Private"


class VideoUpload(BaseModel):
    media_type: MediaType = MediaType.video
    title: Optional[str] = None
    description: Optional[str] = None
    status: Visibility = Visibility.public
    tags: List[str] = []
