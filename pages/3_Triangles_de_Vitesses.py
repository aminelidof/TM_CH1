import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# --- CONFIGuration DE LA PAGE ---
st.set_page_config(page_title="Turbomachines Pro - Analyse Multiphysique", layout="wide")

# CSS Avancé pour un look "Software Industriel"
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .stMetric { border: 1px solid #1F497D; padding: 15px; border-radius: 12px; background-color: #ffffff; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    .main-header { font-size: 32px; color: #1F497D; font-weight: bold; border-bottom: 3px solid #1F497D; padding-bottom: 10px; }
    .section-card { background-color: #ffffff; padding: 20px; border-radius: 15px; border-left: 5px solid #1F497D; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🌀 Plateforme d\'Analyse Aérodynamique et Thermodynamique</p>', unsafe_allow_html=True)

# --- SIDEBAR : PARAMÉTRAGE EXPERT ---
with st.sidebar:
    st.header("🛠️ Bureau d'Études")
    with st.expander("🚀 Paramètres Cinématiques", expanded=True):
        U = st.slider("Vitesse périphérique (U) [m/s]", 100, 650, 320)
        Ca = st.slider("Vitesse axiale (Ca) [m/s]", 50, 350, 160)
        alpha1 = st.slider("Angle d'injection (α1) [°]", 0, 45, 12)
        beta2 = st.slider("Angle de sortie relatif (β2) [°]", 10, 65, 42)

    with st.expander("🌡️ Conditions Fluides (Air)"):
        T01 = st.number_input("Température totale entrée (T01) [K]", value=288.15)
        P01 = st.number_input("Pression totale entrée (P01) [bar]", value=1.01325)
        Cp = 1005
        gamma = 1.4
        R = 287.05

    st.info("💡 Cette simulation utilise les modèles de diffusion de Lieblein (1953) et les critères de stabilité de la NASA.")

# --- CALCULS NOYAU (ENGINE) ---
# Conversion angles
a1_rad, b2_rad = np.radians(alpha1), np.radians(beta2)

# Station 1 : Entrée Rotor
Cw1 = Ca * np.tan(a1_rad)
Vw1 = U - Cw1
beta1 = np.degrees(np.arctan2(Vw1, Ca))
C1 = np.sqrt(Ca**2 + Cw1**2)
V1 = np.sqrt(Ca**2 + Vw1**2)

# Station 2 : Sortie Rotor
Vw2 = Ca * np.tan(b2_rad)
Cw2 = U - Vw2
alpha2 = np.degrees(np.arctan2(Cw2, Ca))
C2 = np.sqrt(Ca**2 + Cw2**2)
V2 = np.sqrt(Ca**2 + Vw2**2)

# --- ANALYSE THERMODYNAMIQUE ---
W_euler = U * (Cw2 - Cw1)
delta_T0 = W_euler / Cp
T02 = T01 + delta_T0

# Calcul du rendement estimé (Modèle simplifié de charge d'aube)
# Un coefficient de charge psi élevé diminue généralement le rendement
phi = Ca / U
psi = W_euler / (U**2)
eta_poly_est = 0.94 - (0.05 * psi) # Estimation empirique

# Rapport de pression
Pi_stage = (1 + (eta_poly_est * delta_T0 / T01))**(gamma/(gamma-1))
P02 = P01 * Pi_stage

# --- CRITÈRES DE DIFFUSION AVANCÉS ---
# Facteur de Haller
haller = V2 / V1
# Facteur de Diffusion de Lieblein (DF) - Supposant une solidité d'aube s=1.5
solidite = 1.5
df_lieblein = (1 - V2/V1) + (abs(Vw1 - Vw2) / (2 * solidite * V1))

# --- STYLE CSS SPÉCIFIQUE POUR LES METRICS (À mettre en haut de la page) ---
st.markdown("""
    <style>
    /* Conteneur principal de la métrique */
    div[data-testid="stMetric"] {
        background-color: #161B22 !important;
        border: 1px solid #30363D !important;
        border-top: 3px solid #58A6FF !important; /* Ligne bleue supérieure pour le style */
        padding: 15px 10px !important;
        border-radius: 10px !important;
        transition: transform 0.2s;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: scale(1.02);
        border-color: #58A6FF !important;
    }

    /* Libellé (Le titre en petit) */
    div[data-testid="stMetricLabel"] > div {
        color: #8B949E !important; /* Gris clair pour le titre */
        font-size: 14px !important;
        font-weight: bold !important;
        text-transform: uppercase;
    }

    /* Valeur (Le chiffre en gros) */
    div[data-testid="stMetricValue"] > div {
        color: #FFFFFF !important; /* BLANC PUR pour la valeur */
        font-size: 24px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- AFFICHAGE : TABLEAU DE BORD (DASHBOARD) ---
st.subheader("📊 Performances Globales de l'Étage")

# Utilisation de containers pour isoler les colonnes
with st.container():
    c1, c2, c3, c4, c5 = st.columns(5)
    
    # On peut ajouter un petit indicateur de tendance (delta) si vous voulez
    c1.metric("Travail Euler", f"{W_euler/1000:.2f} kJ/kg")
    c2.metric("Rapport Pression π", f"{Pi_stage:.3f}")
    c3.metric("Température T02", f"{T02:.1f} K")
    c4.metric("Coeff. de Charge ψ", f"{psi:.2f}")
    c5.metric("Coeff. de Débit φ", f"{phi:.2f}")

st.markdown("---")

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION ET STYLE ---
st.markdown("""
<style>
    .calc-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f497d;
        margin-bottom: 20px;
    }
    .result-val {
        color: #e63946;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- LAYOUT PRINCIPAL ---
col_plot, col_text = st.columns([1.5, 1])

with col_plot:
    st.subheader("📐 Triangles des Vitesses")
    
    # 
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), facecolor='#f5f7f9')

    def draw_triangle(ax, u, ca, cw, title, color_c, color_v, is_exit=False):
        # Vecteur U (Base)
        ax.quiver(0, 0, u, 0, angles='xy', scale_units='xy', scale=1, color='black', label='U (Rotor)')
        # Vecteur C (Absolu)
        ax.quiver(0, 0, cw, ca, angles='xy', scale_units='xy', scale=1, color=color_c, width=0.015, label='C (Absolu)')
        # Vecteur V (Relatif)
        ax.quiver(u, 0, cw-u, ca, angles='xy', scale_units='xy', scale=1, color=color_v, width=0.01, label='V (Relatif)')
        
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_xlim(-50, max(u, cw) + 150)
        ax.set_ylim(-20, ca + 150)
        ax.set_aspect('equal')
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.legend(loc='upper right', fontsize='small')

    draw_triangle(ax1, U, Ca, Cw1, "Entrée (Station 1)", "#1f77b4", "#ff7f0e")
    draw_triangle(ax2, U, Ca, Cw2, "Sortie (Station 2)", "#2ca02c", "#d62728")
    
    st.pyplot(fig)

    st.info("""
    **Interprétation Physique :** Le rotor dévie l'écoulement en augmentant la composante tangentielle ($C_{w1} \rightarrow C_{w2}$). 
    C'est ce 'redressement' du fluide qui traduit le transfert de couple mécanique en énergie fluide.
    """)

with col_text:
    st.subheader("🏁 Analyse Étape par Étape")
    
    with st.container():
        st.markdown('<div class="calc-box">', unsafe_allow_html=True)
        
        # --- ÉTAPE 1 : EULER AVEC DÉTAIL DES COMPOSANTES ---
        st.markdown("#### 1. Transfert de Travail ($W$)")

        with st.expander("🔍 D'où viennent les valeurs 175.9 et 34.0 ?", expanded=False):
            st.write("Ces valeurs sont les projections tangentielles des vitesses absolues :")
            st.latex(rf"C_{{w1}} = C_a \cdot \tan(\alpha_1) = {Cw1:.1f} \, m/s")
            st.latex(rf"C_{{w2}} = U - (C_a \cdot \tan(\beta_2)) = {Cw2:.1f} \, m/s")

        st.write("Calcul du travail spécifique par l'équation d'Euler :")
        st.latex(r"W = U \cdot (C_{w2} - C_{w1})")

        # Ligne de remplacement avec vos chiffres
        st.latex(rf"W = {U:.1f} \cdot ({Cw2:.1f} - {Cw1:.1f})")

        # Résultat final
        work = U * (Cw2 - Cw1)
        st.latex(rf"W = {work:.1f} \, J/kg")        
        # --- ÉTAPE 2 : THERMO ---
        st.markdown("#### 2. Saut de Température ($\Delta T_0$)")
        st.write("D'après le 1er principe en système ouvert ($q=0$) :")
        delta_T0 = work / 1004.5
        st.latex(rf"\Delta T_0 = \frac{{W}}{{c_p}} = {delta_T0:.2f} \, K")
        
# --- ÉTAPE 3 : PRESSION ---
        st.markdown("#### 3. Taux de Pression ($\pi$)")
        st.write("Le taux de pression isentropique lie l'augmentation de température à l'augmentation de pression :")
        
        # Calculs
        pi_is = ( (T01 + delta_T0) / T01 )**(gamma/(gamma-1))
        puissance_gamma = gamma/(gamma-1) # vaut 3.5 pour l'air
        
        # Affichage avec remplacement des chiffres
        st.latex(rf"\pi_{{is}} = \left( \frac{{T_{{01}} + \Delta T_0}}{{T_{{01}}}} \right)^{{\frac{{\gamma}}{{\gamma-1}}}}")
        st.latex(rf"\pi_{{is}} = \left( \frac{{{T01:.1f} + {delta_T0:.2f}}}{{{T01:.1f}}} \right)^{{{puissance_gamma:.1f}}}")
        st.latex(rf"\pi_{{is}} = {pi_is:.3f}")
        
        st.info(f"💡 Ce résultat signifie que l'étage augmente la pression de **{(pi_is-1)*100:.1f} %** par rapport à l'entrée.")

        # --- ÉTAPE 4 : MACH & DIAGNOSTIC ---
        st.markdown("#### 4. Diagnostic de l'Écoulement")
        
        # Calcul vitesse du son
        a1 = np.sqrt(gamma * R * T01)
        # Calcul Mach relatif
        M_v1 = V1 / a1
        
        st.write("**Vitesse du son à l'entrée ($a_1$) :**")
        st.latex(rf"a_1 = \sqrt{{\gamma \cdot R \cdot T_{{01}}}} = \sqrt{{1.4 \cdot 287 \cdot {T01:.1f}}} = {a1:.1f} \, m/s")
        
        st.write("**Nombre de Mach relatif ($M_{v1}$) :**")
        st.latex(rf"M_{{v1}} = \frac{{V_1}}{{a_1}} = \frac{{{V1:.1f}}}{{{a1:.1f}}} = {M_v1:.2f}")

        # Verdict de l'ingénieur
        if M_v1 > 0.9:
            st.error(f"🚨 **Verdict :** M = {M_v1:.2f} (Régime Transsonique). Apparition d'ondes de choc sur l'extrados de l'aube, ce qui va chuter le rendement.")
        elif M_v1 > 0.7:
            st.warning(f"⚠️ **Verdict :** M = {M_v1:.2f} (Régime Subsonique élevé). Risque de blocage si le débit augmente.")
        else:
            st.success(f"✅ **Verdict :** M = {M_v1:.2f} (Régime Subsonique). Écoulement sain et pertes minimales.")

        st.markdown('</div>', unsafe_allow_html=True)

# --- DIAGNOSTIC INDUSTRIEL ET STABILITÉ ---
st.header("🔬 Diagnostic de Stabilité et de Charge")

t1, t2, t3 = st.tabs(["🛡️ Critères de Décrochage", "📉 Diagramme de Smith", "📖 Physique de l'Étage"])

with t1:
    col_crit1, col_crit2 = st.columns(2)
    with col_crit1:
        st.subheader("Rapport de Haller")
        st.write("Limite académique : > 0.72")
        st.progress(min(max(haller, 0.0), 1.0))
        if haller < 0.72:
            st.error(f"❌ **Haller : {haller:.2f}** - Risque de décollement important.")
        else:
            st.success(f"✅ **Haller : {haller:.2f}** - Diffusion saine.")

    with col_crit2:
        st.subheader("Facteur de Lieblein (D-Factor)")
        st.write("Limite industrielle : < 0.55")
        if df_lieblein > 0.55:
            st.error(f"🚨 **D-Factor : {df_lieblein:.2f}** - Surcharge aérodynamique ! Le flux ne suivra pas l'aube.")
        else:
            st.success(f"✅ **D-Factor : {df_lieblein:.2f}** - Charge optimale.")

with t2:
    st.write("Le **Diagramme de Smith** permet de situer l'étage par rapport à l'optimum de rendement.")
    # Simulation visuelle d'un diagramme de Smith
    smith_x = np.linspace(0.2, 0.9, 50)
    smith_y = 0.9 - 2*(smith_x - 0.5)**2 # Parabole de rendement
    
    fig2, ax_smith = plt.subplots(figsize=(8, 4))
    ax_smith.plot(smith_x, smith_y, 'b--', label="Zone d'efficacité max (90%)")
    ax_smith.scatter(phi, 0.9 - 2*(phi - 0.5)**2, color='red', s=100, label="Votre Point de Design")
    ax_smith.set_xlabel("Coefficient de débit (φ)")
    ax_smith.set_ylabel("Efficacité estimée")
    ax_smith.legend()
    st.pyplot(fig2)

with t3:
    st.markdown(f"""
    ### ⚙️ Transformation de l'Énergie
    L'augmentation de pression dans cet étage est de **{ (Pi_stage-1)*100 :.1f}%**.
    
    1. **Le Rotor** convertit le travail mécanique en énergie cinétique (augmentation de $C$) et en pression statique (diffusion de $V$).
    2. **Le Stator** (analysé ici via $\alpha_2$) devra transformer l'énergie cinétique de sortie $C_2$ en pression statique supplémentaire en redressant le flux vers l'axe.
    
    **Note sur la compressibilité :** A un Mach relatif de **{V1/np.sqrt(gamma*R*T01):.2f}**, le compresseur est en régime 
    {'**Supersonique** (Ondes de choc probables)' if V1/np.sqrt(gamma*R*T01) > 1.0 else '**Subsonique**'}.
    """)



st.markdown("---")
st.caption("🚀 Développé par Dr FODIL - M1 GM | Module : Turbomachines Avancées")


