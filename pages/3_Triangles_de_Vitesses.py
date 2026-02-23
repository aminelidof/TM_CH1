import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- 1. CONFIGURATION ET DESIGN ---
st.set_page_config(page_title="AxialFlow Pro | Master 1 GM", layout="wide")

st.markdown("""
    <style>
    /* Global Background */
    [data-testid="stAppViewContainer"] { background-color: #0E1117; color: #FFFFFF; }
    
    /* Header Principal */
    .main-header { 
        font-size: 32px; color: #58A6FF; font-weight: 800; text-align: center;
        border-bottom: 2px solid #30363D; padding-bottom: 15px; margin-bottom: 20px;
    }

    /* Cards des Metrics */
    div[data-testid="stMetric"] {
        background-color: #161B22 !important;
        border: 1px solid #30363D !important;
        border-top: 4px solid #58A6FF !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    div[data-testid="stMetricLabel"] > div { color: #8B949E !important; font-size: 13px !important; font-weight: bold; text-transform: uppercase; }
    div[data-testid="stMetricValue"] > div { color: #FFFFFF !important; font-size: 26px !important; }

    /* Zone de Calcul (Expertise) */
    .calc-container {
        background-color: #1C2128; padding: 25px; border-radius: 15px; border: 1px solid #30363D;
    }
    h4 { color: #58A6FF !important; border-left: 4px solid #58A6FF; padding-left: 10px; margin-top: 25px !important; }
    
    /* Tabs Style */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #161B22; border-radius: 5px 5px 0 0; color: white; padding: 10px 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. LOGIQUE DE CALCUL (BACKEND) ---
with st.sidebar:
    st.header("🛠️ Bureau d'Études")
    with st.expander("🚀 Paramètres Cinématiques", expanded=True):
        U = st.slider("Vitesse périphérique (U) [m/s]", 100, 650, 320)
        Ca = st.slider("Vitesse axiale (Ca) [m/s]", 50, 350, 160)
        alpha1 = st.slider("Angle d'injection (α1) [°]", 0, 45, 12)
        beta2 = st.slider("Angle de sortie relatif (β2) [°]", 10, 65, 42)

    with st.expander("🌡️ Conditions Ambiantes"):
        T01 = st.number_input("Température totale entrée (T01) [K]", value=288.15)
        P01 = st.number_input("Pression totale entrée (P01) [bar]", value=1.013)
        Cp, gamma, R = 1004.5, 1.4, 287.05

# --- CALCULS PHYSIQUES ---
a1_rad, b2_rad = np.radians(alpha1), np.radians(beta2)

# Station 1
Cw1 = Ca * np.tan(a1_rad)
Vw1 = U - Cw1
V1 = np.sqrt(Ca**2 + Vw1**2)
C1 = np.sqrt(Ca**2 + Cw1**2)

# Station 2
Vw2 = Ca * np.tan(b2_rad)
Cw2 = U - Vw2
V2 = np.sqrt(Ca**2 + Vw2**2)
C2 = np.sqrt(Ca**2 + Cw2**2)

# Thermodynamique
W_euler = U * (Cw2 - Cw1)
delta_T0 = W_euler / Cp
phi, psi = Ca / U, W_euler / (U**2)
eta_poly = 0.94 - (0.05 * psi)
pi_is = ( (T01 + (eta_poly * delta_T0)) / T01 )**(gamma/(gamma-1))

# Stabilité
haller = V2 / V1
df_lieblein = (1 - V2/V1) + (abs(Cw2 - Cw1) / (2 * 1.5 * V1))

# --- 3. AFFICHAGE : DASHBOARD ---
st.markdown('<p class="main-header">🌀 AxialFlow Pro : Analyse de l\'Étage</p>', unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Travail Euler", f"{W_euler/1000:.2f} kJ/kg")
m2.metric("Rapport Pression π", f"{pi_is:.3f}")
m3.metric("Saut Temp. ΔT0", f"{delta_T0:.2f} K")
m4.metric("Coeff. Charge ψ", f"{psi:.2f}")
m5.metric("Coeff. Débit φ", f"{phi:.2f}")

st.divider()

# --- 4. CŒUR DE LA PAGE : TRIANGLES ET EXPERTISE ---
col_left, col_right = st.columns([1.3, 1])

with col_left:
    st.subheader("📐 Triangles des Vitesses")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), facecolor='#0E1117')
    
    def draw_tri(ax, u, ca, cw, title, c_col, v_col):
        ax.set_facecolor('#161B22')
        # Vecteurs (U: blanc, C: bleu, V: orange/rouge)
        ax.quiver(0, 0, u, 0, angles='xy', scale_units='xy', scale=1, color='white', label='U', width=0.012)
        ax.quiver(0, 0, cw, ca, angles='xy', scale_units='xy', scale=1, color=c_col, label='C', width=0.018)
        ax.quiver(u, 0, cw-u, ca, angles='xy', scale_units='xy', scale=1, color=v_col, label='V', width=0.012)
        
        ax.set_title(title, color='#58A6FF', fontsize=12, fontweight='bold')
        ax.set_xlim(-50, max(u, cw) + 100)
        ax.set_ylim(-20, ca + 100)
        ax.axis('off')
        ax.legend(loc='upper right', fontsize='x-small', facecolor='#0E1117', labelcolor='white')

    draw_tri(ax1, U, Ca, Cw1, "Entrée (Station 1)", "#58A6FF", "#FFA657")
    draw_tri(ax2, U, Ca, Cw2, "Sortie (Station 2)", "#7EE787", "#FF7B72")
    
    st.pyplot(fig)
    

    st.info("**Interprétation :** Le rotor dévie l'écoulement en augmentant la composante tangentielle ($C_{w1} \\rightarrow C_{w2}$), créant le transfert de puissance.")

with col_right:
    st.subheader("🏁 Analyse Étape par Étape")
    st.markdown('<div class="calc-container">', unsafe_allow_html=True)
    
    st.markdown("#### 1. Transfert de Travail ($W$)")
    st.latex(rf"W = U \cdot (C_{{w2}} - C_{{w1}}) = {U} \cdot ({Cw2:.1f} - {Cw1:.1f})")
    st.latex(rf"W = {W_euler:.1f} \, J/kg")
    
    st.markdown("#### 2. Saut de Température ($\Delta T_0$)")
    st.latex(rf"\Delta T_0 = \frac{{W}}{{c_p}} = \frac{{{W_euler:.1f}}}{{1004.5}} = {delta_T0:.2f} \, K")
    
    st.markdown("#### 3. Taux de Pression ($\pi$)")
    st.latex(rf"\pi_{{is}} = \left( \frac{{{T01:.1f} + {delta_T0:.2f}}}{{{T01:.1f}}} \right)^{{3.5}} = {pi_is:.3f}")
    st.success(f"Augmentation de pression : **{(pi_is-1)*100:.1f} %**")

    st.markdown("#### 4. Diagnostic Mach")
    a1 = np.sqrt(gamma * R * T01)
    M_v1 = V1 / a1
    st.latex(rf"M_{{v1}} = \frac{{V_1}}{{a_1}} = \frac{{{V1:.1f}}}{{{a1:.1f}}} = {M_v1:.2f}")

    if M_v1 > 0.9: st.error(f"🚨 Verdict : Transsonique ({M_v1:.2f})")
    elif M_v1 > 0.7: st.warning(f"⚠️ Verdict : Subsonique élevé ({M_v1:.2f})")
    else: st.success(f"✅ Verdict : Subsonique sain ({M_v1:.2f})")

    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. STABILITÉ ET DIAGNOSTIC INDUSTRIEL ---
st.divider()
st.header("🔬 Diagnostic de Stabilité et de Charge")

t1, t2, t3 = st.tabs(["🛡️ Stabilité (Haller/Lieblein)", "📉 Diagramme de Smith", "📖 Physique de l'Étage"])

with t1:
    c_crit1, c_crit2 = st.columns(2)
    with c_crit1:
        st.write(f"**Rapport de Haller :** `{haller:.3f}`")
        if haller < 0.72: st.error("❌ Risque de décollement (Haller < 0.72)")
        else: st.success("✅ Diffusion saine")
    with c_crit2:
        st.write(f"**D-Factor (Lieblein) :** `{df_lieblein:.3f}`")
        if df_lieblein > 0.55: st.error("🚨 Surcharge aérodynamique (> 0.55)")
        else: st.success("✅ Charge optimale")

with t2:
    st.write("Visualisation du point de fonctionnement par rapport à l'optimum de Smith.")
    s_x = np.linspace(0.2, 0.9, 50)
    s_y = 0.92 - 2*(s_x - 0.5)**2
    f_smith, ax_s = plt.subplots(figsize=(8, 3), facecolor='#0E1117')
    ax_s.set_facecolor('#161B22')
    ax_s.plot(s_x, s_y, 'b--', alpha=0.6)
    ax_s.scatter(phi, 0.92 - 2*(phi - 0.5)**2, color='red', s=100, label="Votre Design")
    ax_s.set_xlabel("φ", color='white'); ax_s.set_ylabel("η", color='white')
    ax_s.tick_params(colors='white')
    st.pyplot(f_smith)
    

with t3:
    st.write(f"""
    L'augmentation de pression de **{(pi_is-1)*100:.1f}%** est réalisée par :
    1. **Le Rotor** : Conversion du travail en énergie cinétique et pression.
    2. **Le Stator** : Redressement du flux et transformation de l'énergie cinétique $C_2$ en pression statique.
    """)

st.divider()
st.caption("🚀 Développé par Dr FODIL - M1 GM | AxialFlow Pro v2.0")
