import streamlit as st
import urllib.request
import urllib.parse
import json
import random
from datetime import datetime

st.set_page_config(page_title="Droits de Santé Belgique", page_icon="🏥", layout="wide")

st.title("🏥 Droits de Santé en Belgique")
st.markdown("---")

st.sidebar.title("Navigation")
menu = st.sidebar.radio("Choisissez une section :", ["🏠 Accueil", "🔍 Recherche en direct", "📋 Mes droits INAMI", "ℹ️ À propos"])

# Liste d'instances SearXNG publiques (gratuites et illimitées)
SEARXNG_INSTANCES = [
    "https://searx.be",
    "https://searx.info",
    "https://search.bus-hit.me",
    "https://searx.network",
    "https://search.trom.tf"
]

def rechercher_web(question):
    """Recherche via instances SearXNG publiques (gratuit et illimité)"""
    
    # Mélanger les instances pour essayer dans un ordre aléatoire
    instances = SEARXNG_INSTANCES.copy()
    random.shuffle(instances)
    
    for instance in instances:
        try:
            # Requête avec filtres pour la Belgique
            query = f"{question} Belgique site:inami.fgov.be OR site:sante.belgique.be"
            url = f"{instance}/search?q={urllib.parse.quote(query)}&format=json&language=fr"
            
            req = urllib.request.Request(
                url, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                    'Accept': 'application/json'
                }
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                results = []
                for item in data.get('results', [])[:5]:
                    title = item.get('title', 'Sans titre')
                    content = item.get('content', '')
                    url_result = item.get('url', '#')
                    
                    results.append(f"**{title}**\n{content}\n🔗 [Voir]({url_result})")
                
                if results:
                    return results
                    
        except Exception as e:
            # Essayer l'instance suivante
            continue
    
    return ["Aucun résultat trouvé. Les serveurs de recherche sont temporairement indisponibles."]

if menu == "🏠 Accueil":
    st.header("Bienvenue sur votre guide des droits de santé")
    st.markdown("""
    ### Recherche illimitée et gratuite
    
    **Sources :** INAMI, SPF Santé Belgique, mutuelles
    
    ✅ **100% gratuit** - **Illimité** - **Sources officielles**
    
    ⚠️ *Informations à titre indicatif.*
    """)

elif menu == "🔍 Recherche en direct":
    st.header("🔍 Recherche d'informations")
    st.success("✅ Recherche illimitée et gratuite via SearXNG")
    
    question = st.text_input("Votre question :", placeholder="Ex: Forfait palliatif INAMI")
    
    if st.button("🔎 Rechercher", type="primary"):
        if question:
            with st.spinner("Recherche en cours sur les sites officiels..."):
                resultats = rechercher_web(question)
                st.markdown("---")
                for res in resultats:
                    st.markdown(res)
                    st.markdown("---")
        else:
            st.warning("Veuillez entrer une question.")

elif menu == "📋 Mes droits INAMI":
    st.header("📋 Vos droits")
    st.markdown("""
    - **Médecin généraliste** : 75% remboursés
    - **Kinésithérapie** : Sur prescription
    - **Médicaments** : Catégories A, B, C
    """)

elif menu == "ℹ️ À propos":
    st.header("ℹ️ À propos")
    st.markdown(f"Mis à jour : {datetime.now().strftime('%d/%m/%Y')}")

st.markdown("---")
st.caption("🏥 Droits de Santé Belgique - Recherche illimitée")
