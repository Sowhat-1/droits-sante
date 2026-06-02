import streamlit as st
import urllib.request
import urllib.parse
import re
from datetime import datetime

st.set_page_config(page_title="Droits de Santé Belgique", page_icon="🏥", layout="wide")

st.title("🏥 Droits de Santé en Belgique")
st.markdown("---")

st.sidebar.title("Navigation")
menu = st.sidebar.radio("Choisissez une section :", [" Accueil", "🔍 Recherche en direct", "📋 Mes droits INAMI", "ℹ️ À propos"])

def rechercher_web(question):
    try:
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(question)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            snippets = re.findall(r'class="result__snippet[^>]*>(.*?)</a>', html, re.DOTALL)
            return [re.sub(r'<[^>]+>', '', s).strip() for s in snippets[:5] if re.sub(r'<[^>]+>', '', s).strip()]
    except Exception as e:
        return [f"Erreur: {e}"]

if menu == "🏠 Accueil":
    st.header("Bienvenue sur votre guide des droits de santé")
    st.markdown("""
    ### Cette application vous aide à comprendre vos droits en matière de santé en Belgique.
    **Ce que vous pouvez faire ici :**
    - 🔍 **Rechercher en direct** : Posez une question et obtenez des réponses actualisées.
    -  **Consulter vos droits** : Informations sur l'INAMI, remboursements, etc.
    
    ⚠️ *Les informations sont à titre indicatif. Consultez toujours un professionnel de santé.*
    """)

elif menu == "🔍 Recherche en direct":
    st.header("🔍 Recherche d'informations en temps réel")
    question = st.text_input("Votre question :", placeholder="Ex: Remboursement consultation généraliste")
    if st.button("🔎 Rechercher", type="primary"):
        if question:
            with st.spinner("Recherche en cours..."):
                resultats = rechercher_web(question)
                st.success(f"✅ {len(resultats)} résultats trouvés !")
                for i, res in enumerate(resultats, 1):
                    st.markdown(f"**{i}.** {res}")
                    st.markdown("---")
        else:
            st.warning("Veuillez entrer une question.")

elif menu == "📋 Mes droits INAMI":
    st.header("📋 Vos droits selon l'INAMI")
    st.markdown("""
    ### 🔹 Soins de santé de base
    - **Médecin généraliste** : Remboursement de 75% (ticket modérateur de 25%)
    - **Spécialiste** : Remboursement variable selon la convention
    - **Médicaments** : Catégories A, B, C avec taux différents
    
    ### 🔹 Hospitalisation
    - Forfait journalier à charge du patient
    - Remboursement des frais médicaux selon le type de chambre
    """)

elif menu == "ℹ️ À propos":
    st.header("ℹ️ À propos")
    st.markdown(f"Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y')}")

st.markdown("---")
st.caption("🏥 Droits de Santé Belgique | Application informative")
