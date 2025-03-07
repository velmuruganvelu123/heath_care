import os
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ Supabase URL or Key is missing! Check your .env file.")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_data():
    """Fetch data from Supabase and return as a DataFrame."""
    try:
        response = supabase.table("health_care").select("*").execute()
        data = response.data if hasattr(response, "data") else []
        return pd.DataFrame(data) if data else None
    except Exception as e:
        print(f"❌ Error fetching data from Supabase: {e}")
        return None
