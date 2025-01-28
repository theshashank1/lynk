from enum import Enum

from pydantic import BaseModel


class Provider(str, Enum):

    email = "Email"
    google = "Google"
    facebook = "Facebook"


class Signup(BaseModel):
    email: str
    password: str
    username: str | None = None


class SignupResponse(BaseModel):
    user_id: str


class SigninResponse(BaseModel):
    user_id: str
    access_token: str
