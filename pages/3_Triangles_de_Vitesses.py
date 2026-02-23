import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- 1. CONFIGURATION ET STYLE ---
# (On garde votre style mais on l'épure pour la cohérence)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0E1117; }
    .main-header { font-size: 28px; color: #58A6FF; font-weight: bold; border-bottom: 2px solid #58A6FF; padding-bottom: 10px; margin-bottom: 20px; }
    
    /* Style des Metrics */
    div[data-testid="stMetric"] {
        background-color: #161B22 !important;
        border: 1px solid #30363D !important;
        border-top: 3px solid #58A6FF !important;
        padding: 15px !important;
        border-radius: 10px !important;
    }
    div[data-testid="stMetricLabel"] > div { color: #8B949E !important; font-size: 12px !important; text-transform: uppercase; }
    div[data-testid="stMetricValue"] > div { color: #FFFFFF !important; font-size: 22px !important; }
    
    /* Boites de calcul */
    .calc-box { background-color: #1C2128; padding: 20px; border-radius: 12px; border: 1px solid #30363D; color: #FFFFFF; }
    </style>
""", unsafe_allow_html=True)

# --- 2. LOGIQUE DE CALCUL (Moteur interne) ---
# (Placé en haut pour que les variables soient disponibles partout)
with st.sidebar:
    st.header("🛠️ Paramètres du Design")
    U = st.slider("Vitesse périphérique (U) [m/s]", 100, 650, 320)
    Ca = st.slider("Vitesse axiale (Ca) [m/s]", 50, 350, 160)
    alpha1 = st.slider("Angle d'injection (α1) [°]", 0, 45, 12)
    beta2 = st.slider("Angle de sortie relatif (β2) [°]", 10, 65, 42)
    
    st.divider()
    T01 = st.number_input("Température totale T01 [K]", value=288.15)
    P01 = st.number_input("Pression totale P01 [bar]", value=1.013)
    gamma, Cp, R = 1.4, 1005, 287.05

# Calculs cinématiques
a1_rad, b2_rad = np.radians(alpha1), np.radians(beta2)
Cw1 = Ca * np.tan(a1_rad)
Vw1 = U - Cw1
V1 = np.sqrt(Ca**2 + Vw1**2)

Vw2 = Ca * np.tan(b2_rad)
Cw2 = U - Vw2
V2 = np.sqrt(Ca**2 + Vw2**2)

# Thermodynamique
W_euler = U * (Cw2 - Cw1)
delta_T0 = W_euler / Cp
phi, psi = Ca / U, W_euler / (U**2)
eta_poly = 0.92
Pi_stage = (1 + (eta_poly * delta_T0 / T01))**(gamma/(gamma-1))

# --- 3. AFFICHAGE : HEADER & DASHBOARD ---
st.markdown('<p class="main-header">📐 Analyse des Triangles de Vitesses</p>', unsafe_allow_html=True)

cols = st.columns(5)
cols[0].metric("Travail Euler", f"{W_euler/1000:.2f} kJ/kg")
cols[1].metric("Rapport Pression", f"{Pi_stage:.3f}")
cols[2].metric("ΔT Total", f"{delta_T0:.1f} K")
cols[3].metric("Coeff. Charge ψ", f"{psi:.2f}")
cols[4].metric("Coeff. Débit φ", f"{phi:.2f}")

st.divider()

# --- 4. AFFICHAGE : GRAPHIQUES ET ANALYSE ---
col_left, col_right = st.columns([1.2, 0.8])

with col_left:
    st.subheader("🌀 Visualisation des Vecteurs")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), facecolor='#0E1117')
    plt.subplots_adjust(wspace=0.4)

    def draw_triangle(ax, u, ca, cw, title, color_c, color_v):
        ax.set_facecolor('#161B22')
        # Vecteur U
        ax.quiver(0, 0, u, 0, angles='xy', scale_units='xy', scale=1, color='white', label='U')
        # Vecteur C (Absolu)
        ax.quiver(0, 0, cw, ca, angles='xy', scale_units='xy', scale=1, color=color_c, width=0.015, label='C')
        # Vecteur V (Relatif)
        ax.quiver(u, 0, cw-u, ca, angles='xy', scale_units='xy', scale=1, color=color_v, width=0.01, label='V')
        
        ax.set_title(title, color='white', fontsize=10)
        ax.set_xlim(-50, max(u, cw) + 100)
        ax.set_ylim(-20, ca + 100)
        ax.tick_params(colors='white', labelsize=8)
        ax.grid(True, alpha=0.1)
        ax.legend(fontsize='x-small')

    draw_triangle(ax1, U, Ca, Cw1, "Entrée Rotor (Station 1)", "#58A6FF", "#FFA657")
    draw_triangle(ax2, U, Ca, Cw2, "Sortie Rotor (Station 2)", "#7EE787", "#FF7B72")
    
    st.pyplot(fig)
    
    with st.expander("📖 Aide à l'interprétation"):
        st.write("Le triangle montre comment le rotor 'aspire' le fluide et lui communique de l'énergie en augmentant sa vitesse tangentielle absolue (C_w).")

with col_right:
    st.subheader("📜 Détails du Calcul")
    st.markdown('<div class="calc-box">', unsafe_allow_html=True)
    
    st.markdown("**1. Composantes Tangentielles :**")
    st.latex(rf"C_{{w1}} = {Cw1:.1f} \, m/s \quad | \quad C_{{w2}} = {Cw2:.1f} \, m/s")
    
    st.markdown("**2. Équation d'Euler :**")
    st.latex(rf"W = {U} \cdot ({Cw2:.1f} - {Cw1:.1f}) = {W_euler:.0f} \, J/kg")
    
    st.markdown("**3. Diagnostic Mach :**")
    a1 = np.sqrt(gamma * R * T01)
    m_v1 = V1 / a1
    st.write(f"Vitesse du son $a_1$: {a1:.1f} m/s")
    st.write(f"Mach relatif $M_{{v1}}$: **{m_v1:.2f}**")
    
    if m_v1 > 0.9: st.error("Régime Transsonique 🚨")
    elif m_v1 > 0.7: st.warning("Régime Subsonique élevé ⚠️")
    else: st.success("Régime Subsonique stable ✅")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. SECTION BASSE : STABILITÉ ---
st.divider()
st.subheader("🛡️ Critères de Stabilité Industriels")
t1, t2 = st.columns(2)

with t1:
    haller = V2 / V1
    st.write(f"**Facteur de Haller :** `{haller:.2f}`")
    st.progress(min(max(haller, 0.0), 1.0))
    if haller < 0.72: st.error("Décollement probable (Haller < 0.72)")
    else: st.success("Diffusion contrôlée")

with t2:
    df_lieblein = (1 - V2/V1) + (abs(Cw2 - Cw1) / (2 * 1.5 * V1))
    st.write(f"**D-Factor (Lieblein) :** `{df_lieblein:.2f}`")
    if df_lieblein > 0.55: st.error("Surcharge aérodynamique (> 0.55)")
    else: st.success("Charge aube optimale")

st.caption("AxialFlow Pro | Master 1 Génie Mécanique | Univ. Maghnia")
