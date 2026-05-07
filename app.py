import streamlit as st
import base64
import os
from utils.supabase_client import get_supabase
from utils.auth_handler import hash_password, check_password, validate_email, is_strong_password

# --- CONFIGURATION ---
st.set_page_config(
    page_title="MindLoop | It's happening now",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- UTILS ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# --- INITIALIZATION ---
if 'page' not in st.session_state:
    st.session_state['page'] = 'landing'
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = None
if 'auth_mode' not in st.session_state:
    st.session_state['auth_mode'] = 'login'

load_css("assets/styles.css")

# --- PAGES ---

def landing_page():
    # --- HERO SECTION ---
    st.markdown(f"""
    <div style="text-align:center; padding: 100px 0 60px 0;">
        <div class="float">
            <img src="data:image/png;base64,{get_base64_image('assets/logo.png')}" style="width:160px; margin-bottom:40px; filter: drop-shadow(0 0 30px #FF0080);">
        </div>
        <h1 class="title-text" style="font-size: 100px; margin-bottom: 20px;">MindLoop</h1>
        <p class="subtitle-text" style="font-size: 28px; max-width: 1000px; margin: 0 auto 50px auto; color: #fff; line-height: 1.4; letter-spacing: 1px;">
            The Sentient Network Designed by <span style="color:var(--neon-blue); font-weight:bold; border-bottom: 2px solid var(--neon-blue);">Yekzan KUS</span>. <br>
            Where Artificial Intelligence meets Human Consciousness.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- FOUNDER SECTION (The Architect) ---
    col_a, col_b = st.columns([1, 1.2])
    with col_a:
        st.image("assets/yekzan_visionary.png", caption="Yekzan KUS - The Architect", use_container_width=True)
    with col_b:
        st.markdown(f"""
        <div class="visionary-card">
            <h2 style="font-family: 'Syncopate', sans-serif; color: #FFD700; font-size: 32px; margin-bottom: 20px;">THE ARCHITECT'S VISION</h2>
            <p style="font-size: 18px; line-height: 1.8; color: #eee;">
                "MindLoop n'est pas un simple réseau social. C'est le manifeste d'une nouvelle ère. 
                J'ai conçu cet écosystème pour briser les barrières entre le réel et le digital. 
                Ici, chaque connexion est amplifiée par une intelligence sentiente capable de comprendre 
                l'essence même de vos interactions."
            </p>
            <p style="font-weight: 700; color: #FFD700; font-size: 20px; margin-top: 20px;">— Yekzan KUS</p>
            <div style="margin-top: 30px; display: flex; gap: 20px;">
                <div class="stat-box" style="flex: 1; text-align: center;">
                    <div style="font-size: 24px; font-weight: 900; color: #00DFD8;">20/20</div>
                    <div style="font-size: 12px; text-transform: uppercase; color: #888;">Design Score</div>
                </div>
                <div class="stat-box" style="flex: 1; text-align: center;">
                    <div style="font-size: 24px; font-weight: 900; color: #FF0080;">ELITE</div>
                    <div style="font-size: 12px; text-transform: uppercase; color: #888;">Status</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- MAIN CTA ---
    _, col2, _ = st.columns([1,1.5,1])
    with col2:
        if st.button("ESTABLISH NEURAL CONNECTION", key="btn_hero_enter"):
            st.session_state['page'] = 'auth'
            st.rerun()

    # --- LIVE GRID SECTION ---
    st.markdown("""
    <div style="margin-top: 120px; text-align: center; margin-bottom: 60px;">
        <h2 class="title-text" style="font-size: 45px;">Sentient Feed <span class="live-badge">● QUANTUM LIVE</span></h2>
        <p class="subtitle-text" style="font-size: 18px;">Interact with the elite network in real-time.</p>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced Grid
    st.image("assets/live_grid_ultra.png", use_container_width=True)

    # --- COMPETITIVE EDGE ---
    st.markdown("""
    <div style="margin-top: 100px; padding: 80px; background: linear-gradient(to bottom, rgba(255,255,255,0.01), rgba(0,223,216,0.02)); border-radius: 50px; border: 1px solid var(--glass-border); text-align: center;">
        <h2 class="title-text" style="font-size: 50px; margin-bottom: 40px;">OBSOLETING THE PAST</h2>
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
        if st.button("CLAIM YOUR IDENTITY NOW", key="btn_final_beta"):
            st.session_state['page'] = 'auth'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def auth_page():
    logo_base64 = get_base64_image('assets/logo.png')
    
    st.markdown(f"""
    <div style="text-align:center; padding-top: 40px;">
        <div class="float">
            <img src="data:image/png;base64,{logo_base64}" style="width:80px; margin-bottom:20px; filter: drop-shadow(0 0 15px #FF0080);">
        </div>
        <h1 class="title-text" style="font-size: 42px;">It's happening now</h1>
        <p class="subtitle-text">Connect to the sentient network.</p>
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
            email = st.text_input("Neural ID (Email)", placeholder="name@domain.com")
            password = st.text_input("Access Key", type="password", placeholder="••••••••")
            
            if st.button("AUTHENTICATE →"):
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
            
            if st.button("Request Access (Sign Up)", key="btn_signup_toggle"):
                st.session_state['auth_mode'] = 'signup'
                st.rerun()

        else: # Signup
            full_name = st.text_input("Full Identity Name", placeholder="Identity Name")
            email = st.text_input("Neural ID (Email)", placeholder="name@domain.com")
            password = st.text_input("Create Access Key", type="password")
            
            if st.button("INITIALIZE ACCOUNT →"):
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

            if st.button("Return to Terminal (Login)"):
                st.session_state['auth_mode'] = 'login'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def dashboard_page():
    user = st.session_state['user']
    st.markdown(f"""
    <div style="padding: 40px; text-align: center;">
        <h1 class="title-text">Welcome to the Loop, {user['full_name']}</h1>
        <p class="subtitle-text">Sentient Mode: <span style="color:var(--neon-blue);">ACTIVE</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.image("assets/live_grid.png", caption="Sentient Feed Visualization", use_container_width=True)
    
    if st.button("Disconnect from Loop"):
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
