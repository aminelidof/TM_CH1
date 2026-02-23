import streamlit as st

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="AxialFlow Pro | M1-GM",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. STYLE CSS AVANCÉ (DARK INDUSTRIAL) ---
st.markdown("""
    <style>
    /* Import Police Moderne */
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;700&display=swap');
    
    .stApp {
        background-color: #0E1117;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Cartes de Navigation */
    .nav-card {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 25px;
        transition: all 0.3s ease;
        text-align: center;
        margin-bottom: 20px;
    }
    .nav-card:hover {
        border-color: #58A6FF;
        transform: translateY(-5px);
        background: #1C2128;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }

    /* Badge Header */
    .main-title {
        background: linear-gradient(90deg, #58A6FF, #2ea043);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
    }

    /* Footer Professionnel */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(13, 17, 23, 0.95);
        color: #8B949E;
        text-align: center;
        padding: 12px;
        font-size: 13px;
        border-top: 1px solid #30363D;
        z-index: 1000;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. DÉFINITION DES PAGES (LIÉES À VOTRE DOSSIER /pages) ---
# Assurez-vous que les noms de fichiers correspondent exactement à ceux sur GitHub
pages_dict = {
    "📚 Cours Théorique": [
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

pg = st.navigation(pages_dict)

# --- 4. BARRE LATÉRALE (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🌀 AxialFlow</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Bloc Auteur
    st.markdown(f"""
    <div style="background-color: #0D1117; padding: 15px; border-radius: 10px; border: 1px solid #30363D;">
        <p style="margin:0; color:#58A6FF; font-weight:bold; font-size:14px;">🎓 LOGICIEL ACADÉMIQUE</p>
        <p style="margin:5px 0 0 0; font-size:15px; color:white;"><b>FODIL M. E. A.</b></p>
        <p style="margin:0; font-size:13px; color:#8B949E;">Master 1 Génie Mécanique</p>
        <p style="margin:0; font-size:13px; color:#8B949E;">Univ. de Maghnia</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.info("**Module :** Turbomachines II\n\n**Focus :** Compresseurs Axiaux")

# --- 5. LOGIQUE D'AFFICHAGE DU DASHBOARD ---
# Si aucune page spécifique n'est encore sélectionnée ou si on est à la racine
# Streamlit switch_page peut être utilisé pour forcer l'accueil si besoin.

# Rendu de la page sélectionnée
pg.run()

# --- 6. FOOTER ---
st.markdown(f"""
    <div class="footer">
        © 2026 - AxialFlow | <b>Développé par Dr. FODIL</b> | Master 1 Génie Mécanique - Centre Universitaire de Maghnia
    </div>
""", unsafe_allow_html=True)
