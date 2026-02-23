import streamlit as st

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Turbomachines Pro | M1-GM",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. THÈME DARK PERSONNALISÉ (CSS) ---
st.markdown("""
    <style>
    /* 1. Fond principal et texte */
    [data-testid="stAppViewContainer"] {
        background-color: #0E1117;
        color: #FFFFFF;
    }

    /* 2. Barre latérale (Sidebar) en Dark */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }

    /* 3. Titres de navigation dans la sidebar */
    .st-emotion-cache-16idsys p {
        font-weight: bold;
        color: #58A6FF !important; /* Bleu clair électrique pour le Dark Mode */
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 1px;
    }

    /* 4. Cartes d'info et blocs (adapté au sombre) */
    .stInfo, .stSuccess, .stWarning, .stError {
        background-color: #1F2937 !important;
        border: 1px solid #30363D !important;
        color: #E6EDF3 !important;
    }

    /* 5. Footer Académique Dark */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #161B22;
        color: #8B949E;
        text-align: center;
        padding: 8px;
        font-size: 11px;
        border-top: 1px solid #30363D;
        z-index: 100;
    }

    /* 6. Style des boutons de navigation sélectionnés */
    [data-testid="stSidebarNavLink"] {
        color: #C9D1D9 !important;
    }
    [data-testid="stSidebarNavLink"][aria-current="page"] {
        background-color: #1F2937 !important;
        color: #58A6FF !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. INFOS D'IDENTIFICATION (SIDEBAR) ---
with st.sidebar:
    st.markdown("### 🎓 Identification")
    # Utilisation d'un bloc stylisé pour l'identification
    st.markdown(f"""
    <div style="background-color: #0D1117; padding: 15px; border-radius: 10px; border: 1px solid #30363D;">
        <p style="margin:0; color:#58A6FF; font-weight:bold;">Logiciel : AxialFlow </p>
        <p style="margin:0; font-size:14px;"><b>Nom :</b> FODIL Mohammed El Amine</p>
        <p style="margin:0; font-size:14px;"><b>Grade :</b> Master 1 GM</p>
        <p style="margin:0; font-size:14px;"><b>Université :</b> Univ. de Maghnia</p>
        <hr style="margin:10px 0; border-color:#30363D;">
        <p style="margin:0; font-size:12px; color:#8B949E;">📧 fodilmedam@gmail.com</p>
        <p style="margin:0; font-size:12px; color:#8B949E;">📞 0550139987</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

# --- 4. DÉFINITION DES PAGES ---
intro = st.Page("pages/1_Introduction.py", title="Introduction", icon="📖")
thermo = st.Page("pages/2_Thermodynamique.py", title="Thermodynamique", icon="🔥")
triangles = st.Page("pages/3_Triangles_de_Vitesses.py", title="Triangles de Vitesses", icon="🌀")
reaction = st.Page("pages/4_Degre_de_Reaction.py", title="Degré de Réaction", icon="⚖️")
exercices = st.Page("pages/5_Exercices_et_Corrections.py", title="Exercices & Corrections", icon="📝")

# --- 5. NAVIGATION ---
pg = st.navigation({
    "📚 Cours Compresseur Axial": [intro, thermo],
    "⚙️ Analyse Technique": [triangles, reaction],
    "📝 Évaluation": [exercices]
})

# --- 6. FOOTER ---
st.markdown("""
    <div class="footer">
        © 2026 - AxialFlow | Dr FODIL | Master 1 Génie Mécanique - Centre Universitair de Maghnia
    </div>
""", unsafe_allow_html=True)

pg.run()


