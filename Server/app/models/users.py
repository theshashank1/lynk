from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):  # type: ignore[call-arg]
    id: str = Field(primary_key=True)
    username: str = Field(max_length=50, unique=True)
    hashed_password: str = Field(nullable=False)
    email: str = Field(max_length=100, unique=True)
    account_status: str = Field(default="active", max_length=20)
    is_verified: bool = Field(default=False)
    last_login_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(
        default=None, sa_column_kwargs={"onupdate": datetime.utcnow}
    )

    class Config:
        orm_mode = True  # This is the updated way to declare orm_mode
