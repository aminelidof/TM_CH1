import streamlit as st

st.set_page_config(page_title="2. Analyse Thermodynamique - M1 GM", layout="wide")

# Titre Principal avec style
st.markdown('<h1 style="color:#1F497D;">🔥 Analyse Thermodynamique de l\'Étage</h1>', unsafe_allow_html=True)

st.markdown("""
L'analyse thermodynamique d'un étage de compresseur axial repose sur le **Premier Principe de la Thermodynamique** appliqué en système ouvert. 
On étudie ici le transfert d'énergie entre les aubages et le fluide (air).
""")

# --- SECTION A : BILAN ÉNERGÉTIQUE ET EULER ---
st.header("A. Bilans d'Énergie et Équation d'Euler")
col1, col2 = st.columns([1.5, 1])

with col1:
    st.write("""
    Pour un compresseur axial, l'écoulement est supposé adiabatique ($q=0$). 
    Le travail fourni par le rotor est égal à la variation de l'**enthalpie d'arrêt** ($h_0$) du fluide.
    """)
    st.latex(r"W = \Delta h_0 = h_{02} - h_{01} = c_p (T_{02} - T_{01})")
    
    st.write("**Équation d'Euler (Forme Cinématique) :**")
    st.write(r"Comme les rayons d'entrée et de sortie sont sensiblement identiques ($U_1 \approx U_2 = U$) :")
    st.latex(r"W = U(C_{w2} - C_{w1}) = U \cdot \Delta C_w")
    
    st.info("💡 **Physique du transfert** : Le rotor augmente la vitesse absolue du fluide, ce qui accroît son énergie cinétique, ensuite convertie en pression dans le stator.")

with col2:
    st.markdown("### 📊 États de Stagnation")
    st.write("Rappel des grandeurs d'arrêt :")
    st.latex(r"T_0 = T + \frac{C^2}{2 c_p}")
    st.latex(r"P_0 = P \left( \frac{T_0}{T} \right)^{\frac{\gamma}{\gamma-1}}")

st.write("---")

# --- SECTION B : PARAMÈTRES ADIMENSIONNELS (COEFFICIENTS) ---
st.header("B. Critères de Performance et Coefficients de Design")
st.write("Ces coefficients permettent de comparer des machines de tailles différentes.")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("#### 1. Coefficient de Charge ($\psi$)")
    st.write("Aussi appelé coefficient de température. Il mesure le travail spécifique par unité d'énergie cinétique du rotor.")
    st.latex(r"\psi = \frac{\Delta h_0}{U^2} = \frac{c_p \Delta T_0}{U^2}")
    st.caption("Standard industriel : 0.3 < ψ < 0.5")

with c2:
    st.markdown("#### 2. Coefficient de Débit ($\phi$)")
    st.write("Rapport entre la vitesse axiale (flux) et la vitesse d'entraînement.")
    st.latex(r"\phi = \frac{C_a}{U}")
    st.caption("Standard industriel : 0.4 < φ < 0.8")

with c3:
    st.markdown("#### 3. Facteur de Glissement ($\sigma_s$)")
    st.write("Prend en compte l'inertie du fluide qui ne suit pas parfaitement l'angle de l'aube.")
    st.latex(r"\sigma_s = 1 - \frac{2}{Z}")
    st.write("D'après **Stantz**, le travail réel devient :")
    st.latex(r"W_{réel} = \sigma_s \cdot W_{idéal}")

st.write("---")

# --- SECTION C : RENDEMENTS ET PERTES (LE COEUR DU M1) ---
st.header("C. Étude du Rendement et des Pertes")

tab1, tab2 = st.tabs(["📉 Rendement Isentropique", "📈 Rendement Polytropique"])

with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Définition :** Rapport entre le travail idéal (isentropique) et le travail réel fourni.")
        st.latex(r"\eta_{is} = \frac{h_{02s} - h_{01}}{h_{02} - h_{01}} = \frac{\pi_e^{\frac{\gamma-1}{\gamma}} - 1}{\frac{T_{02}}{T_{01}} - 1}")
    with col_b:
        st.write("**Diagramme h-s (Enthalpie-Entropie)**")
        st.info("🔍 Visualisation : La compression réelle s'accompagne d'une augmentation d'entropie due aux frottements, décalant le point de sortie vers la droite.")

with tab2:
    st.write("**Pourquoi le rendement polytropique ($\eta_p$) ?**")
    st.write("""
    Dans un compresseur multi-étagé, le rendement isentropique diminue artificiellement à cause de l'effet de réchauffage. 
    Le rendement polytropique représente le rendement 'infinitésimal' constant pour chaque étage.
    """)
    st.latex(r"\eta_p = \frac{\gamma-1}{\gamma} \cdot \frac{\ln(P_2/P_1)}{\ln(T_2/T_1)}")
    st.success("🎯 C'est la valeur de référence pour le design préliminaire en bureau d'études.")

# --- SECTION D : ANALYSE DES PERTES ---
st.subheader("🧱 Origine des Pertes Thermodynamiques")
st.markdown("""
1. **Pertes de Profil** : Frottement de la couche limite sur les parois des aubes (viscosité).
2. **Pertes Secondaires** : Tourbillons créés aux jonctions entre l'aube et le carter/moyeu.
3. **Pertes de Jeu (Tip Leakage)** : Fuite du fluide entre le sommet de l'aube mobile et le carter fixe.
4. **Pertes par Choc** : Apparaissent dès que la vitesse relative $V$ devient transsonique ($Ma_{rel} > 0.8$).
""")

st.write("---")
st.caption("Support de cours Master 1 GM - Dr FODIL - Université de Maghnia")