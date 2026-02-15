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

# --- AFFICHAGE : TABLEAU DE BORD (DASHBOARD) ---
st.subheader("📊 Performances Globales de l'Étage")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Travail Euler", f"{W_euler/1000:.2f} kJ/kg")
c2.metric("Rapport Pression π", f"{Pi_stage:.3f}")
c3.metric("Température T02", f"{T02:.1f} K")
c4.metric("Coeff. de Charge ψ", f"{psi:.2f}")
c5.metric("Coeff. de Débit φ", f"{phi:.2f}")

st.write("---")

# --- VISUALISATION DES TRIANGLES ---
col_plot, col_text = st.columns([2, 1])

with col_plot:
    st.subheader("📐 Triangles des Vitesses (Stations 1 & 2)")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), facecolor='#f5f7f9')

    def draw_triangle(ax, u, ca, cw, vw, title, color_c, color_v):
        # Vecteur Entraînement U
        ax.quiver(0, 0, u, 0, angles='xy', scale_units='xy', scale=1, color='black', label='U (Rotor)')
        # Vecteur Absolu C
        ax.quiver(0, 0, cw, ca, angles='xy', scale_units='xy', scale=1, color=color_c, width=0.015, label='C (Absolu)')
        # Vecteur Relatif V (Fermeture)
        ax.quiver(u, 0, cw-u, ca, angles='xy', scale_units='xy', scale=1, color=color_v, width=0.01, label='V (Relatif)')
        
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_xlim(-50, max(u, cw) + 100)
        ax.set_ylim(-20, ca + 100)
        ax.set_aspect('equal')
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(loc='lower right', fontsize='small')

    draw_triangle(ax1, U, Ca, Cw1, Vw1, f"Entrée Rotor\n(β1 = {beta1:.1f}°)", "#1f77b4", "#ff7f0e")
    draw_triangle(ax2, U, Ca, Cw2, -Vw2, f"Sortie Rotor\n(α2 = {alpha2:.1f}°)", "#2ca02c", "#d62728")
    
    st.pyplot(fig)

with col_text:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🔍 Analyse Cinématique")
    st.write(f"**Vitesse son locale (a1) :** {np.sqrt(gamma*R*T01):.1f} m/s")
    st.write(f"**Mach relatif entrée (M_w1) :** {V1/np.sqrt(gamma*R*T01):.2f}")
    st.write(f"**Mach absolu sortie (M_c2) :** {C2/np.sqrt(gamma*R*T02):.2f}")
    st.markdown("---")
    st.write("**Déviation du flux :**")
    st.latex(rf"\Delta \beta = {abs(beta1-beta2):.1f}^\circ")
    st.latex(rf"\Delta C_w = {Cw2-Cw1:.1f} \, m/s")
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