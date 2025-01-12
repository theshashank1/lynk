import os
from contextlib import contextmanager
from typing import Generator

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

# Load environment variables from .env file
load_dotenv()


database_password = os.getenv("DB_PASSWORD")

database_url = os.getenv("DATABASE_URL")
direct_url = os.getenv("DIRECT_URL")

# Add error handling and connection pooling settings
engine = create_engine(
    database_url,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    echo=False,  # Set to True for SQL query logging
)

# Use the DIRECT_URL for migrations
direct_engine = create_engine(direct_url, echo=False)


# Session maker as context manager
@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


# FastAPI dependency
def get_session() -> Generator[Session, None, None]:
    with get_db_session() as session:
        yield session


# Initialize tables
def init_db():
    SQLModel.metadata.create_all(engine)


# Migrations function (using direct URL)
def run_migrations():
    # Use direct connection for migrations
    SQLModel.metadata.create_all(direct_engine)
