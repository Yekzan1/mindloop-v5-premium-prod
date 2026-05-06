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
    # Dynamic Hero Section
    st.markdown(f"""
    <div style="text-align:center; padding: 60px 0;">
        <div class="float">
            <img src="data:image/png;base64,{get_base64_image('assets/logo.png')}" style="width:140px; margin-bottom:30px; filter: drop-shadow(0 0 20px #FF0080);">
        </div>
        <h1 class="title-text" style="font-size: 80px;">MindLoop</h1>
        <p class="subtitle-text" style="font-size: 24px; max-width: 900px; margin: 0 auto 40px auto; color: #fff;">
            The world's first <span style="color:var(--neon-blue); font-weight:bold;">Sentient Social Network</span>. 
            Experience live interactions, intelligent matching, and a community that evolves with you.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Hero Image / Vibe
    st.image("assets/hero_vibe.png", use_container_width=True)

    # Main CTA
    _, col2, _ = st.columns([1,1.5,1])
    with col2:
        if st.button("ENTER THE EVOLUTION", key="btn_hero_enter"):
            st.session_state['page'] = 'auth'
            st.rerun()

    # Live Now Section (LiveMe Vibes)
    st.markdown("""
    <div style="margin-top: 100px; text-align: center;">
        <h2 class="title-text" style="font-size: 40px;">Live Now <span class="live-badge">● LIVE</span></h2>
        <p class="subtitle-text">Join thousands of active loops happening this second.</p>
    </div>
    """, unsafe_allow_html=True)

    # Grid of Live Profiles (Simulation)
    profiles = [
        {"name": "Nova_AI", "viewers": "12.4k", "img": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&h=500&fit=crop"},
        {"name": "PixelMaster", "viewers": "8.1k", "img": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=500&fit=crop"},
        {"name": "ZenLoop", "viewers": "5.2k", "img": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=500&fit=crop"},
        {"name": "CyberSoul", "viewers": "25.9k", "img": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=500&fit=crop"},
        {"name": "Luna_X", "viewers": "1.2k", "img": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=400&h=500&fit=crop"},
        {"name": "Drift_King", "viewers": "3.4k", "img": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=400&h=500&fit=crop"},
    ]

    cols = st.columns(3)
    for i, profile in enumerate(profiles):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="glass-card" style="padding: 0; overflow: hidden; margin-bottom: 20px;">
                <div style="position: relative; aspect-ratio: 4/5;">
                    <img src="{profile['img']}" style="width: 100%; height: 100%; object-fit: cover;">
                    <div style="position: absolute; top: 10px; left: 10px;">
                        <span class="live-badge">● {profile['viewers']}</span>
                    </div>
                    <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 20px; background: linear-gradient(to top, rgba(0,0,0,0.9), transparent);">
                        <h4 style="margin: 0; font-weight: 700; font-size: 18px;">{profile['name']}</h4>
                        <p style="margin: 0; font-size: 12px; color: #ccc;">Interactive Stream</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Trust / Stats Section
    st.markdown("""
    <div style="margin-top: 80px; padding: 60px; background: rgba(255, 255, 255, 0.02); border-radius: 40px; border: 1px solid var(--glass-border);">
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
            <div class="stat-box">
                <div class="stat-value">2.4M</div>
                <div class="stat-label">Active Loops</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">50k+</div>
                <div class="stat-label">Verified Creators</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">0.1ms</div>
                <div class="stat-label">Latency</div>
            </div>
        </div>
    </div>
    
    <div style="text-align:center; margin-top:100px;">
        <h2 class="title-text" style="font-size: 50px;">Beyond Instagram. <br>Beyond X.</h2>
        <p class="subtitle-text" style="font-size: 20px;">MindLoop isn't just an app. It's a sentient experience.</p>
    </div>
    """, unsafe_allow_html=True)

    # Final CTA
    _, final_col, _ = st.columns([1,2,1])
    with final_col:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("JOIN THE BETA ACCESS", key="btn_final_beta"):
            st.session_state['page'] = 'auth'
            st.rerun()

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
