import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def _get_credentials():
    """
    Priority:
    1. st.secrets (Streamlit Cloud)
    2. Environment variables / .env (local)
    """
    url = ""
    key = ""

    # 1 — Streamlit Cloud secrets
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_ANON_KEY"]
    except Exception:
        pass

    # 2 — .env / env vars fallback
    if not url:
        url = os.getenv("SUPABASE_URL", "")
    if not key:
        key = os.getenv("SUPABASE_ANON_KEY", "")

    return url.strip(), key.strip()


def get_supabase() -> Client | None:
    url, key = _get_credentials()
    if not url or not key:
        return None
    try:
        return create_client(url, key)
    except Exception:
        return None


def test_connection() -> tuple[bool, str]:
    """Returns (ok, message) for diagnostics."""
    url, key = _get_credentials()
    if not url:
        return False, "SUPABASE_URL manquant"
    if not key:
        return False, "SUPABASE_ANON_KEY manquant"
    try:
        client = create_client(url, key)
        client.table("users").select("id").limit(1).execute()
        return True, "Connexion Supabase OK"
    except Exception as e:
        return False, str(e)
