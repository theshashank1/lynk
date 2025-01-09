import os

from fastapi import APIRouter, HTTPException
from supabase import Client, create_client

from ..schema.auth import Signup

router = APIRouter(tags=["Authentication"])

url: str = os.environ.get("SUPABASE_URL") or ""
key: str = os.environ.get("SUPABASE_ANON_KEY") or ""

print(url, key)
supabase: Client = create_client(url, key)


@router.post("/signup")
async def signup(data: Signup, provider: str = "Email"):
    if provider == "Email":
        if not data.email or not data.password:
            raise HTTPException(
                status_code=400, detail="Email and password are required"
            )

        # Sign up the user (Supabase will hash the password internally):
        response = supabase.auth.sign_up(
            {"email": data.email, "password": data.password}
        )

        # Check for errors during sign-up:
        if not response.get("user"):
            raise HTTPException(status_code=400, detail="Sign-up failed")

        return {"user_id": response["user"]["id"]}
    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")
