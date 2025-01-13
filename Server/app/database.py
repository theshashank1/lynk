import os
from typing import Generator

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

# Load environment variables from a .env file
load_dotenv()

# Fetch environment variables with validation

DATABASE_URL = os.getenv("DB_URL")

# Validate that essential environment variables are set
if not DATABASE_URL:
    raise ValueError("One or more essential environment variables are not set.")

# Add error handling and connection pooling settings
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    echo=False,  # Set to True for SQL query logging
)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    raise ConnectionError(f"Failed to connect to the database: {e}")


# Session maker as context manager
def get_session() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


# Initialize tables
def init_db():
    SQLModel.metadata.create_all(engine)


# Example usage of init_db function
if __name__ == "__main__":
    init_db()
