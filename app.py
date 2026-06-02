import streamlit as st
import urllib.request
import urllib.parse
import json
from datetime import datetime

st.set_page_config(page_title="Droits de Santé Belgique", page_icon="🏥", layout="wide")

st.title("🏥 Droits de Santé en Belgique")
st.markdown("---")

st.sidebar.title("Navigation")
menu = st.sidebar.radio("Choisissez une section :", ["🏠 Accueil", "🔍 Recherche en direct", "📋 Mes droits INAMI", "ℹ️ À propos"])

def rechercher_web(question):
    """Recherche via SearXNG (API publique gratuite)"""
    try:
        # On utilise une instance publique de SearXNG
        url = f"https://searx.be/search?q={urllib.parse.quote(question)}&format=json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            results = []
            for item in data.get('results', [])[:5]:
                title = item.get('title', 'Sans titre')
                content = item.get('content', '')
                link = item.get('url', '#')
                results.append(f"**{title}**\n{content}\n🔗 [Voir la source]({link})")
            
            return results if results else ["Aucun résultat trouvé."]
            
    except Exception as e:
        return [f"Erreur de connexion : {e}"]

if menu == "🏠 Accueil":
    st.header("Bienvenue sur votre guide des droits de santé")
    st.markdown("""
    ### Cette application vous aide à comprendre vos droits en matière de santé en Belgique.
    **Ce que vous pouvez faire ici :**
    - 🔍 **Rechercher en direct** : Posez une question et obtenez des réponses actualisées.
    - 📋 **Consulter vos droits** : Informations sur l'INAMI, remboursements, etc.
    
    ⚠️ *Les informations sont à titre indicatif.*
    """)

elif menu == "🔍 Recherche en direct":
    st.header("🔍 Recherche d'informations en temps réel")
    question = st.text_input("Votre question :", placeholder="Ex: Montant forfait palliatif INAMI")
    
    if st.button("🔎 Rechercher", type="primary"):
        if question:
            with st.spinner("Recherche en cours..."):
                resultats = rechercher_web(question)
                st.markdown("---")
                for res in resultats:
                    st.markdown(res)
                    st.markdown("---")
        else:
            st.warning("Veuillez entrer une question.")

elif menu == "📋 Mes droits INAMI":
    st.header("📋 Vos droits selon l'INAMI")
    st.markdown("""
    ### 🔹 Soins de santé de base
    - **Médecin généraliste** : Remboursement de 75%
    - **Spécialiste** : Remboursement variable
    - **Médicaments** : Catégories A, B, C
    """)

elif menu == "ℹ️ À propos":
    st.header("ℹ️ À propos")
    st.markdown(f"Mis à jour le : {datetime.now().strftime('%d/%m/%Y')}")

st.markdown("---")
st.caption("🏥 Droits de Santé Belgique")
