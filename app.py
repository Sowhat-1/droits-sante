import streamlit as st
from duckduckgo_search import DDGS
from datetime import datetime

st.set_page_config(page_title="Droits de Santé Belgique", page_icon="🏥", layout="wide")

st.title("🏥 Droits de Santé en Belgique")
st.markdown("---")

st.sidebar.title("Navigation")
menu = st.sidebar.radio("Choisissez une section :", ["🏠 Accueil", "🔍 Recherche en direct", "📋 Mes droits INAMI", "ℹ️ À propos"])

def rechercher_web(question):
    """Recherche gratuite et illimitée via la librairie DDGS"""
    try:
        with DDGS() as ddgs:
            # On cherche les 5 meilleurs résultats
            results = list(ddgs.text(question, max_results=5))
            if results:
                return [f" {r['title']}\n{r['body']}\n🔗 {r['href']}" for r in results]
            else:
                return ["Aucun résultat trouvé pour cette question."]
    except Exception as e:
        return [f"Erreur lors de la recherche : {e}"]

if menu == "🏠 Accueil":
    st.header("Bienvenue sur votre guide des droits de santé")
    st.markdown("""
    ### Cette application vous aide à comprendre vos droits en matière de santé en Belgique.
    **Ce que vous pouvez faire ici :**
    - 🔍 **Rechercher en direct** : Posez une question et obtenez des réponses actualisées depuis Internet.
    - 📋 **Consulter vos droits** : Informations sur l'INAMI, remboursements, etc.
    
    ⚠️ *Les informations sont à titre indicatif. Consultez toujours un professionnel de santé.*
    """)

elif menu == " Recherche en direct":
    st.header(" Recherche d'informations en temps réel")
    question = st.text_input("Votre question :", placeholder="Ex: Montant forfait palliatif INAMI")
    if st.button("🔎 Rechercher", type="primary"):
        if question:
            with st.spinner("Recherche en cours..."):
                resultats = rechercher_web(question)
                st.success("✅ Résultats trouvés !")
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
    - **Médecin généraliste** : Remboursement de 75% (ticket modérateur de 25%)
    - **Spécialiste** : Remboursement variable selon la convention
    - **Médicaments** : Catégories A, B, C avec taux différents
    """)

elif menu == "ℹ️ À propos":
    st.header("ℹ️ À propos")
    st.markdown(f"Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y')}")

st.markdown("---")
st.caption("🏥 Droits de Santé Belgique | Application informative")
