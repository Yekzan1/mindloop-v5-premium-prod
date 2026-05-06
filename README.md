# 🧠 MindLoop Production Setup

## 1. Supabase Configuration (OBLIGATOIRE)
1. Créez un projet sur [Supabase](https://supabase.com/).
2. Allez dans **SQL Editor** et collez le contenu de `database_schema.sql`.
3. Allez dans **Project Settings > API** :
   - Copiez `Project URL`.
   - Copiez `anon public` key.

## 2. Environment Variables
Créez un fichier `.env` à la racine avec :
```env
SUPABASE_URL=votre_url
SUPABASE_ANON_KEY=votre_cle_anon
```

## 3. Installation et Lancement
Ouvrez un terminal dans ce dossier et lancez :
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🎯 Architecture
- `app.py` : Frontend & Routage.
- `assets/` : Design system (CSS + Images).
- `utils/` : Sécurité (bcrypt) & Base de données.
- `database_schema.sql` : Structure pour Supabase.
