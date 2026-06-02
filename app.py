import streamlit as st
import urllib.request
import urllib.parse
import json
import re
from datetime import datetime

st.set_page_config(page_title="Droits de Santé Belgique", page_icon="🏥", layout="wide")

st.title("🏥 Droits de Santé en Belgique")
st.markdown("---")

st.sidebar.title("Navigation")
menu = st.sidebar.radio("Choisissez une section :", ["🏠 Accueil", "🔍 Recherche en direct", "📋 Mes droits INAMI", "ℹ️ À propos"])

def rechercher_sites_officiels(question):
    """Recherche ciblée sur les sites officiels belges"""
    try:
        # On ajoute des filtres pour chercher uniquement sur les sites officiels
        query = f"{question} (site:inami.fgov.be OR site:sante.belgique.be OR site:myhealth.be OR site:cz.be OR site:anmc.be)"
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
            
            # Extraction des résultats
            results = []
            # Chercher les titres et extraits
            titles = re.findall(r'class="result__a"[^>]*>(.*?)</a>', html, re.DOTALL)
            snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
            urls = re.findall(r'class="result__url"[^>]*href="([^"]+)"', html)
            
            for i in range(min(5, len(titles))):
                title = re.sub(r'<[^>]+>', '', titles[i]).strip() if i < len(titles) else "Sans titre"
                snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip() if i < len(snippets) else ""
                link = urls[i] if i < len(urls) else "#"
                
                if title and snippet:
                    results.append(f"**{title}**\n{snippet}\n🔗 [Source officielle]({link})")
            
            return results if results else ["Aucun résultat trouvé sur les sites officiels. Essayez une autre formulation."]
            
    except Exception as e:
        return [f"Erreur de recherche : {e}"]

if menu == "🏠 Accueil":
    st.header("Bienvenue sur votre guide des droits de santé")
    st.markdown("""
    ### Cette application vous aide à comprendre vos droits en matière de santé en Belgique.
    
    **Sources officielles recherchées :**
    - 🏛️ **INAMI** (inami.fgov.be) - Institut national d'assurance maladie-invalidité
    - 🏥 **SPF Santé** (sante.belgique.be) - Service public fédéral
    - 💊 **MyHealth** (myhealth.be) - Portail santé belge
    - 🏦 **Mutuelles** (cz.be, anmc.be, etc.)
    
    ⚠️ *Les informations sont à titre indicatif. Consultez toujours un professionnel de santé.*
    """)

elif menu == "🔍 Recherche en direct":
    st.header("🔍 Recherche sur les sites officiels belges")
    st.success("✅ Cette recherche cible uniquement les sources officielles belges (INAMI, SPF Santé, mutuelles)")
    
    question = st.text_input(
        "Votre question :", 
        placeholder="Ex: Remboursement kinésithérapie INAMI",
        help="Posez votre question sur les droits de santé en Belgique"
    )
    
    if st.button("🔎 Rechercher", type="primary"):
        if question:
            with st.spinner("Recherche sur les sites officiels..."):
                resultats = rechercher_sites_officiels(question)
                st.markdown("---")
                for res in resultats:
                    st.markdown(res)
                    st.markdown("---")
        else:
            st.warning("Veuillez entrer une question.")
    
    st.markdown("---")
    st.markdown("### 💡 Exemples de questions :")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Forfait palliatif INAMI"):
            st.session_state.question = "Forfait palliatif INAMI"
            st.rerun()
    with col2:
        if st.button("Remboursement médecin généraliste"):
            st.session_state.question = "Remboursement médecin généraliste Belgique"
            st.rerun()

elif menu == "📋 Mes droits INAMI":
    st.header("📋 Vos droits selon l'INAMI")
    st.markdown("""
    ### 🔹 Soins de santé de base
    - **Médecin généraliste** : 75% remboursés (ticket modérateur 25%)
    - **Spécialiste** : Variable selon convention
    - **Médicaments** : 
      - Catégorie A : 100% remboursé
      - Catégorie B : 50-75% remboursé
      - Catégorie C : 20-50% remboursé
    
    ### 🔹 Kinésithérapie
    - Sur prescription médicale obligatoire
    - Séances remboursées selon pathologie
    - Maximum par année selon l'affection
    
    ### 🔹 Hospitalisation
    - Forfait journalier à charge du patient
    - Remboursement selon type de chambre
    - Franchise hospitalière applicable
    """)

elif menu == "ℹ️ À propos":
    st.header("ℹ️ À propos")
    st.markdown("""
    ### Sources officielles
    Cette application recherche exclusivement sur les sites officiels belges :
    - INAMI (inami.fgov.be)
    - SPF Santé Publique (sante.belgique.be)
    - Mutuelles belges
    
    ### Limitations
    - Les informations sont à titre indicatif
    - Consultez toujours un professionnel de santé
    - Vérifiez toujours sur les sites officiels pour les montants exacts
    """)
    st.markdown(f"\n**Dernière mise à jour :** {datetime.now().strftime('%d/%m/%Y')}")

st.markdown("---")
st.caption("🏥 Droits de Santé Belgique | Sources officielles uniquement")
