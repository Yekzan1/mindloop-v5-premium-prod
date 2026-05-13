import streamlit as st
import base64
import os
from utils.supabase_client import get_supabase
from utils.auth_handler import hash_password, check_password, validate_email

# ── SEO (no <script> tags — Streamlit strips them) ──────────────────────────
SEO = """
<meta name="description" content="MindLoop — The AI-powered professional learning network. Share knowledge, collaborate, and grow with intelligent tools.">
<meta name="keywords" content="MindLoop, AI learning, professional network, knowledge sharing, collaboration, Yekzan KUS">
<meta name="author" content="Yekzan KUS">
<meta property="og:type" content="website">
<meta property="og:url" content="https://mindloop.streamlit.app/">
<meta property="og:title" content="MindLoop — Intelligence Loop">
<meta property="og:description" content="Every piece of knowledge becomes interactive with AI.">
<meta property="og:image" content="https://mindloop.streamlit.app/app/static/hero_bg.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://mindloop.streamlit.app/">
"""
st.markdown(SEO, unsafe_allow_html=True)

st.set_page_config(
    page_title="MindLoop — Intelligence Loop",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Translations ─────────────────────────────────────────────────────────────
T = {
    "EN": {
        "tagline": "Every idea becomes intelligence.",
        "hero_sub": "The AI-powered professional learning network",
        "hero_desc": "Share knowledge. Collaborate. Grow. Powered by AI that transforms every post into interactive learning.",
        "cta_primary": "Start for free →",
        "cta_secondary": "See how it works",
        "feat1_t": "AI-Enhanced Posts",
        "feat1_d": "Every post is automatically enriched — summaries, quizzes, flashcards.",
        "feat2_t": "Smart Collaboration",
        "feat2_d": "Connect with people sharing your skills and goals.",
        "feat3_t": "Skill Graph",
        "feat3_d": "Your expertise is visualized and grows with every interaction.",
        "feat4_t": "Learning Paths",
        "feat4_d": "AI recommends personalized curricula based on your activity.",
        "ai_title": "Watch AI Transform a Post",
        "ai_input": '📝 User posts: "Introduction to SQL"',
        "ai_out1": "📋 Smart Summary",
        "ai_out2": "🧠 Auto Quiz",
        "ai_out3": "🔖 Flashcards",
        "ai_out4": "🔗 Resources",
        "ai_out5": "👥 Connect with 12 SQL learners",
        "auth_title": "Join the Loop",
        "auth_sub": "Create your account in seconds",
        "login_title": "Welcome back",
        "login_sub": "Sign in to your account",
        "email": "Email address",
        "password": "Password",
        "name": "Full name",
        "btn_login": "Sign in →",
        "btn_signup": "Create account →",
        "to_signup": "No account? Create one",
        "to_login": "Already have an account? Sign in",
        "dash_hello": "Welcome back",
        "dash_subtitle": "Your intelligence loop is active",
        "post_placeholder": "Share knowledge, a course, a discovery…",
        "post_btn": "Publish & Let AI Enhance",
        "feed_title": "Intelligence Feed",
        "profile_title": "My Profile",
        "skills_title": "My Skills",
        "logout": "Sign out",
    },
    "FR": {
        "tagline": "Chaque idée devient intelligence.",
        "hero_sub": "Le réseau professionnel d'apprentissage propulsé par l'IA",
        "hero_desc": "Partagez vos connaissances. Collaborez. Évoluez. Propulsé par une IA qui transforme chaque post en apprentissage interactif.",
        "cta_primary": "Commencer gratuitement →",
        "cta_secondary": "Voir comment ça fonctionne",
        "feat1_t": "Posts enrichis par IA",
        "feat1_d": "Chaque post est enrichi automatiquement — résumés, quiz, fiches.",
        "feat2_t": "Collaboration Intelligente",
        "feat2_d": "Connectez-vous avec des personnes partageant vos compétences.",
        "feat3_t": "Graphe de Compétences",
        "feat3_d": "Votre expertise se visualise et grandit à chaque interaction.",
        "feat4_t": "Parcours d'Apprentissage",
        "feat4_d": "L'IA recommande des cursus personnalisés selon votre activité.",
        "ai_title": "L'IA transforme vos posts",
        "ai_input": '📝 Utilisateur poste : "Introduction au SQL"',
        "ai_out1": "📋 Résumé intelligent",
        "ai_out2": "🧠 Quiz automatique",
        "ai_out3": "🔖 Fiches de révision",
        "ai_out4": "🔗 Ressources",
        "ai_out5": "👥 Connecté à 12 apprenants SQL",
        "auth_title": "Rejoignez le Loop",
        "auth_sub": "Créez votre compte en quelques secondes",
        "login_title": "Bon retour",
        "login_sub": "Connectez-vous à votre compte",
        "email": "Adresse email",
        "password": "Mot de passe",
        "name": "Nom complet",
        "btn_login": "Se connecter →",
        "btn_signup": "Créer un compte →",
        "to_signup": "Pas de compte ? En créer un",
        "to_login": "Déjà un compte ? Se connecter",
        "dash_hello": "Bon retour",
        "dash_subtitle": "Votre intelligence loop est active",
        "post_placeholder": "Partagez une connaissance, un cours, une découverte…",
        "post_btn": "Publier & Enrichir avec l'IA",
        "feed_title": "Fil Intelligent",
        "profile_title": "Mon Profil",
        "skills_title": "Mes Compétences",
        "logout": "Se déconnecter",
    }
}

# ── State ─────────────────────────────────────────────────────────────────────
for k, v in [("lang","EN"),("page","landing"),("auth_mode","signup"),
              ("authenticated",False),("user",None)]:
    if k not in st.session_state:
        st.session_state[k] = v

def tr(k): return T[st.session_state.lang].get(k, k)

# ── Helpers ───────────────────────────────────────────────────────────────────
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def img_b64(path):
    try:
        with open(path,"rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

LOGO_Y   = img_b64("assets/logo_y.png")    # Original Y logo
LOGO_NEW = img_b64("assets/logo.png")       # New neural logo

load_css()

# Lang switcher (sidebar)
with st.sidebar:
    lang = st.selectbox("🌐 Language", ["EN","FR"],
                        index=0 if st.session_state.lang=="EN" else 1)
    if lang != st.session_state.lang:
        st.session_state.lang = lang
        st.rerun()

# ── LANDING PAGE ──────────────────────────────────────────────────────────────
def landing():
    logo = img_b64("assets/logo_y.png")   # Y logo
    hero = img_b64("assets/hero_bg.png")

    # Fullscreen hero
    yekzan_img = img_b64("assets/yekzan_visionary.png")

    st.markdown(f"""
    <div style="
        position:relative; min-height:100vh; display:flex; flex-direction:column;
        align-items:center; justify-content:center; text-align:center;
        padding: 80px 40px 120px;
        background: url('data:image/png;base64,{hero}') center/cover no-repeat;
    ">
        <div style="
            position:absolute; inset:0;
            background: linear-gradient(180deg, rgba(6,9,18,0.5) 0%, rgba(6,9,18,0.95) 100%);
        "></div>
        <div style="position:relative; z-index:2;">
            <!-- Y LOGO -->
            <div class="ml-float" style="margin-bottom:32px;">
                <img src="data:image/png;base64,{logo}" alt="MindLoop"
                     style="width:120px; height:120px; object-fit:contain;
                            filter: drop-shadow(0 0 30px rgba(0,245,255,0.5));">
            </div>
            <div class="ml-badge" style="margin:0 auto 24px;">⚡ AI-Powered Learning Network</div>
            <h1 class="ml-display" style="font-size:clamp(52px,8vw,96px); margin:0 0 24px;">
                {tr('tagline')}
            </h1>
            <p style="font-size:18px; color:rgba(240,244,255,0.6); margin-bottom:8px; letter-spacing:2px;">
                Designed by <span style="color:#00F5FF; font-weight:700;">Yekzan KUS</span>
            </p>
            <p style="font-size:20px; color:rgba(240,244,255,0.7); max-width:640px;
                margin:16px auto 48px; line-height:1.7;">
                {tr('hero_desc')}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CTA buttons below hero
    _, c, _ = st.columns([1,1.4,1])
    with c:
        if st.button(tr("cta_primary"), key="hero_cta"):
            st.session_state.page = "auth"
            st.session_state.auth_mode = "signup"
            st.rerun()

    # Feature grid
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:48px;">
        <div class="ml-label">WHAT MINDLOOP DOES</div>
        <h2 class="ml-display" style="font-size:42px; margin-top:16px;">
            Knowledge, Supercharged
        </h2>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4, gap="small")
    feats = [
        ("🤖","feat1_t","feat1_d"),
        ("🤝","feat2_t","feat2_d"),
        ("📊","feat3_t","feat3_d"),
        ("🎯","feat4_t","feat4_d"),
    ]
    for col, (icon, ti, di) in zip(cols, feats):
        with col:
            st.markdown(f"""
            <div class="ml-feature">
                <span class="ml-feature-icon">{icon}</span>
                <div class="ml-feature-title">{tr(ti)}</div>
                <div class="ml-feature-desc">{tr(di)}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── FOUNDER SECTION ────────────────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    fc1, fc2 = st.columns([1, 1.3], gap="large")
    with fc1:
        yekzan_img = img_b64("assets/yekzan_visionary.png")
        st.markdown(f"""
        <div style="border-radius:24px; overflow:hidden; border:1px solid rgba(0,245,255,0.15);
            box-shadow:0 0 60px rgba(0,245,255,0.07);">
            <img src="data:image/png;base64,{yekzan_img}" alt="Yekzan KUS"
                 style="width:100%; display:block;">
        </div>
        """, unsafe_allow_html=True)
    with fc2:
        st.markdown(f"""
        <div class="ml-card ml-card-glow" style="height:100%;">
            <div class="ml-badge ml-badge-violet" style="margin-bottom:20px;">FOUNDER & ARCHITECT</div>
            <h2 style="font-family:'Space Grotesk'; font-size:36px; font-weight:700;
                color:#FFFFFF; margin:0 0 8px;">Yekzan KUS</h2>
            <p style="font-size:15px; color:rgba(0,245,255,0.7); margin-bottom:24px; letter-spacing:1px;">
                Visionary · Builder · Innovator
            </p>
            <p style="font-size:16px; color:rgba(240,244,255,0.7); line-height:1.8; font-style:italic;">
                &ldquo;MindLoop is not just a platform — it&rsquo;s a new intelligence layer
                for human collaboration. Every idea you share becomes richer, smarter,
                and more connected than before.&rdquo;
            </p>
            <div style="display:flex; gap:16px; margin-top:32px;">
                <div class="ml-stat" style="flex:1;">
                    <div class="ml-stat-value" style="font-size:28px;">100%</div>
                    <div class="ml-stat-label">Free Forever</div>
                </div>
                <div class="ml-stat" style="flex:1;">
                    <div class="ml-stat-value" style="font-size:28px;">AI</div>
                    <div class="ml-stat-label">First Platform</div>
                </div>
                <div class="ml-stat" style="flex:1;">
                    <div class="ml-stat-value" style="font-size:28px;">∞</div>
                    <div class="ml-stat-label">Knowledge</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)

    # ── AI DEMO SECTION ──────────────────────────────────────────────────────
    # AI demo section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:40px;">
        <div class="ml-label">AI IN ACTION</div>
        <h2 class="ml-display" style="font-size:42px; margin-top:16px;">{tr('ai_title')}</h2>
    </div>
    """, unsafe_allow_html=True)

    ca, cb = st.columns(2, gap="large")
    with ca:
        st.markdown(f"""
        <div class="ml-card ml-card-glow" style="height:100%;">
            <div class="ml-label" style="margin-bottom:20px;">INPUT</div>
            <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06);
                border-radius:12px; padding:20px; font-size:16px; color:#fff;">
                {tr('ai_input')}
            </div>
            <div style="margin-top:20px; color:rgba(240,244,255,0.5); font-size:13px;">
                → AI processes in &lt;2s
            </div>
        </div>
        """, unsafe_allow_html=True)
    with cb:
        st.markdown(f"""
        <div class="ml-ai-card" style="height:100%;">
            <div class="ml-label" style="margin-bottom:20px;">OUTPUT</div>
            {"".join([f'<div style="background:rgba(255,255,255,0.03); border:1px solid rgba(0,245,255,0.1); border-radius:10px; padding:12px 16px; margin-bottom:10px; font-size:14px; color:#F0F4FF;">{o}</div>' for o in [tr("ai_out1"),tr("ai_out2"),tr("ai_out3"),tr("ai_out4"),tr("ai_out5")]])}
        </div>
        """, unsafe_allow_html=True)

    # Stats
    st.markdown("<br><br>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    stats = [("10K+","Learners"),("98%","Satisfaction"),("50ms","AI Response"),("∞","Knowledge")]
    for col, (val, lbl) in zip([s1,s2,s3,s4], stats):
        with col:
            st.markdown(f"""
            <div class="ml-stat">
                <div class="ml-stat-value">{val}</div>
                <div class="ml-stat-label">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    # Final CTA
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center; padding:80px 40px;
        background:linear-gradient(135deg,rgba(124,58,237,0.1) 0%,rgba(0,245,255,0.05) 100%);
        border:1px solid rgba(124,58,237,0.2); border-radius:28px; margin:0 40px 80px;">
        <h2 class="ml-display" style="font-size:48px; margin-bottom:16px;">
            Ready to loop in?
        </h2>
        <p style="font-size:18px; color:rgba(240,244,255,0.6); margin-bottom:40px;">
            Free forever. No credit card required.
        </p>
    </div>
    """, unsafe_allow_html=True)
    _, cta_col, _ = st.columns([1,1,1])
    with cta_col:
        if st.button(tr("cta_primary"), key="final_cta"):
            st.session_state.page = "auth"
            st.session_state.auth_mode = "signup"
            st.rerun()
    st.markdown("<br><br>", unsafe_allow_html=True)


# ── AUTH PAGE ─────────────────────────────────────────────────────────────────
def auth():
    mode = st.session_state.auth_mode
    title = tr("auth_title") if mode=="signup" else tr("login_title")
    sub   = tr("auth_sub")   if mode=="signup" else tr("login_sub")

    st.markdown(f"""
    <div style="text-align:center; padding:60px 20px 32px;">
        <h1 class="ml-display" style="font-size:52px;">{title}</h1>
        <p style="color:rgba(240,244,255,0.5); font-size:16px;">{sub}</p>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1,1.4,1])
    with col:
        st.markdown('<div class="ml-card-auth">', unsafe_allow_html=True)

        # OAuth
        st.markdown(f"""
        <div class="ml-oauth-btn">
            <img src="https://www.google.com/favicon.ico" width="18"> Continue with Google
        </div>
        <div class="ml-oauth-btn">
            <img src="https://github.githubassets.com/favicons/favicon.svg" width="18"> Continue with GitHub
        </div>
        <div class="ml-divider">or</div>
        """, unsafe_allow_html=True)

        if mode == "signup":
            name  = st.text_input(tr("name"), placeholder="Ada Lovelace")
            email = st.text_input(tr("email"), placeholder="ada@mindloop.io")
            pwd   = st.text_input(tr("password"), type="password", placeholder="Min. 8 characters")

            if st.button(tr("btn_signup")):
                if not (name and email and pwd):
                    st.warning("Please fill in all fields.")
                elif not validate_email(email):
                    st.error("Invalid email address.")
                elif len(pwd) < 8:
                    st.error("Password must be at least 8 characters.")
                else:
                    sb = get_supabase()
                    if sb:
                        # Check duplicate
                        try:
                            existing = sb.table("users").select("id").eq("email", email).execute()
                            if existing.data:
                                st.error("An account with this email already exists. Sign in instead.")
                            else:
                                sb.table("users").insert({
                                    "full_name": name,
                                    "email": email,
                                    "password_hash": hash_password(pwd)
                                }).execute()
                                st.success("✅ Account created! You can now sign in.")
                                st.session_state.auth_mode = "login"
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")
                    else:
                        st.error("Database unavailable. Check your .env file.")

            st.markdown(f"""<p style="text-align:center; margin-top:20px; font-size:14px;
                color:rgba(240,244,255,0.4); cursor:pointer;" onclick="">{tr("to_login")}</p>""",
                unsafe_allow_html=True)
            if st.button(tr("to_login"), key="go_login"):
                st.session_state.auth_mode = "login"
                st.rerun()

        else:  # login
            email = st.text_input(tr("email"), placeholder="ada@mindloop.io")
            pwd   = st.text_input(tr("password"), type="password", placeholder="••••••••")

            if st.button(tr("btn_login")):
                if not (email and pwd):
                    st.warning("Please fill in all fields.")
                else:
                    sb = get_supabase()
                    if sb:
                        try:
                            res = sb.table("users").select("*").eq("email", email).execute()
                            if res.data and check_password(pwd, res.data[0]["password_hash"]):
                                st.session_state.authenticated = True
                                st.session_state.user = res.data[0]
                                st.session_state.page = "dashboard"
                                st.rerun()
                            else:
                                st.error("Incorrect email or password.")
                        except Exception as e:
                            st.error(f"Connection error: {e}")
                    else:
                        st.error("Database unavailable.")

            if st.button(tr("to_signup"), key="go_signup"):
                st.session_state.auth_mode = "signup"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


# ── DASHBOARD ─────────────────────────────────────────────────────────────────
def dashboard():
    user = st.session_state.user or {}
    name = user.get("full_name", "User")

    # Sidebar nav
    with st.sidebar:
        logo_y_b64 = img_b64("assets/logo_y.png")
        st.markdown(f"""
        <div style="padding:24px 16px; border-bottom:1px solid rgba(255,255,255,0.06); margin-bottom:16px;
            display:flex; align-items:center; gap:12px;">
            <img src="data:image/png;base64,{logo_y_b64}" alt="Y"
                 style="width:36px; height:36px; object-fit:contain;
                        filter:drop-shadow(0 0 8px rgba(0,245,255,0.5));">
            <div>
                <div style="font-family:'Space Grotesk'; font-size:16px; font-weight:700; color:#F0F4FF;">MindLoop</div>
                <div style="font-size:11px; color:rgba(0,245,255,0.6);">by Yekzan KUS</div>
            </div>
        </div>
        <div style="padding:0 8px;">
            <div class="ml-nav-item active">🏠 Feed</div>
            <div class="ml-nav-item">🤖 AI Workspace</div>
            <div class="ml-nav-item">👥 Network</div>
            <div class="ml-nav-item">📊 My Skills</div>
            <div class="ml-nav-item">👤 Profile</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button(tr("logout")):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.page = "landing"
            st.rerun()

    # Main content
    st.markdown(f"""
    <div style="padding:40px 60px 0;">
        <div class="ml-badge ml-badge-live">⚡ LIVE</div>
        <h1 class="ml-display" style="font-size:42px; margin:16px 0 4px;">
            {tr('dash_hello')}, {name.split()[0]}
        </h1>
        <p style="color:rgba(240,244,255,0.5); font-size:15px; margin-bottom:40px;">
            {tr('dash_subtitle')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    feed_col, side_col = st.columns([2,1], gap="large")

    with feed_col:
        st.markdown('<div style="padding:0 60px;">', unsafe_allow_html=True)

        # Compose box
        st.markdown('<div class="ml-card ml-card-glow" style="margin-bottom:24px;">', unsafe_allow_html=True)
        new_post = st.text_area("", placeholder=tr("post_placeholder"), height=100, label_visibility="collapsed")
        if st.button(tr("post_btn")):
            if new_post.strip():
                st.success("✅ Post published! AI is enhancing it now…")
            else:
                st.warning("Write something first.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Feed
        st.markdown(f'<h3 style="font-family:Space Grotesk; margin-bottom:20px;">{tr("feed_title")}</h3>', unsafe_allow_html=True)

        demo_posts = [
            ("Alexandre M.", "Python", "Introduction to Machine Learning",
             ["📋 Auto-summary ready","🧠 5-question quiz generated","🔖 8 flashcards created"],
             ["Python","ML","Data Science"]),
            ("Sofia L.", "Design", "UX Design Principles for 2025",
             ["📋 Key points extracted","🎯 3 exercises generated","🔗 12 resources linked"],
             ["UX","Design","Product"]),
            ("James K.", "Backend", "SQL Query Optimization Guide",
             ["📋 Cheat sheet created","🧠 Quiz ready","👥 Connect with 8 learners"],
             ["SQL","Database","Backend"]),
        ]
        for author, role, title, ai_items, tags in demo_posts:
            tags_html = "".join(f'<span class="ml-skill-tag">{t}</span>' for t in tags)
            ai_html = "".join(f'<div style="font-size:13px; color:rgba(240,244,255,0.7); padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.04);">{i}</div>' for i in ai_items)
            st.markdown(f"""
            <div class="ml-post-card">
                <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                    <div style="width:40px; height:40px; border-radius:50%;
                        background:linear-gradient(135deg,#7C3AED,#00F5FF);
                        display:flex; align-items:center; justify-content:center;
                        font-weight:700; font-size:15px; color:#fff; flex-shrink:0;">
                        {author[0]}
                    </div>
                    <div>
                        <div style="font-weight:600; font-size:14px;">{author}</div>
                        <div style="font-size:12px; color:rgba(240,244,255,0.4);">{role}</div>
                    </div>
                    <div class="ml-badge ml-badge-violet" style="margin-left:auto; font-size:11px;">AI Enhanced</div>
                </div>
                <div style="font-size:16px; font-weight:600; margin-bottom:12px;">{title}</div>
                <div>{tags_html}</div>
                <div class="ml-ai-card" style="margin-top:16px; padding:16px;">
                    <div class="ml-label" style="margin-bottom:8px; font-size:10px;">AI GENERATED</div>
                    {ai_html}
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with side_col:
        st.markdown('<div style="padding:0 40px 0 0;">', unsafe_allow_html=True)

        # Profile card
        st.markdown(f"""
        <div class="ml-card ml-card-glow" style="margin-bottom:20px; text-align:center;">
            <div style="width:64px; height:64px; border-radius:50%; margin:0 auto 16px;
                background:linear-gradient(135deg,#7C3AED,#00F5FF);
                display:flex; align-items:center; justify-content:center;
                font-size:24px; font-weight:700; color:#fff;">
                {name[0].upper()}
            </div>
            <div style="font-family:'Space Grotesk'; font-weight:700; font-size:18px;">{name}</div>
            <div class="ml-badge" style="margin:12px auto 0; display:inline-flex;">
                ⚡ Active Learner
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Skills
        st.markdown(f'<h4 style="font-family:Space Grotesk; margin-bottom:16px;">{tr("skills_title")}</h4>', unsafe_allow_html=True)
        for skill, pct, color in [("Python",82,"#00F5FF"),("AI/ML",65,"#7C3AED"),("SQL",71,"#FF2D78"),("Design",48,"#10F5A0")]:
            st.markdown(f"""
            <div style="margin-bottom:16px;">
                <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:6px;">
                    <span>{skill}</span><span style="color:{color};">{pct}%</span>
                </div>
                <div class="ml-progress-bar">
                    <div class="ml-progress-fill" style="width:{pct}%; background:{color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Suggested connections
        st.markdown('<h4 style="font-family:Space Grotesk; margin:24px 0 16px;">Suggested for you</h4>', unsafe_allow_html=True)
        for person, skill in [("Maya R.","AI Researcher"),("Tom B.","Backend Dev"),("Nina L.","Data Analyst")]:
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px; padding:12px;
                background:rgba(255,255,255,0.02); border-radius:12px; margin-bottom:8px;
                border:1px solid rgba(255,255,255,0.04);">
                <div style="width:36px; height:36px; border-radius:50%;
                    background:linear-gradient(135deg,#FF2D78,#7C3AED);
                    display:flex; align-items:center; justify-content:center;
                    font-weight:700; font-size:13px; color:#fff; flex-shrink:0;">{person[0]}</div>
                <div style="flex:1;">
                    <div style="font-size:13px; font-weight:600;">{person}</div>
                    <div style="font-size:11px; color:rgba(240,244,255,0.4);">{skill}</div>
                </div>
                <div style="font-size:20px; cursor:pointer; color:rgba(240,244,255,0.3);">+</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ── ROUTER ────────────────────────────────────────────────────────────────────
if st.session_state.authenticated:
    dashboard()
elif st.session_state.page == "auth":
    auth()
else:
    landing()
