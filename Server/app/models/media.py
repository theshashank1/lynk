from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, SQLModel


class Video(SQLModel, table=True):  # type: ignore[call-arg]
    id: str = Field(primary_key=True)  # UUID primary key
    user_id: str = Field(foreign_key="user.uid")  # Reference to Users table
    title: str = Field(nullable=False, max_length=100)  # Media title
    description: Optional[str] = None  # Media description
    media_url: str = Field(nullable=False)  # URL of the media
    thumbnail_url: Optional[str] = None  # URL of the thumbnail
    media_type: str = Field(nullable=False, max_length=20)  # Type (e.g., video, audio)
    status: str = Field(default="public", max_length=20)  # Status of the media
    tags: Optional[List[str]] = Field(
        default=None, sa_column_kwargs={"type_": "ARRAY(TEXT)"}
    )  # Array of tags
    views: int = Field(default=0)  # View count
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Creation timestamp
    updated_at: Optional[datetime] = Field(
        default=None, sa_column_kwargs={"onupdate": datetime.utcnow}
    )  # Update timestamp

    class Config:
        orm_mode = True  # Enables ORM compatibility
