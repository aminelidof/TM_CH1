import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- 1. CONFIGURATION ET STYLE HAUTE VISIBILITÉ ---
st.markdown("""
    <style>
    /* Global Dark Theme */
    [data-testid="stAppViewContainer"] { background-color: #0E1117; }
    
    /* Titre Principal Stylisé */
    .main-header { 
        font-size: 32px; 
        color: #58A6FF; 
        font-weight: 800; 
        text-align: center;
        border-bottom: 2px solid #30363D;
        padding-bottom: 15px;
        margin-bottom: 25px;
    }

    /* Cartes de Metrics High-Contrast */
    div[data-testid="stMetric"] {
        background-color: #161B22 !important;
        border: 1px solid #30363D !important;
        border-top: 4px solid #58A6FF !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    div[data-testid="stMetricLabel"] > div { color: #8B949E !important; font-size: 13px !important; font-weight: bold; }
    div[data-testid="stMetricValue"] > div { color: #FFFFFF !important; font-size: 26px !important; }

    /* Zone de Calcul LaTeX */
    .calc-container {
        background-color: #1C2128;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #30363D;
        margin-top: 10px;
    }
    h4 { color: #58A6FF !important; margin-top: 20px !important; border-left: 4px solid #58A6FF; padding-left: 10px; }
    
    /* Style des onglets */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #161B22;
        border-radius: 5px 5px 0 0;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. LOGIQUE DE CALCUL (BACKEND) ---
with st.sidebar:
    st.markdown("### 🛠️ Bureau d'Études")
    with st.expander("🚀 Géométrie & Cinématique", expanded=True):
        U = st.slider("Vitesse périphérique (U) [m/s]", 100, 650, 320)
        Ca = st.slider("Vitesse axiale (Ca) [m/s]", 50, 350, 160)
        alpha1 = st.slider("Angle d'injection (α1) [°]", 0, 45, 12)
        beta2 = st.slider("Angle de sortie relatif (β2) [°]", 10, 65, 42)

    with st.expander("🌡️ Conditions Ambiantes"):
        T01 = st.number_input("Température totale entrée (T01) [K]", value=288.15)
        P01 = st.number_input("Pression totale entrée (P01) [bar]", value=1.01325)
        Cp, gamma, R = 1004.5, 1.4, 287.05

# --- MOTEUR DE CALCUL ---
a1_rad, b2_rad = np.radians(alpha1), np.radians(beta2)

# Station 1
Cw1 = Ca * np.tan(a1_rad)
Vw1 = U - Cw1
V1 = np.sqrt(Ca**2 + Vw1**2)
beta1 = np.degrees(np.arctan2(Vw1, Ca))

# Station 2
Vw2 = Ca * np.tan(b2_rad)
Cw2 = U - Vw2
V2 = np.sqrt(Ca**2 + Vw2**2)
alpha2 = np.degrees(np.arctan2(Cw2, Ca))

# Thermodynamique
W_euler = U * (Cw2 - Cw1)
delta_T0 = W_euler / Cp
pi_is = ( (T01 + delta_T0) / T01 )**(gamma/(gamma-1))
phi, psi = Ca / U, W_euler / (U**2)

# --- 3. AFFICHAGE : DASHBOARD SUPÉRIEUR ---
st.markdown('<p class="main-header">🌀 AxialFlow Pro : Analyse de l\'Étage</p>', unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Travail Euler", f"{W_euler/1000:.2f} kJ/kg")
m2.metric("Rapport Pression π", f"{pi_is:.3f}")
m3.metric("Saut Temp. ΔT0", f"{delta_T0:.2f} K")
m4.metric("Coeff. Charge ψ", f"{psi:.2f}")
m5.metric("Coeff. Débit φ", f"{phi:.2f}")

st.write("")

# --- 4. CŒUR DE LA PAGE : TRIANGLES ET CALCULS DÉTAILLÉS ---
col_left, col_right = st.columns([1.3, 1])

with col_left:
    st.subheader("📐 Visualisation des Triangles de Vitesses")
    
    # Dessin Matplotlib avec thème sombre
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), facecolor='#0E1117')
    
    def plot_tri(ax, u, ca, cw, title, c_color, v_color):
        ax.set_facecolor('#161B22')
        # Vecteurs
        ax.quiver(0, 0, u, 0, angles='xy', scale_units='xy', scale=1, color='white', label='U (Entraînement)', width=0.01)
        ax.quiver(0, 0, cw, ca, angles='xy', scale_units='xy', scale=1, color=c_color, label='C (Absolu)', width=0.015)
        ax.quiver(u, 0, cw-u, ca, angles='xy', scale_units='xy', scale=1, color=v_color, label='V (Relatif)', width=0.012)
        
        ax.set_title(title, color='#58A6FF', fontsize=14, fontweight='bold')
        ax.set_xlim(-50, max(u, cw) + 100)
        ax.set_ylim(-20, ca + 100)
        ax.axis('off')
        ax.legend(loc='upper right', fontsize='small', facecolor='#0E1117', labelcolor='white')

    plot_tri(ax1, U, Ca, Cw1, "Entrée (Station 1)", "#58A6FF", "#FFA657")
    plot_tri(ax2, U, Ca, Cw2, "Sortie (Station 2)", "#7EE787", "#FF7B72")
    
    st.pyplot(fig)
    

    # Stabilité Industrielle
    st.markdown("### 🛡️ Diagnostic de Stabilité")
    s1, s2 = st.columns(2)
    with s1:
        haller = V2 / V1
        st.write(f"**Facteur de Haller :** `{haller:.3f}`")
        if haller < 0.72: st.error("❌ Décollement critique")
        else: st.success("✅ Diffusion saine")
    with s2:
        df = (1 - V2/V1) + (abs(Cw2 - Cw1) / (2 * 1.5 * V1))
        st.write(f"**D-Factor :** `{df:.3f}`")
        if df > 0.55: st.error("❌ Surcharge d'aube")
        else: st.success("✅ Charge optimale")

with col_right:
    st.subheader("🏁 Expertise et Démonstration")
    st.markdown('<div class="calc-container">', unsafe_allow_html=True)
    
    # ÉTAPE 1
    st.markdown("#### 1. Transfert de Travail ($W$)")
    st.latex(rf"C_{{w1}} = {Ca} \cdot \tan({alpha1}^\circ) = {Cw1:.1f} \, m/s")
    st.latex(rf"C_{{w2}} = {U} - ({Ca} \cdot \tan({beta2}^\circ)) = {Cw2:.1f} \, m/s")
    st.latex(rf"W = U \cdot (C_{{w2}} - C_{{w1}}) = {W_euler:.1f} \, J/kg")
    
    # ÉTAPE 2
    st.markdown("#### 2. Saut de Température ($\Delta T_0$)")
    st.write("Calcul via le premier principe :")
    st.latex(rf"\Delta T_0 = \frac{{W}}{{c_p}} = \frac{{{W_euler:.1f}}}{{{Cp}}} = {delta_T0:.2f} \, K")
    
    # ÉTAPE 3
    st.markdown("#### 3. Taux de Pression ($\pi$)")
    st.latex(rf"\pi_{{is}} = \left( \frac{{{T01:.1f} + {delta_T0:.2f}}}{{{T01:.1f}}} \right)^{{3.5}} = {pi_is:.3f}")
    st.info(f"Augmentation de pression : **{(pi_is-1)*100:.1f} %**")

    # ÉTAPE 4
    st.markdown("#### 4. Diagnostic de Compressibilité")
    a1 = np.sqrt(gamma * R * T01)
    Mv1 = V1 / a1
    st.latex(rf"a_1 = \sqrt{{\gamma R T_{{01}}}} = {a1:.1f} \, m/s")
    st.latex(rf"M_{{v1}} = \frac{{V_1}}{{a_1}} = {Mv1:.2f}")

    if Mv1 > 0.9:
        st.error(f"🚨 **Régime Transsonique** (M={Mv1:.2f}). Ondes de choc probables.")
    elif Mv1 > 0.7:
        st.warning(f"⚠️ **Régime Subsonique élevé**. Pertes de compressibilité.")
    else:
        st.success(f"✅ **Régime Subsonique**. Rendement optimal.")

    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. FOOTER ---
st.divider()
st.caption("AxialFlow Pro | Logiciel Académique | Dr. FODIL | Master 1 Génie Mécanique")
