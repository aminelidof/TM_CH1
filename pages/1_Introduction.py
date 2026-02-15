import streamlit as st

# 1. Configuration de la page
st.set_page_config(page_title="1. Introduction - Compresseurs Axiaux", layout="wide")

st.markdown('<h1 style="color:#1F497D;">1️⃣ Introduction et Constitution</h1>', unsafe_allow_html=True)

# --- SECTION VISUELLE ---
col1, col2 = st.columns([1.5, 1])

with col1:
    st.write("""
    Le **compresseur axial** est une turbomachine thermique réceptrice. Son rôle est d'accroître la pression 
    d'un fluide compressible (air ou gaz) en lui transférant de l'énergie cinétique via des aubages en rotation.
    """)
    
    st.info("💡 **Définition de l'Étage** : L'unité de base est l'étage, composé d'un **Rotor** (roue mobile) suivi d'un **Stator** (redresseur fixe).")

    st.markdown("""
    ### Caractéristiques Principales
    * **Débit massique :** Très élevé, ce qui le rend indispensable pour les turboréacteurs d'aviation.
    * **Écoulement :** Les lignes de courant sont quasiment parallèles à l'axe de rotation.
    * **Taux de compression :** Faible par étage (**1.2 à 1.5**), nécessitant une configuration multi-étagée.
    """)

with col2:
    # On essaie de charger votre image locale
    try:
        st.image("compresseur.gif", 
                 caption="Vue en coupe d'un étage axial : Rotor (R) et Stator (S)",
                 use_container_width=True)
    except:
        st.error("⚠️ Image 'compresseur.webp' non trouvée à la racine du projet.")
        # Image de secours (URL) pour que l'animation "marche" quand même en test
        st.image("https://upload.wikimedia.org/wikipedia/commons/4/40/Axial_flow_compressor_stage.png", 
                 caption="Schéma technique (Source alternative)")

# --- COMPARAISON TECHNIQUE (CONTENU RICHE) ---
st.markdown("---")
st.subheader("📊 Comparaison : Axial vs Centrifuge")

st.write("Pour un étudiant en Master 1 GM, il est crucial de savoir pourquoi choisir un compresseur axial :")

data = {
    "Caractéristique": ["Débit massique", "Rapport de pression / étage", "Encombrement frontal", "Rendement global"],
    "Compresseur Axial": ["Très Élevé (🚀)", "Faible (1.2 - 1.5)", "Petit", "Excellent"],
    "Compresseur Centrifuge": ["Moyen", "Élevé (4.0 - 7.0)", "Grand", "Bon (mais limité)"]
}
st.table(data)

# --- DÉTAILS DES COMPOSANTS ---
st.markdown("### 🛠️ Rôle des composants de l'étage")
c1, c2 = st.columns(2)

with c1:
    st.success("🌀 **Le Rotor**")
    st.write("""
    - **Accélération** : Augmente la vitesse absolue du fluide.
    - **Travail** : C'est le seul élément qui fournit du travail mécanique au fluide (Équation d'Euler).
    - **Pression** : Augmente également la pression statique par effet centrifuge partiel.
    """)

with c2:
    st.warning("🧱 **Le Stator (Redresseur)**")
    st.write("""
    - **Diffusion** : Transforme l'énergie cinétique en pression statique (ralentissement).
    - **Désorbitation** : Redresse l'écoulement pour qu'il attaque l'étage suivant avec le bon angle.
    - **Travail** : Ne fournit aucun travail (élément fixe).
    """)