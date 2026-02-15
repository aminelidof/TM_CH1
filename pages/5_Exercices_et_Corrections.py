import streamlit as st

# --- STYLE CSS (Assurez-vous qu'il est défini en haut de votre fichier) ---
st.markdown("""
    <style>
    .exo-container { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 6px solid #1f497d; margin-bottom: 20px; }
    .corr-container { background-color: #e8f4ea; padding: 20px; border-radius: 10px; border-left: 6px solid #28a745; }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="TD Corrigés - Compresseurs Axiaux", layout="wide")

st.title("📝 Travaux Dirigés : Exercices & Solutions")
st.markdown("""
Cette section regroupe les exercices d'application directe du cours sur les compresseurs axiaux. 
Chaque solution est détaillée avec les rappels de formules nécessaires.
""")

# Style CSS pour l'esthétique des blocs
st.markdown("""
    <style>
    .exo-container { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 6px solid #1f497d; margin-bottom: 20px; }
    .corr-container { background-color: #e8f4ea; padding: 20px; border-radius: 10px; border-left: 6px solid #28a745; }
    </style>
""", unsafe_allow_html=True)

# --- EXERCICE 1 : THERMODYNAMIQUE ---
st.markdown('<div class="exo-container">', unsafe_allow_html=True)
st.subheader("Exercice 1 : État de sortie et Rendement")
st.write("""
Un étage de compresseur axial aspire de l'air aux conditions suivantes :  
- **P1** = 1 bar, **T1** = 290 K.  
- Le rapport de pression de l'étage est **π** = 1.3.  
- Le rendement isentropique de l'étage est **η_is** = 0.88.  
**Question :** Calculer la température réelle de sortie **T2** et le travail massique consommé ($c_p = 1005$ J/kg.K).
""")
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("👉 Voir la Correction Détaillée de l'Exercice 1"):
    st.markdown('<div class="corr-container">', unsafe_allow_html=True)
    st.markdown("### Solution :")
    st.write("1. **Température isentropique (théorique) :**")
    st.latex(r"T_{2is} = T_1 \cdot (\pi)^{\frac{\gamma-1}{\gamma}} = 290 \cdot (1.3)^{0.2857} \approx 312.6 \, K")
    st.write("2. **Température réelle (en utilisant le rendement) :**")
    st.latex(r"T_2 = T_1 + \frac{T_{2is} - T_1}{\eta_{is}} = 290 + \frac{312.6 - 290}{0.88} = 315.7 \, K")
    st.write("3. **Travail massique :**")
    st.latex(r"W = c_p (T_2 - T_1) = 1005 \cdot (315.7 - 290) = 25.82 \, kJ/kg")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# --- EXERCICE 2 : CINÉMATIQUE (TRIANGLES) ---
st.markdown('<div class="exo-container">', unsafe_allow_html=True)
st.subheader("Exercice 2 : Analyse des Vitesses (Euler)")
st.write("""
Pour un compresseur tournant à **N = 8000 tr/min** avec un rayon moyen de **0.3 m** :  
- La vitesse axiale est constante : **Ca** = 160 m/s.  
- L'angle de l'écoulement à l'entrée est **α1** = 15°.  
- L'angle de sortie absolu est **α2** = 45°.  
**Question :** Déterminer le travail fourni au fluide par l'équation d'Euler.
""")
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("👉 Voir la Correction Détaillée de l'Exercice 2"):
    st.markdown('<div class="corr-container">', unsafe_allow_html=True)
    import numpy as np
    # Calculs pour affichage dynamique
    U = (2 * np.pi * 8000 / 60) * 0.3
    Cw1 = 160 * np.tan(np.radians(15))
    Cw2 = 160 * np.tan(np.radians(45))
    W = U * (Cw2 - Cw1)
    
    st.write(f"1. **Vitesse périphérique (U) :** $U = \omega \cdot R = {U:.2f}$ m/s")
    st.write(f"2. **Composantes tangentielles :**")
    st.write(f"- $C_{{w1}} = C_a \tan(\\alpha_1) = 160 \cdot 0.267 = {Cw1:.2f}$ m/s")
    st.write(f"- $C_{{w2}} = C_a \tan(\\alpha_2) = 160 \cdot 1.0 = {Cw2:.2f}$ m/s")
    st.write("3. **Travail d'Euler :**")
    st.latex(r"W = U(C_{w2} - C_{w1})")
    st.success(f"**W = {W/1000:.2f} kJ/kg**")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# --- EXERCICE 3 : DEGRÉ DE RÉACTION ---
st.markdown('<div class="exo-container">', unsafe_allow_html=True)
st.subheader("Exercice 3 : Conception (Degré de Réaction)")
st.write("""
On considère un étage symétrique où le degré de réaction **R = 0.5**.  
On donne **U** = 250 m/s, **Ca** = 150 m/s et le travail de l'étage **W** = 30 kJ/kg.  
**Question :** Calculer les angles des aubes $\\beta_1$ et $\\beta_2$.
""")
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("👉 Voir la Correction Détaillée de l'Exercice 3"):
    st.markdown('<div class="corr-container">', unsafe_allow_html=True)
    st.write("Puisque **R = 0.5**, les triangles sont symétriques : $\\alpha_1 = \\beta_2$ et $\\beta_1 = \\alpha_2$.")
    st.write("1. **Différence des vitesses tangentielles :**")
    st.latex(r"\Delta C_w = \frac{W}{U} = \frac{30000}{250} = 120 \, m/s")
    st.write("2. **Pour R=0.5, on sait que :**")
    st.latex(r"C_{w1} + C_{w2} = U \implies C_{w1} = (U - \Delta C_w)/2 = 65 \, m/s")
    st.latex(r"C_{w2} = 185 \, m/s")
    st.write("3. **Calcul de l'angle relatif :**")
    st.latex(r"V_{w1} = U - C_{w1} = 185 \, m/s \implies \tan \beta_1 = \frac{185}{150} \implies \beta_1 \approx 51^\circ")
    st.markdown('</div>', unsafe_allow_html=True)

# --- EXERCICE 4 : GLISSEMENT (STANTZ) ---
st.write("---")
st.subheader("Exercice 4 : Facteur de Glissement")
st.markdown('<div class="exo-container">', unsafe_allow_html=True)
st.write("Un rotor de compresseur possède **Z = 32** aubes. En utilisant la formule de **Stantz** vue en cours, déterminez le facteur de glissement $\sigma_s$.")
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("👉 Voir la Correction"):
    st.latex(r"\sigma_s = 1 - \frac{2}{Z} = 1 - \frac{2}{32} = 0.9375")
    st.info("Ce facteur réduit le travail transféré car le fluide ne suit pas parfaitement l'angle de l'aube.")

# --- EXERCICE 5 : COEFFICIENT DE CHARGE ---
st.write("---")
st.subheader("📝 Exercice 5 : Coefficient de Charge ($\psi$)")
st.markdown('<div class="exo-container">', unsafe_allow_html=True)
st.write("""
À partir des données de l'exercice 2 :
- Travail massique : **W = 34 500 J/kg**
- Vitesse périphérique : **U = 251.3 m/s**

**Question :** Calculez le coefficient de température (ou coefficient de charge) $\psi$.
""")
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("👉 Voir la Correction"):
    st.markdown('<div class="corr-container">', unsafe_allow_html=True)
    st.write("Le coefficient de charge quantifie le travail fourni par l'étage par unité d'énergie cinétique du rotor :")
    st.latex(r"\psi = \frac{W}{U^2}")
    st.write("Calcul numérique :")
    st.latex(r"\psi = \frac{34500}{(251.3)^2} \approx 0.546")
    st.success(r"$\psi \approx 0.55$")
    st.info("💡 Un coefficient $\psi$ élevé indique un étage très chargé, ce qui peut réduire la plage de stabilité (risque de pompage).")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# --- SECTION : MÉTHODOLOGIE DE DIMENSIONNEMENT ---
st.header("🚀 Synthèse : Démarche de Dimensionnement")
st.markdown("""
Pour concevoir un étage de compresseur axial, les ingénieurs suivent cette séquence logique de calculs. 
Utilisez le simulateur ci-dessous pour tester vos propres valeurs.
""")

# Utilisation de colonnes pour organiser les formules
col_formule, col_interactive = st.columns([1, 1])

with col_formule:
    st.subheader("📚 Rappels Théoriques")
    
    # 1. Vitesse périphérique
    st.markdown("**1. Cinématique du Rotor**")
    st.latex(r"U = \omega \cdot r = \frac{2\pi N}{60} \cdot r")

    # 2. Travail et Déviation
    st.markdown("**2. Équation d'Euler**")
    st.write("Relie la géométrie des triangles de vitesses au travail :")
    st.latex(r"W = U \cdot \Delta C_w = U(C_{w2} - C_{w1})")

    # 3. Évolution des températures
    st.markdown("**3. Bilan Énergétique**")
    st.latex(r"\Delta T_0 = \frac{W}{c_p} \implies T_{02} = T_{01} + \frac{W}{c_p}")

    # 4. Évolution des pressions
    st.markdown("**4. Performances de Compression**")
    st.write("Rapport de pression de l'étage :")
    st.latex(r"\pi_e = \frac{P_{02}}{P_{01}} = \left[ 1 + \eta_{is} \frac{\Delta T_0}{T_{01}} \right]^{\frac{\gamma}{\gamma-1}}")



with col_interactive:
    st.subheader("⚙️ Calculateur Dynamique")
    
    # Paramètres de calcul
    cp = 1005  # J/kg.K
    gamma = 1.4
    
    # Entrées utilisateur
    W_input = st.number_input("Travail requis (W) [J/kg]", value=25000, step=500)
    T01_input = st.number_input("Température d'entrée (T01) [K]", value=288.15, step=1.0)
    eta_is = st.slider("Rendement isentropique (η_is)", 0.80, 0.95, 0.90)

    # Calculs
    delta_T = W_input / cp
    T02_calc = T01_input + delta_T
    rapport_p = (1 + eta_is * (delta_T / T01_input))**(gamma/(gamma-1))

    # Affichage des résultats "Pro"
    st.markdown("---")
    st.write("**Résultats calculés :**")
    st.metric("Augmentation de Température", f"{delta_T:.2f} K")
    st.metric("Température finale T02", f"{T02_calc:.2f} K")
    st.metric("Rapport de pression (π)", f"{rapport_p:.3f}")
    
    if rapport_p > 1.5:
        st.warning("⚠️ Ce rapport de pression est élevé pour un seul étage axial (risque de décrochage).")
    else:
        st.success("✅ Dimensionnement dans les standards industriels (1.2 - 1.5).")