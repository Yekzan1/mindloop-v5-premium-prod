import streamlit as st
import base64
import os
from utils.supabase_client import get_supabase
from utils.auth_handler import hash_password, check_password, validate_email, is_strong_password

# --- SEO & META TAGS ---
SEO_META = """
<head>
    <meta name="description" content="MindLoop - The world's first Sentient Social Network designed by Yekzan KUS. Experience the future of human-AI connection. Join the elite evolution.">
    <meta name="keywords" content="MindLoop, Yekzan KUS, Sentient Social Network, AI, Artificial Intelligence, Future Social Media, Elite Network, Neural Connection">
    <meta name="author" content="Yekzan KUS">
    <meta property="og:title" content="MindLoop | The Sentient Revolution">
    <meta property="og:description" content="Experience the next era of social interaction. Designed by Yekzan KUS.">
    <meta property="og:image" content="https://mindloop.streamlit.app/assets/yekzan_visionary.png">
    <meta property="og:url" content="https://mindloop.streamlit.app/">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://mindloop.streamlit.app/">
</head>
"""
st.markdown(SEO_META, unsafe_allow_html=True)

# --- CONFIGURATION ---
st.set_page_config(
    page_title="MindLoop | The Sentient Revolution",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- TRANSLATIONS ---
LANGUAGES = {
    "EN": {
        "hero_subtitle": "The Sentient Network Designed by",
        "hero_desc": "Where Artificial Intelligence meets Human Consciousness.",
        "vision_title": "THE ARCHITECT'S VISION",
        "vision_text": '"MindLoop is not just another social network. It is the manifest of a new era. I designed this ecosystem to break the barriers between the real and the digital. Here, every connection is amplified by a sentient intelligence capable of understanding the very essence of your interactions."',
        "stat_design": "Design Score",
        "stat_status": "Status",
        "cta_neural": "ESTABLISH NEURAL CONNECTION",
        "feed_title": "Sentient Feed",
        "feed_badge": "QUANTUM LIVE",
        "feed_desc": "Interact with the elite network in real-time.",
        "edge_title": "OBSOLETING THE PAST",
        "cta_claim": "CLAIM YOUR IDENTITY NOW",
        "auth_happening": "It's happening now",
        "auth_connect": "Connect to the sentient network.",
        "auth_neural_id": "Neural ID (Email)",
        "auth_key": "Access Key",
        "auth_btn": "AUTHENTICATE →",
        "auth_request": "Request Access (Sign Up)",
        "auth_init": "INITIALIZE ACCOUNT →",
        "auth_return": "Return to Terminal (Login)",
        "dash_welcome": "Welcome to the Loop",
        "dash_mode": "Sentient Mode",
        "dash_disconnect": "Disconnect from Loop"
    },
    "FR": {
        "hero_subtitle": "Le Réseau Sentient Conçu par",
        "hero_desc": "Où l'Intelligence Artificielle rencontre la Conscience Humaine.",
        "vision_title": "LA VISION DE L'ARCHITECTE",
        "vision_text": '"MindLoop n\'est pas un simple réseau social. C\'est le manifeste d\'une nouvelle ère. J\'ai conçu cet écosystème pour briser les barrières entre le réel et le digital. Ici, chaque connexion est amplifiée par une intelligence sentiente capable de comprendre l\'essence même de vos interactions."',
        "stat_design": "Score Design",
        "stat_status": "Statut",
        "cta_neural": "ÉTABLIR UNE CONNEXION NEURALE",
        "feed_title": "Flux Sentient",
        "feed_badge": "QUANTUM LIVE",
        "feed_desc": "Interagissez avec le réseau d'élite en temps réel.",
        "edge_title": "OBSOLÉSCENCE DU PASSÉ",
        "cta_claim": "RÉCLAMEZ VOTRE IDENTITÉ",
        "auth_happening": "C'est maintenant que ça se passe",
        "auth_connect": "Connectez-vous au réseau sentient.",
        "auth_neural_id": "Identifiant Neural (Email)",
        "auth_key": "Clé d'Accès",
        "auth_btn": "AUTHENTIFICATION →",
        "auth_request": "Demander l'Accès (S'inscrire)",
        "auth_init": "INITIALISER LE COMPTE →",
        "auth_return": "Retour au Terminal (Connexion)",
        "dash_welcome": "Bienvenue dans le Loop",
        "dash_mode": "Mode Sentient",
        "dash_disconnect": "Se déconnecter du Loop"
    }
}

# --- INITIALIZATION ---
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'EN'
if 'page' not in st.session_state:
    st.session_state['page'] = 'landing'
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = None
if 'auth_mode' not in st.session_state:
    st.session_state['auth_mode'] = 'login'

def t(key):
    return LANGUAGES[st.session_state['lang']].get(key, key)

# --- UTILS ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

load_css("assets/styles.css")

# --- SUBTLE LANGUAGE SELECTOR ---
st.markdown("""
    <div style="position: fixed; bottom: 20px; left: 20px; z-index: 1000; opacity: 0.3; transition: opacity 0.3s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.3'">
        <style>
            .stSelectbox [data-testid="stMarkdownContainer"] { display: none; }
        </style>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Settings")
    new_lang = st.selectbox("Language", options=["EN", "FR"], index=0 if st.session_state['lang'] == 'EN' else 1, key="lang_selector")
    if new_lang != st.session_state['lang']:
        st.session_state['lang'] = new_lang
        st.rerun()

# --- PAGES ---

def landing_page():
    # --- HERO SECTION ---
    st.markdown(f"""
    <div style="text-align:center; padding: 100px 0 60px 0;">
        <div class="float">
            <img src="data:image/png;base64,{get_base64_image('assets/logo.png')}" alt="MindLoop Logo" style="width:160px; margin-bottom:40px; filter: drop-shadow(0 0 30px #FF0080);">
        </div>
        <h1 class="title-text" style="font-size: 100px; margin-bottom: 20px;">MindLoop</h1>
        <p class="subtitle-text" style="font-size: 28px; max-width: 1000px; margin: 0 auto 50px auto; color: #fff; line-height: 1.4; letter-spacing: 1px;">
            {t('hero_subtitle')} <span style="color:var(--neon-blue); font-weight:bold; border-bottom: 2px solid var(--neon-blue);">Yekzan KUS</span>. <br>
            {t('hero_desc')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- FOUNDER SECTION (The Architect) ---
    col_a, col_b = st.columns([1, 1.2])
    with col_a:
        st.image("assets/yekzan_visionary.png", caption=f"Yekzan KUS - The Architect", use_container_width=True)
    with col_b:
        st.markdown(f"""
        <div class="visionary-card">
            <h2 style="font-family: 'Syncopate', sans-serif; color: #FFD700; font-size: 32px; margin-bottom: 20px;">{t('vision_title')}</h2>
            <p style="font-size: 18px; line-height: 1.8; color: #eee;">
                {t('vision_text')}
            </p>
            <p style="font-weight: 700; color: #FFD700; font-size: 20px; margin-top: 20px;">— Yekzan KUS</p>
            <div style="margin-top: 30px; display: flex; gap: 20px;">
                <div class="stat-box" style="flex: 1; text-align: center;">
                    <div style="font-size: 24px; font-weight: 900; color: #00DFD8;">20/20</div>
                    <div style="font-size: 12px; text-transform: uppercase; color: #888;">{t('stat_design')}</div>
                </div>
                <div class="stat-box" style="flex: 1; text-align: center;">
                    <div style="font-size: 24px; font-weight: 900; color: #FF0080;">ELITE</div>
                    <div style="font-size: 12px; text-transform: uppercase; color: #888;">{t('stat_status')}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- MAIN CTA ---
    _, col2, _ = st.columns([1,1.5,1])
    with col2:
        if st.button(t('cta_neural'), key="btn_hero_enter"):
            st.session_state['page'] = 'auth'
            st.rerun()

    # --- LIVE GRID SECTION ---
    st.markdown(f"""
    <div style="margin-top: 120px; text-align: center; margin-bottom: 60px;">
        <h2 class="title-text" style="font-size: 45px;">{t('feed_title')} <span class="live-badge">● {t('feed_badge')}</span></h2>
        <p class="subtitle-text" style="font-size: 18px;">{t('feed_desc')}</p>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced Grid
    st.image("assets/live_grid_ultra.png", use_container_width=True)

    # --- COMPETITIVE EDGE ---
    st.markdown(f"""
    <div style="margin-top: 100px; padding: 80px; background: linear-gradient(to bottom, rgba(255,255,255,0.01), rgba(0,223,216,0.02)); border-radius: 50px; border: 1px solid var(--glass-border); text-align: center;">
        <h2 class="title-text" style="font-size: 50px; margin-bottom: 40px;">{t('edge_title')}</h2>
        <div style="display: flex; justify-content: center; gap: 50px; flex-wrap: wrap;">
            <div style="opacity: 0.5; text-decoration: line-through; font-size: 24px;">Instagram</div>
            <div style="opacity: 0.5; text-decoration: line-through; font-size: 24px;">X (Twitter)</div>
            <div style="opacity: 0.5; text-decoration: line-through; font-size: 24px;">TikTok</div>
            <div style="font-size: 32px; color: var(--neon-blue); font-weight: 900; font-family: 'Syncopate';">MINDLOOP</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- FINAL CTA ---
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, final_col, _ = st.columns([1,2,1])
    with final_col:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button(t('cta_claim'), key="btn_final_beta"):
            st.session_state['page'] = 'auth'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def auth_page():
    logo_base64 = get_base64_image('assets/logo.png')
    
    st.markdown(f"""
    <div style="text-align:center; padding-top: 40px;">
        <div class="float">
            <img src="data:image/png;base64,{logo_base64}" alt="Logo" style="width:80px; margin-bottom:20px; filter: drop-shadow(0 0 15px #FF0080);">
        </div>
        <h1 class="title-text" style="font-size: 42px;">{t('auth_happening')}</h1>
        <p class="subtitle-text">{t('auth_connect')}</p>
    </div>
    """, unsafe_allow_html=True)

    _, center_col, _ = st.columns([1, 2, 1])
    
    with center_col:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # OAuth Buttons
        st.markdown(f"""
        <div style="margin-bottom: 20px;">
            <div class="oauth-btn"><img src="https://www.google.com/favicon.ico"> Google Access</div>
            <div class="oauth-btn"><img src="https://github.githubassets.com/favicons/favicon.svg"> GitHub Access</div>
        </div>
        <div style="text-align:center; color:#555; margin-bottom:20px;">— or use neural identity —</div>
        """, unsafe_allow_html=True)

        if st.session_state['auth_mode'] == 'login':
            email = st.text_input(t('auth_neural_id'), placeholder="name@domain.com")
            password = st.text_input(t('auth_key'), type="password", placeholder="••••••••")
            
            if st.button(t('auth_btn')):
                if email and password:
                    try:
                        supabase = get_supabase()
                        if supabase:
                            response = supabase.table("users").select("*").eq("email", email).execute()
                            if response.data:
                                user = response.data[0]
                                if check_password(password, user['password_hash']):
                                    st.session_state['authenticated'] = True
                                    st.session_state['user'] = user
                                    st.session_state['page'] = 'dashboard'
                                    st.rerun()
                                else:
                                    st.error("Access Denied: Invalid Key")
                            else:
                                st.error("Neural ID not found")
                        else:
                            st.error("Supabase Offline")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            if st.button(t('auth_request'), key="btn_signup_toggle"):
                st.session_state['auth_mode'] = 'signup'
                st.rerun()

        else: # Signup
            full_name = st.text_input("Full Identity Name", placeholder="Identity Name")
            email = st.text_input(t('auth_neural_id'), placeholder="name@domain.com")
            password = st.text_input("Create Access Key", type="password")
            
            if st.button(t('auth_init')):
                if email and password and full_name:
                    try:
                        supabase = get_supabase()
                        hashed = hash_password(password)
                        data = {"email": email, "password_hash": hashed, "full_name": full_name}
                        supabase.table("users").insert(data).execute()
                        st.success("Identity Initialized!")
                        st.session_state['auth_mode'] = 'login'
                        st.rerun()
                    except:
                        st.error("Identity already exists")

            if st.button(t('auth_return')):
                st.session_state['auth_mode'] = 'login'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def dashboard_page():
    user = st.session_state['user']
    st.markdown(f"""
    <div style="padding: 40px; text-align: center;">
        <h1 class="title-text">{t('dash_welcome')}, {user['full_name']}</h1>
        <p class="subtitle-text">{t('dash_mode')}: <span style="color:var(--neon-blue);">ACTIVE</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.image("assets/live_grid.png", caption="Sentient Feed Visualization", use_container_width=True)
    
    if st.button(t('dash_disconnect')):
        st.session_state['authenticated'] = False
        st.session_state['user'] = None
        st.session_state['page'] = 'landing'
        st.rerun()

# --- ROUTING ---
if st.session_state['authenticated']:
    dashboard_page()
elif st.session_state['page'] == 'landing':
    landing_page()
elif st.session_state['page'] == 'auth':
    auth_page()
