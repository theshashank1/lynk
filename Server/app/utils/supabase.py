import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import HTTPException
from supabase import Client, create_client

# Load environment variables
load_dotenv()

url: Optional[str] = os.environ.get("SUPABASE_URL")
key: Optional[str] = os.environ.get("SUPABASE_ANON_KEY")

supabase: Client = create_client(url or "", key or "")


# Centralize Supabase configuration
def get_supabase_client() -> Optional[Client]:
    if not url:
        raise HTTPException(
            status_code=500,
            detail="SUPABASE_URL is not properly configured in the environment",
        )

    if not key:
        raise HTTPException(
            status_code=500,
            detail="SUPABASE_ANON_KEY is not properly configured in the environment",
        )

    return create_client(url, key)
