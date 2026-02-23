import streamlit as st

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="AxialFlow Pro | M1-GM",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. THÈME DARK HAUT CONTRASTE (CSS) ---
st.markdown("""
    <style>
    /* 1. Fond principal et Texte Global en BLANC */
    [data-testid="stAppViewContainer"] {
        background-color: #0E1117;
        color: #FFFFFF !important;
    }

    /* Forcer le texte de tous les paragraphes et labels en blanc */
    p, span, label, .stMarkdown {
        color: #FFFFFF !important;
    }

    /* 2. Titres en Bleu Électrique pour la visibilité */
    h1, h2, h3, h4, h5, h6 {
        color: #58A6FF !important;
        font-weight: 700 !important;
    }

    /* 3. Barre latérale (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #161B22 !important;
        border-right: 1px solid #30363D;
    }
    
    /* Texte de la sidebar en blanc */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #FFFFFF !important;
    }

    /* 4. Cartes d'info (Info, Success, etc.) - Fond plus clair pour le contraste */
    .stAlert {
        background-color: #1F2937 !important;
        color: #FFFFFF !important;
        border: 1px solid #58A6FF !important;
    }

    /* 5. Footer Stylisé */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #161B22;
        color: #F0F6FC !important; /* Blanc cassé pour le footer */
        text-align: center;
        padding: 10px;
        font-size: 12px;
        border-top: 2px solid #58A6FF;
        z-index: 100;
    }

    /* 6. Boutons de navigation */
    [data-testid="stSidebarNavLink"] span {
        color: #C9D1D9 !important;
    }
    [data-testid="stSidebarNavLink"][aria-current="page"] span {
        color: #58A6FF !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. IDENTIFICATION (SIDEBAR) ---
with st.sidebar:
    st.markdown("## 🎓 Identification")
    st.markdown(f"""
    <div style="background-color: #0D1117; padding: 15px; border-radius: 10px; border: 1px solid #58A6FF;">
        <p style="margin:0; color:#58A6FF !important; font-weight:bold; font-size:16px;">Logiciel : AxialFlow</p>
        <hr style="margin:10px 0; border-color:#30363D;">
        <p style="margin:0; font-size:14px;"><b>Nom :</b> FODIL Mohammed El Amine</p>
        <p style="margin:0; font-size:14px;"><b>Grade :</b> Master 1 GM</p>
        <p style="margin:0; font-size:14px;"><b>Université :</b> Univ. de Maghnia</p>
        <hr style="margin:10px 0; border-color:#30363D;">
        <p style="margin:0; font-size:12px; color:#58A6FF !important;">📧 fodilmedam@gmail.com</p>
        <p style="margin:0; font-size:12px; color:#58A6FF !important;">📞 0550139987</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

# --- 4. DÉFINITION ET NAVIGATION ---
pages_config = {
    "📚 Cours Compresseur Axial": [
        st.Page("pages/1_Introduction.py", title="Introduction", icon="📖"),
        st.Page("pages/2_Thermodynamique.py", title="Thermodynamique", icon="🔥")
    ],
    "⚙️ Analyse Technique": [
        st.Page("pages/3_Triangles_de_Vitesses.py", title="Triangles de Vitesses", icon="🌀"),
        st.Page("pages/4_Degre_de_Reaction.py", title="Degré de Réaction", icon="⚖️")
    ],
    "📝 Évaluation": [
        st.Page("pages/5_Exercices_et_Corrections.py", title="Exercices & Corrections", icon="📝")
    ]
}

pg = st.navigation(pages_config)

# --- 5. FOOTER ---
st.markdown("""
    <div class="footer">
        © 2026 - AxialFlow | <b>Dr FODIL</b> | Master 1 Génie Mécanique - Centre Universitaire de Maghnia
    </div>
""", unsafe_allow_html=True)

pg.run()
