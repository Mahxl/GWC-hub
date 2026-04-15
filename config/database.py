import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

def supabase_cf():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("error with url or key")
        
    return create_client(url, key)