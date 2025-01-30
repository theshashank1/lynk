from datetime import datetime
from typing import List, Optional

from pydantic import field_validator
from sqlmodel import JSON, Column, Field, SQLModel


class Video(SQLModel, table=True):  # type: ignore[call-arg]
    id: str = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    title: str = Field(nullable=False, max_length=100)
    description: Optional[str] = None
    media_url: str = Field(nullable=False)
    thumbnail_url: Optional[str] = None
    media_type: str = Field(nullable=False, max_length=20)
    status: str = Field(default="public", max_length=20)
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    views: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(
        default=None, sa_column_kwargs={"onupdate": datetime.utcnow}
    )

    @field_validator("tags", mode="before")
    @classmethod
    def validate_tags(cls, v) -> List[str]:
        if isinstance(v, str):
            return []
        return v or []

    class Config:
        from_attributes = True  # New name for orm_mode in Pydantic v2
