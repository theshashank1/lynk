import os
from typing import Annotated  # Add this import

from database import get_session
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from models import users
from passlib.hash import bcrypt
from schemas.auth import Provider, SigninResponse, Signup, SignupResponse
from sqlmodel import Session
from supabase import Client, create_client
from utils.uuid import generate_username

router = APIRouter(tags=["Authentication"])

load_dotenv()

url: str = os.environ.get("SUPABASE_URL") or ""
key: str = os.environ.get("SUPABASE_ANON_KEY") or ""

supabase: Client = create_client(url, key)

# Define the dependency type
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/signup", response_model=SignupResponse)
async def signup(
    data: Signup, provider: Provider = Provider.email, session: SessionDep = None
):
    if provider == "Email":
        if not data.email or not data.password:
            raise HTTPException(
                status_code=400, detail="Email and password are required"
            )

        try:
            response = supabase.auth.sign_up(
                {"email": data.email, "password": data.password}
            )

            if not response.user:
                raise HTTPException(status_code=400, detail="Sign-up failed")

            hashed_password = bcrypt.hash(data.password)

            user = users.User(
                uid=response.user.id,
                email=data.email,
                username=data.username or generate_username(data.email),
                hashed_password=hashed_password,
                is_verified=response.user.email_confirmed_at is not None,
                created_at=response.user.created_at,
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            return SignupResponse(user_id=response.user.id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")


@router.post("/signin", response_model=SigninResponse)
async def signin(data: Signup, provider: Provider = Provider.email):
    if provider == "Email":
        if not data.email or not data.password:
            raise HTTPException(
                status_code=400, detail="Email and password are required"
            )

        try:
            response = supabase.auth.sign_in_with_password(
                {"email": data.email, "password": data.password}
            )

            if not response.user:
                raise HTTPException(status_code=401, detail="Invalid credentials")

            return SigninResponse(
                user_id=response.user.id, access_token=response.session.access_token
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")
