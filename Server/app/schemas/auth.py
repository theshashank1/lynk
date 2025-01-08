from pydantic import BaseModel, EmailStr


class Signup(BaseModel):
    email: EmailStr
    password: str
