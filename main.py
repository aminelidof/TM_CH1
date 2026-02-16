import streamlit as st

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="AxialFlow Pro | M1-GM",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. THÈME DARK "PREMIUM" (CSS AMÉLIORÉ) ---
st.markdown("""
    <style>
    /* Importation d'une police moderne */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #0D1117;
    }

    /* 2. Barre latérale stylisée */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
        box-shadow: 5px 0 15px rgba(0,0,0,0.5);
    }

    /* 3. Titres des sections dans la sidebar */
    .st-emotion-cache-16idsys p {
        font-weight: 800 !important;
        color: #58A6FF !important;
        text-transform: uppercase;
        font-size: 0.75rem !important;
        letter-spacing: 1.5px;
        margin-bottom: 5px;
    }

    /* 4. Cartes d'identité et Info avec effet Glassmorphism */
    .id-card {
        background: linear-gradient(145deg, #161b22, #0d1117);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363D;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        transition: 0.3s;
    }
    .id-card:hover {
        border-color: #58A6FF;
        box-shadow: 0 4px 25px rgba(88, 166, 255, 0.2);
    }

    /* 5. Boutons de navigation */
    [data-testid="stSidebarNavLink"] {
        border-radius: 8px;
        margin: 2px 10px;
        transition: 0.2s;
    }
    [data-testid="stSidebarNavLink"]:hover {
        background-color: #21262D !important;
    }
    [data-testid="stSidebarNavLink"][aria-current="page"] {
        background: linear-gradient(90deg, #1f2937 0%, #161b22 100%) !important;
        border-left: 4px solid #58A6FF !important;
        color: #58A6FF !important;
    }

    /* 6. Footer avec effet de flou */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: rgba(22, 27, 34, 0.8);
        backdrop-filter: blur(10px);
        color: #8B949E;
        text-align: center;
        padding: 12px;
        font-size: 12px;
        border-top: 1px solid #30363D;
        z-index: 99;
    }
    
    /* 7. Amélioration des titres principaux */
    h1, h2, h3 {
        color: #F0F6FC;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. INFOS D'IDENTIFICATION (SIDEBAR OPTIMISÉE) ---
with st.sidebar:
    st.markdown("### 👤 Utilisateur")
    st.markdown(f"""
    <div class="id-card">
        <p style="margin:0; color:#58A6FF; font-size:12px; font-weight:bold; text-transform:uppercase;">Application</p>
        <p style="margin:0 0 10px 0; font-size:20px; font-weight:800; color:#F0F6FC;">AxialFlow <span style="color:#58A6FF;">Pro</span></p>
        <p style="margin:0; font-size:14px; color:#C9D1D9;"><b>👨‍🏫 Dr. FODIL M.E.A.</b></p>
        <p style="margin:0; font-size:13px; color:#8B949E;">Master 1 Génie Mécanique</p>
        <p style="margin:0; font-size:13px; color:#8B949E;">🏫 Université de Maghnia</p>
        <hr style="margin:15px 0; border-color:#30363D;">
        <div style="display:flex; flex-direction:column; gap:5px;">
            <span style="font-size:12px; color:#58A6FF;">📧 fodilmedam@gmail.com</span>
            <span style="font-size:12px; color:#58A6FF;">📞 0550139987</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.divider()

# --- 4. DÉFINITION DES PAGES (AVEC ICÔNES AMÉLIORÉES) ---
intro = st.Page("pages/1_Introduction.py", title="Concept & Bases", icon="📘")
thermo = st.Page("pages/2_Thermodynamique.py", title="Cycles & Énergie", icon="⚡")
triangles = st.Page("pages/3_Triangles_de_Vitesses.py", title="Cinématique (Triangles)", icon="📐")
reaction = st.Page("pages/4_Degre_de_Reaction.py", title="Équilibrage (Réaction)", icon="⚖️")
exercices = st.Page("pages/5_Exercices_et_Corrections.py", title="Atelier Pratique", icon="🛠️")

# --- 5. NAVIGATION ---
pg = st.navigation({
    "📖 FORMATION THÉORIQUE": [intro, thermo],
    "⚙️ ANALYSE D'INGÉNIERIE": [triangles, reaction],
    "🏁 ÉVALUATION": [exercices]
})

# --- 6. FOOTER ---
st.markdown("""
    <div class="footer">
        <b>AxialFlow Pro v2.0</b> | Développé pour le Master 1 GM | © 2026 Univ. Maghnia
    </div>
""", unsafe_allow_html=True)

# Lancer la page
pg.run()
