import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from schemas.auth import Signup
from supabase import Client, create_client

router = APIRouter(tags=["Authentication"])

load_dotenv()

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

        # response = response.json()
        # print(type(response))
        return response

        # # Check for errors during sign-up:
        if not response["user"]:
            raise HTTPException(status_code=400, detail="Sign-up failed")

        return {"user_id": response["user"]["id"]}
    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")


@router.post("/signin")
async def signin(data: Signup, provider: str = "Email"):
    if provider == "Email":

        if not data.email or not data.password:
            raise HTTPException(
                status_code=400, detail="Email and password are required"
            )

        response = supabase.auth.sign_in_with_password(
            {"email": data.email, "password": data.password}
        )

        return response

    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")
