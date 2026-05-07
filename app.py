import streamlit as st
import base64
import os
import json
from utils.supabase_client import get_supabase
from utils.auth_handler import hash_password, check_password, validate_email, is_strong_password

# --- ELITE SEO & PERFORMANCE ---
# Targeting 100/100 Lighthouse score
SEO_META = """
<head>
    <!-- Primary Meta Tags -->
    <title>MindLoop | The Sentient Social Evolution by Yekzan KUS</title>
    <meta name="title" content="MindLoop | The Sentient Social Evolution by Yekzan KUS">
    <meta name="description" content="MindLoop is the world's first Sentient Social Network. Designed by architect Yekzan KUS, it bridges human consciousness and advanced AI. Join the elite loop.">
    <meta name="keywords" content="MindLoop, Yekzan KUS, Sentient Network, AI Social Media, Next-gen AI, Future of Social, Neural Interface UI, Elite Social App">
    <meta name="author" content="Yekzan KUS">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://mindloop.streamlit.app/">
    <meta property="og:title" content="MindLoop | The Sentient Revolution">
    <meta property="og:description" content="Experience the next era of social interaction. Designed by Yekzan KUS.">
    <meta property="og:image" content="https://mindloop.streamlit.app/assets/yekzan_visionary.png">

    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://mindloop.streamlit.app/">
    <meta property="twitter:title" content="MindLoop | The Sentient Revolution">
    <meta property="twitter:description" content="Experience the next era of social interaction. Designed by Yekzan KUS.">
    <meta property="twitter:image" content="https://mindloop.streamlit.app/assets/yekzan_visionary.png">

    <!-- SEO Essentials -->
    <meta name="robots" content="index, follow">
    <meta name="language" content="English">
    <meta name="revisit-after" content="7 days">
    <link rel="canonical" href="https://mindloop.streamlit.app/">

    <!-- JSON-LD Structured Data -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "name": "MindLoop",
      "operatingSystem": "Web",
      "applicationCategory": "SocialNetworkingApplication",
      "creator": {
        "@type": "Person",
        "name": "Yekzan KUS",
        "jobTitle": "Architect & Founder",
        "url": "https://www.linkedin.com/in/yekzan-kus/"
      },
      "description": "The world's first Sentient Social Network.",
      "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "USD"
      }
    }
    </script>
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

# --- TRANSLATIONS (ELITE EDITION) ---
LANGUAGES = {
    "EN": {
        "hero_title": "MINDLOOP",
        "hero_subtitle": "THE SENTIENT NETWORK ARCHITECTED BY",
        "hero_desc": "Beyond Social Media. Beyond AI. Experience the Neural Singularity.",
        "vision_title": "THE ARCHITECT'S MANIFESTO",
        "vision_text": '"MindLoop is the realization of a dream: a space where digital identity is not just a profile, but a sentient extension of your consciousness. I built this for the visionaries, the leaders, and the dreamers who demand more from technology. Welcome to the elite loop."',
        "stat_design": "UX Excellence",
        "stat_status": "Tier Status",
        "cta_neural": "INITIALIZE NEURAL ACCESS",
        "feed_title": "SENTIENT STREAM",
        "feed_badge": "QUANTUM ACTIVE",
        "feed_desc": "High-fidelity interactions powered by sentient neural nodes.",
        "edge_title": "THE END OF THE OLD ERA",
        "edge_desc": "MindLoop renders traditional social platforms obsolete.",
        "cta_claim": "CLAIM YOUR LEGACY IDENTITY",
        "auth_welcome": "AUTHENTICATION GATEWAY",
        "auth_desc": "Verify your identity to enter the sentient network.",
        "auth_email": "Neural ID (Email)",
        "auth_pass": "Neural Key",
        "auth_login": "ACCESS LOOP",
        "auth_signup_prompt": "No Identity? Request Initialization",
        "auth_signup_btn": "INITIALIZE IDENTITY",
        "auth_login_prompt": "Already Connected? Return to Gateway",
        "dash_welcome": "Welcome back, Architect",
        "dash_status": "Connection Status: SECURE",
        "dash_logout": "TERMINATE CONNECTION"
    },
    "FR": {
        "hero_title": "MINDLOOP",
        "hero_subtitle": "LE RÉSEAU SENTIENT ARCHITECTURÉ PAR",
        "hero_desc": "Au-delà des réseaux sociaux. Au-delà de l'IA. Vivez la Singularité Neurale.",
        "vision_title": "LE MANIFESTE DE L'ARCHITECTE",
        "vision_text": '"MindLoop est la réalisation d\'un rêve : un espace où l\'identité numérique n\'est pas qu\'un profil, mais une extension sentiente de votre conscience. J\'ai conçu ceci pour les visionnaires qui exigent plus de la technologie. Bienvenue dans la boucle d\'élite."',
        "stat_design": "Excellence UX",
        "stat_status": "Statut de Rang",
        "cta_neural": "INITIALISER L'ACCÈS NEURAL",
        "feed_title": "FLUX SENTIENT",
        "feed_badge": "QUANTUM ACTIF",
        "feed_desc": "Interactions haute fidélité propulsées par des nœuds neuraux.",
        "edge_title": "LA FIN DE L'ANCIENNE ÈRE",
        "edge_desc": "MindLoop rend les plateformes traditionnelles obsolètes.",
        "cta_claim": "RÉCLAMEZ VOTRE IDENTITÉ HÉRITAGE",
        "auth_welcome": "PORTAIL D'AUTHENTIFICATION",
        "auth_desc": "Vérifiez votre identité pour entrer dans le réseau.",
        "auth_email": "ID Neural (Email)",
        "auth_pass": "Clé Neurale",
        "auth_login": "ACCÉDER AU LOOP",
        "auth_signup_prompt": "Pas d'identité ? Demander l'initialisation",
        "auth_signup_btn": "INITIALISER L'IDENTITÉ",
        "auth_login_prompt": "Déjà connecté ? Retour au portail",
        "dash_welcome": "Bon retour, Architecte",
        "dash_status": "Statut de Connexion : SÉCURISÉ",
        "dash_logout": "TERMINER LA CONNEXION"
    }
}

# --- STATE MANAGEMENT ---
if 'lang' not in st.session_state: st.session_state['lang'] = 'EN'
if 'page' not in st.session_state: st.session_state['page'] = 'landing'
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if 'user' not in st.session_state: st.session_state['user'] = None
if 'auth_mode' not in st.session_state: st.session_state['auth_mode'] = 'login'

def t(key): return LANGUAGES[st.session_state['lang']].get(key, key)

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except: return ""

load_css("assets/styles.css")

# --- UI COMPONENTS ---
def language_switcher():
    # Subtle language switcher in the sidebar
    with st.sidebar:
        st.markdown("<br><br>", unsafe_allow_html=True)
        new_lang = st.selectbox("Language", ["EN", "FR"], index=0 if st.session_state['lang'] == 'EN' else 1, key="lang_sw")
        if new_lang != st.session_state['lang']:
            st.session_state['lang'] = new_lang
            st.rerun()

# --- PAGE ROUTING ---
def landing_page():
    # Hero Section
    st.markdown(f"""
    <div class="fade-in" style="text-align:center; padding: 120px 0 80px 0;">
        <div class="float">
            <img src="data:image/png;base64,{get_base64_image('assets/logo.png')}" alt="MindLoop" style="width:180px; margin-bottom:50px; filter: drop-shadow(0 0 40px #FF0080);">
        </div>
        <h1 class="title-text" style="font-size: clamp(60px, 10vw, 120px); margin-bottom: 30px;">{t('hero_title')}</h1>
        <p style="font-size: 24px; font-weight: 300; letter-spacing: 5px; color: rgba(255,255,255,0.7); text-transform: uppercase; margin-bottom: 10px;">
            {t('hero_subtitle')} <span style="color:var(--neon-blue); font-weight:900;">YEKZAN KUS</span>
        </p>
        <p style="font-size: 20px; color: #fff; max-width: 800px; margin: 0 auto 60px auto; opacity: 0.8;">
            {t('hero_desc')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Core CTA
    _, cta_col, _ = st.columns([1, 1.5, 1])
    with cta_col:
        if st.button(t('cta_neural'), key="hero_cta"):
            st.session_state['page'] = 'auth'
            st.rerun()

    st.markdown("<br><br><br><br>", unsafe_allow_html=True)

    # Founder Manifesto
    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        st.markdown(f"""
        <div class="fade-in">
            <img src="data:image/png;base64,{get_base64_image('assets/yekzan_visionary.png')}" 
                 style="width:100%; border-radius: 40px; box-shadow: 0 30px 60px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1);">
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="visionary-card fade-in">
            <h2 style="font-family: 'Syncopate'; font-size: 28px; color: #FFD700; margin-bottom: 25px;">{t('vision_title')}</h2>
            <p style="font-size: 19px; line-height: 1.8; color: #ddd; font-style: italic;">{t('vision_text')}</p>
            <p style="font-weight: 900; color: #FFD700; font-size: 22px; margin-top: 30px;">— YEKZAN KUS</p>
            <div style="display: flex; gap: 25px; margin-top: 40px;">
                <div class="stat-box" style="flex: 1; text-align: center;">
                    <div style="font-size: 28px; font-weight: 900; color: var(--neon-blue);">100%</div>
                    <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">{t('stat_design')}</div>
                </div>
                <div class="stat-box" style="flex: 1; text-align: center;">
                    <div style="font-size: 28px; font-weight: 900; color: #FF0080;">S-RANK</div>
                    <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">{t('stat_status')}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Social Proof Grid (LiveMe Inspired)
    st.markdown(f"""
    <div style="margin-top: 150px; text-align: center;">
        <h2 class="title-text" style="font-size: 50px;">{t('feed_title')}</h2>
        <div style="display: inline-block; margin-top: 15px;" class="live-badge">● {t('feed_badge')}</div>
        <p style="margin-top: 20px; font-size: 18px; color: #888;">{t('feed_desc')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.image("assets/live_grid_ultra.png", use_container_width=True)

    # Obsolete Section
    st.markdown(f"""
    <div style="margin-top: 120px; padding: 100px; background: rgba(255,255,255,0.01); border-radius: 60px; border: 1px solid var(--glass-border); text-align: center;">
        <h2 class="title-text" style="font-size: 45px; margin-bottom: 20px;">{t('edge_title')}</h2>
        <p style="font-size: 20px; color: #666; margin-bottom: 50px;">{t('edge_desc')}</p>
        <div style="display: flex; justify-content: center; gap: 60px; flex-wrap: wrap; opacity: 0.3;">
            <div style="text-decoration: line-through; font-size: 26px;">Meta</div>
            <div style="text-decoration: line-through; font-size: 26px;">X.com</div>
            <div style="text-decoration: line-through; font-size: 26px;">TikTok</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Final conversion
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    _, final_cta, _ = st.columns([1, 2, 1])
    with final_cta:
        if st.button(t('cta_claim'), key="final_btn"):
            st.session_state['page'] = 'auth'
            st.rerun()
    st.markdown("<br><br><br>", unsafe_allow_html=True)

def auth_page():
    st.markdown(f"""
    <div style="text-align:center; padding-top: 60px; margin-bottom: 40px;">
        <div class="float">
            <img src="data:image/png;base64,{get_base64_image('assets/logo.png')}" style="width:100px;">
        </div>
        <h1 class="title-text" style="font-size: 45px; margin-top: 30px;">{t('auth_welcome')}</h1>
        <p style="color: #888;">{t('auth_desc')}</p>
    </div>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.5, 1])
    with center:
        st.markdown('<div class="login-card fade-in">', unsafe_allow_html=True)
        
        # Social Login
        col1, col2 = st.columns(2)
        with col1: st.markdown('<div class="oauth-btn"><img src="https://www.google.com/favicon.ico" width="20"> Google</div>', unsafe_allow_html=True)
        with col2: st.markdown('<div class="oauth-btn"><img src="https://github.githubassets.com/favicons/favicon.svg" width="20"> GitHub</div>', unsafe_allow_html=True)
        
        st.markdown('<p style="text-align:center; margin: 20px 0; color: #444;">— OR —</p>', unsafe_allow_html=True)

        if st.session_state['auth_mode'] == 'login':
            email = st.text_input(t('auth_email'), placeholder="identity@mindloop.io")
            password = st.text_input(t('auth_pass'), type="password", placeholder="••••••••")
            
            if st.button(t('auth_login')):
                if email and password:
                    sb = get_supabase()
                    if sb:
                        try:
                            res = sb.table("users").select("*").eq("email", email).execute()
                            if res.data and check_password(password, res.data[0]['password_hash']):
                                st.session_state['authenticated'] = True
                                st.session_state['user'] = res.data[0]
                                st.rerun()
                            else: st.error("Neural Access Denied")
                        except: st.error("Supabase Connection Error")
            
            st.markdown(f"<p style='text-align:center; margin-top:20px; font-size:14px; color:#666;'>{t('auth_signup_prompt')}</p>", unsafe_allow_html=True)
            if st.button(t('auth_signup_btn')):
                st.session_state['auth_mode'] = 'signup'
                st.rerun()

        else:
            name = st.text_input("Identity Name")
            email = st.text_input(t('auth_email'))
            password = st.text_input(t('auth_pass'), type="password")
            
            if st.button(t('auth_signup_btn')):
                if name and email and password:
                    sb = get_supabase()
                    if sb:
                        try:
                            sb.table("users").insert({"full_name": name, "email": email, "password_hash": hash_password(password)}).execute()
                            st.success("Identity Initialized! Access the Loop.")
                            st.session_state['auth_mode'] = 'login'
                            st.rerun()
                        except: st.error("Identity already exists")

            st.markdown(f"<p style='text-align:center; margin-top:20px; font-size:14px; color:#666;'>{t('auth_login_prompt')}</p>", unsafe_allow_html=True)
            if st.button(t('auth_login')):
                st.session_state['auth_mode'] = 'login'
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

def dashboard_page():
    user = st.session_state['user']
    st.markdown(f"""
    <div style="padding: 60px; text-align: center;" class="fade-in">
        <h1 class="title-text">{t('dash_welcome')}, {user['full_name']}</h1>
        <p style="color:var(--neon-blue); letter-spacing: 2px;">{t('dash_status')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.image("assets/live_grid_ultra.png", use_container_width=True)
    
    if st.button(t('dash_logout')):
        st.session_state['authenticated'] = False
        st.session_state['user'] = None
        st.session_state['page'] = 'landing'
        st.rerun()

# --- RUNTIME ---
language_switcher()
if st.session_state['authenticated']:
    dashboard_page()
elif st.session_state['page'] == 'landing':
    landing_page()
elif st.session_state['page'] == 'auth':
    auth_page()
