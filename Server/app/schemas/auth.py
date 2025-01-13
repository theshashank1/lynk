from pydantic import BaseModel


class Signup(BaseModel):
    email: str
    password: str
    username: str | None = None


class SignupResponse(BaseModel):
    user_id: str


class SigninResponse(BaseModel):
    user_id: str
    access_token: str
