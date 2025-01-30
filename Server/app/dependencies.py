from fastapi import Request
from supabase import Client


def get_supabase_client(request: Request) -> Client:
    """
    Retrieves the Supabase client from the app's state.
    """
    return request.app.state.supabase
