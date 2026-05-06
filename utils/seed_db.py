from supabase_client import get_supabase
from auth_handler import hash_password
import uuid

def seed():
    supabase = get_supabase()
    if not supabase:
        print("❌ Supabase non configuré.")
        return

    print("🚀 Initialisation de la base de données...")
    
    # Création d'un utilisateur admin de test
    email = "admin@mindloop.io"
    password = "mindloop_premium_2024"
    
    try:
        # Vérifier si l'utilisateur existe
        res = supabase.table("users").select("*").eq("email", email).execute()
        if not res.data:
            data = {
                "id": str(uuid.uuid4()),
                "email": email,
                "password_hash": hash_password(password),
                "full_name": "MindLoop Admin"
            }
            supabase.table("users").insert(data).execute()
            print(f"✅ Utilisateur admin créé : {email} / {password}")
        else:
            print("ℹ️ L'utilisateur admin existe déjà.")
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")

if __name__ == "__main__":
    seed()
