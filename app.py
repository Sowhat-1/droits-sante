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

def rechercher_qwant(question):
    """Recherche via Qwant API (gratuit et illimité)"""
    try:
        # API non-officielle de Qwant
        url = f"https://api.qwant.com/api/search?q={urllib.parse.quote(question + ' Belgique')}&count=10&offset=0&device=desktop&safesearch=1&lang=fr_FR"
        
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Accept-Language': 'fr-FR,fr;q=0.9'
            }
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            results = []
            # Extraire les résultats web
            web_results = data.get('data', {}).get('web', {}).get('results', [])
            
            for item in web_results[:5]:
                title = item.get('title', 'Sans titre')
                desc = item.get('desc', '')
                url = item.get('url', '#')
                results.append(f"**{title}**\n{desc}\n🔗 [Voir]({url})")
            
            return results if results else ["Aucun résultat trouvé."]
            
    except Exception as e:
        return [f"Erreur : {e}"]

if menu == "🏠 Accueil":
    st.header("Bienvenue")
    st.markdown("### Recherche illimitée via Qwant")

elif menu == "🔍 Recherche en direct":
    st.header("🔍 Recherche")
    st.success("✅ API Qwant - Gratuit et illimité")
    
    question = st.text_input("Votre question :")
    if st.button("🔎 Rechercher", type="primary"):
        if question:
            with st.spinner("Recherche..."):
                for res in rechercher_qwant(question):
                    st.markdown(res)
                    st.markdown("---")

# ... reste du code
