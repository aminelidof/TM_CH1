import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Degré de Réaction - Analyse Avancée", layout="wide")

st.markdown('<h1 style="color:#1F497D;">⚖️ Analyse Approfondie du Degré de Réaction (R)</h1>', unsafe_allow_html=True)

st.write("""
Le **degré de réaction** est le paramètre de conception le plus critique pour équilibrer les pertes aérodynamiques entre les rangées d'aubes fixes et mobiles. 
Il définit physiquement la part de l'augmentation de pression statique réalisée dans le rotor par rapport à l'étage complet.
""")

# --- SECTION 1 : THÉORIE ET FORMALISME ---
st.header("1. Fondements Thermodynamiques")

col_th_1, col_th_2 = st.columns([1.5, 1])

with col_th_1:
    st.markdown("### Définition Enthalpique")
    st.write("Le degré de réaction compare le saut d'enthalpie statique dans le rotor à celui de l'étage :")
    st.latex(r"R = \frac{h_2 - h_1}{h_3 - h_1} \approx \frac{\Delta P_{rotor}}{\Delta P_{étage}}")
    
    st.markdown("### Relation Cinématique (Hypothèse $C_a = cst$)")
    st.write("En utilisant les triangles de vitesses, $R$ est directement lié aux angles des aubes :")
    st.latex(r"R = \frac{C_a}{2U}(\tan \beta_1 + \tan \beta_2)")
    st.write("Ou encore, en fonction de la giration absolue :")
    st.latex(r"R = 1 - \frac{C_{w1} + C_{w2}}{2U}")

with col_th_2:
    st.info("""
    🔍 **Interprétation Physique** :
    - Si **R = 0.5**, les triangles de vitesses sont **symétriques**.
    - Les pertes par frottement sont proportionnelles au cube de la vitesse relative. 
    - Un bon design vise à minimiser les vitesses maximales dans chaque rangée.
    """)

st.write("---")

# --- SECTION 2 : SIMULATEUR DE GÉOMÉTRIE ---
st.header("2. Simulateur Interactif de Répartition de Charge")

with st.sidebar:
    st.header("🛠️ Configuration de l'Étage")
    R_target = st.slider("Degré de Réaction Cible (R)", 0.0, 1.0, 0.5, step=0.05)
    psi = st.slider("Coefficient de Charge (ψ)", 0.2, 0.6, 0.4)
    phi = st.slider("Coefficient de Débit (φ)", 0.4, 0.8, 0.6)

# Calcul des angles basés sur R, psi et phi
# R = 1 - psi/2 - tan(alpha1)*phi
# On en déduit les angles nécessaires pour atteindre ce R
tan_alpha1 = (1 - R_target - psi/2) / phi
alpha1 = np.degrees(np.arctan(tan_alpha1))

tan_alpha2 = (psi / phi) + tan_alpha1
alpha2 = np.degrees(np.arctan(tan_alpha2))

tan_beta1 = (U_phi := 1/phi) - tan_alpha1
beta1 = np.degrees(np.arctan(tan_beta1))

tan_beta2 = tan_beta1 - (psi / phi)
beta2 = np.degrees(np.arctan(tan_beta2))

# Affichage des métriques de design
m1, m2, m3, m4 = st.columns(4)
m1.metric("Angle Rotor Entrée (β1)", f"{beta1:.1f}°")
m2.metric("Angle Rotor Sortie (β2)", f"{beta2:.1f}°")
m3.metric("Angle Stator Entrée (α2)", f"{alpha2:.1f}°")
m4.metric("Angle Stator Sortie (α1)", f"{alpha1:.1f}°")

st.write("---")

# --- SECTION 3 : ANALYSE DES CAS LIMITES ---
st.header("3. Analyse des Régimes de Fonctionnement")

tab1, tab2, tab3 = st.tabs(["📉 R = 0 (Étage à Action)", "⚖️ R = 0.5 (Étage Symétrique)", "📈 R = 1.0 (Réaction Totale)"])

with tab1:
    st.warning("### Configuration à Action pure")
    st.write("""
    - **Principe** : Le rotor ne produit aucune augmentation de pression statique ($P_1 = P_2$). 
    - **Géométrie** : Les triangles de vitesses montrent que $V_1 = V_2$. Le rotor sert uniquement à dévier le fluide pour augmenter son énergie cinétique.
    - **Inconvénient** : Vitesses très élevées dans le stator, entraînant des pertes par frottement massives.
    """)
    

with tab2:
    st.success("### Configuration Symétrique (Standard Industriel)")
    st.write("""
    - **Principe** : L'augmentation de pression est répartie à 50/50 entre le rotor et le stator.
    - **Avantages** : 
    """)
    
    # Utilisation de st.latex pour une mise en valeur maximale
    st.latex(r"\alpha_1 = \beta_2 \quad \text{et} \quad \beta_1 = \alpha_2")
    
    st.write("""
    - **Performance** : Rendement maximal car les nombres de Mach sont minimisés dans les deux rangées.
    - **Fabrication** : Coûts réduits grâce à des profils d'aubes similaires.
    """)
    

with tab3:
    st.error("### Configuration à Réaction Totale")
    st.write("""
    - **Principe** : Le stator ne sert qu'à redresser le flux sans augmenter la pression. Toute la compression est faite par le rotor.
    - **Risque** : Charge excessive sur le rotor, risque de décrochage (stall) très élevé en bout d'aube.
    """)

st.write("---")

# --- SECTION 4 : LE POINT DE VUE DE L'INGÉNIEUR ---
st.header("4. Optimisation et Pertes Secondaires")

st.markdown("""
### Pourquoi ne choisit-on pas toujours R = 0.5 ?
Bien que $R=0.5$ soit optimal pour le rendement de profil, les concepteurs font varier $R$ selon le rayon (du pied au sommet de l'aube) :
1. **Au Pied (Hub)** : On tend vers un $R$ plus faible pour compenser les fortes vitesses tangentielles.
2. **Au Sommet (Tip)** : On tend vers un $R$ plus élevé pour limiter les chocs supersoniques.

**L'équation de l'équilibre radial** impose souvent un $R$ variant de **0.3 à 0.7** le long de l'envergure de l'aube.
""")

# Petit graphique de tendance des pertes
x = np.linspace(0, 1, 100)
pertes = (x - 0.5)**2 + 0.1 # Parabole simplifiée

fig, ax = plt.subplots(figsize=(8, 3))
ax.plot(x, pertes, color='#1F497D', lw=2)
ax.fill_between(x, 0.1, pertes, alpha=0.1, color='blue')
ax.set_title("Évolution des pertes globales en fonction de R")
ax.set_xlabel("Degré de Réaction (R)")
ax.set_ylabel("Coefficient de Pertes")
ax.annotate('Optimum (Design)', xy=(0.5, 0.1), xytext=(0.6, 0.2),
             arrowprops=dict(facecolor='black', shrink=0.05))
st.pyplot(fig)

st.markdown("---")
st.caption("Module Expert M1 GM - Analyse des Turbomachines Axiales - Dr FODIL")