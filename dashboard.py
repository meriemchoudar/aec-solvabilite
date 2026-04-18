import streamlit as st
import pandas as pd

# Configuration et Style
st.set_page_config(page_title="AEC Dashboard - Système Expert", layout="wide")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('MAPINFO_SISMIQUE (1).csv')
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

df = load_data()

if df is not None:
    st.title("🛡️ Dashboard AEC : Interface de Souscription (Logique UML)")
    st.markdown("---")

    # 1. ENTITÉ : LOCALISATION (SIG)
    st.sidebar.header("📍 Entité : Localisation")
    commune_select = st.sidebar.selectbox("Commune du Risque", sorted(df['COMMUNE_CLEAN'].unique()))
    data = df[df['COMMUNE_CLEAN'] == commune_select].iloc[0]

    # 2. ENTITÉ : BÂTIMENT (Caractéristiques IA & RPA)
    st.header("🏠 Caractéristiques du Bâtiment")
    c1, c2, c3 = st.columns(3)
    with c1:
        age_bat = st.number_input("Âge du Bâtiment (IA)", 0, 150, 20)
    with c2:
        usage = st.selectbox("Usage", ["Habitation", "Commercial", "Industriel"])
    with c3:
        conforme_rpa = st.radio("Conformité RPA (Technique)", ("OUI", "NON"))

    # --- MOTEUR DE DÉCISION (INTERSECTION DES ENTITÉS) ---
    st.markdown("---")
    st.subheader("⚖️ Analyse de Risque & Arbitrage Réassurance")

    classe_sig = str(data['CLASSE_COMMUNE']).upper()
   
    # Initialisation des variables de décision
    decision = ""
    reassurance = ""
    couleur = "info"

    # LOGIQUE CUMULATIVE DES FILTRES (UML Decision Logic)
   
    # Filtre de Ruine (SIG + IA)
    if 'SURCONCENTRATION' in classe_sig and age_bat > 40:
        decision = "REFUS SYSTÉMATIQUE OU CESSION 100% OBLIGATOIRE"
        reassurance = "Cession Facultative : 100% au Réassureur"
        couleur = "error"
        motif = "Cumul critique de capitaux et obsolescence structurelle."

    # Filtre de Conformité (RPA)
    elif conforme_rpa == "NON":
        paye_surprime = st.radio("Le client accepte-t-il la surprime pour non-conformité ?", ("OUI", "NON"))
        if paye_surprime == "OUI":
            decision = "ACCORD SOUS RÉSERVE : TARIF ADDITIF + MAINTENANCE"
            reassurance = "Partage différencié : 90% Réassureur / 10% Assureur"
            couleur = "warning"
            motif = "Bâtiment hors-norme compensé par une tarification technique."
        else:
            decision = "REFUS DE SOUSCRIPTION"
            reassurance = "Aucun transfert possible"
            couleur = "error"
            motif = "Refus du client de couvrir le surcoût du risque technique."

    # Filtre Nominal (Zone saine & Conforme)
    else:
        if 'SURCONCENTRATION' in classe_sig:
            decision = "ACCEPTATION AVEC SURPRIME DE CONCENTRATION (10%)"
            reassurance = "Cession Traité : 70% Réassureur / 30% Assureur"
            couleur = "warning"
            motif = "Bâtiment sain mais zone géographiquement saturée."
        else:
            decision = "ACCEPTATION DIRECTE - RÉTENTION OPTIMISÉE"
            reassurance = "Conservation GAM : 50% / Cession : 50%"
            couleur = "success"
            motif = "Risque conforme en zone de développement."

    # Affichage du Verdict
    if couleur == "error": st.error(f"**Décision : {decision}**")
    elif couleur == "warning": st.warning(f"**Décision : {decision}**")
    else: st.success(f"**Décision : {decision}**")

    st.write(f"**Stratégie de Réassurance :** {reassurance}")
    st.write(f"**Justification :** {motif}")

    # Section Solvabilité (Rappel Monte Carlo)
    with st.expander("📊 Analyse de Solvabilité (Fonds Propres)"):
        st.write(f"Capital total engagé sur {commune_select} : {float(data['capital_total']):,.2f} DA")
        st.progress(min(float(data['capital_total']) / 5000000000, 1.0))
        st.caption("Ratio d'exposition par rapport aux fonds propres (5 Mds DA)")
