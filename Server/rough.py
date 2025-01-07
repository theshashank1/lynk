import uvicorn
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from supabase import create_client, Client

import requests



app = FastAPI()


url: str = "https://atpfehtvgvpgazfehmam.supabase.co"
key: str ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF0cGZlaHR2Z3ZwZ2F6ZmVobWFtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzYwNzg2NzcsImV4cCI6MjA1MTY1NDY3N30.cx--Wd9rpovigS4ZiEUkw1NetNUq2SycrG6dEzggQZU"

supabase: Client = create_client(url, key)



# Pydantic models
class User(BaseModel):
    email: str
    password: str
    
    
    
@app.post("/auth/signup")
async def sign_up(user: User):
    try:
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })
        # if response.get("error"):
        #     raise HTTPException(status_code=400, detail=response["error"]["message"])
        return {"message": "User signed up successfully!", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
# Login route
@app.post("/login")
async def login(user: User):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        # if response.error:
        #     raise HTTPException(status_code=400, detail=response["error"]["message"])
        return {"message": "User logged in successfully!", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
# @app.get('/signup-google')
# async def signup_google():
#     try:
#         response = supabase.auth.sign_in_with_oauth({
#             "provider": 'google'
#         })
        
#         return response
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.get('/google')
async def google_auth():
    try:
        response = supabase.auth.sign_in_with_oauth({
            "provider": 'google',
            "options": {
                "redirect_to": "http://127.0.0.1:8000/profile"
            }
        })
        
        # Return the URL where the user should be redirected
        return {"url": response.url}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


        
        
@app.get("/profile/{code}")
async def get_profile(code: str = None):
    try:
        if code:
            session = await supabase.auth.exchange_code_for_session(code)
            
            return {"message": "Authentication successful", "session": session}

        user = supabase.auth.get_user()
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"message": "User profile retrieved successfully!", "user": user}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
async def test_route():
    return {"message" : "User profile retrieved successfully!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
