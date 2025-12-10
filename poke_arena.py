import streamlit as st
import json
from groq import Groq

# Config
st.set_page_config(
    page_title="PokéArena - Le Duel de Données",
    page_icon="PA",
    layout="wide",
)

# Sidebar
st.sidebar.title("Paramètres de l'arène")

groq_api_key = st.sidebar.text_input(
    "Clé API Groq",
    type="password",
    placeholder="Colle ici ta clé API",
)

st.sidebar.markdown("---")

terrain = st.sidebar.selectbox(
    "Terrain de combat",
    options=[
        "Volcan",
        "Océan",
        "Forêt",
        "Champ",
        "Désert",
        "Espace",
    ],
    index=0,
    help="Le terrain influencera le déroulement du combat dans le récit."
)

# Convert JSON to Python dictionary
def parse_champion_json(json_text: str, label: str):
    if not json_text.strip():
        return None

    try:
        data = json.loads(json_text)

        if not isinstance(data, dict):
            st.error(f"{label} : le JSON doit représenter un dictionnaire, pas une liste ou un autre type.")
            return None

        return data

    except json.JSONDecodeError:
        st.error(f"{label} : JSON invalide. Vérifie la syntaxe (guillemets, virgules, accolades...).")
        return None


st.sidebar.info(
    "Colle les JSON de ton champion et de son adversaire dans la page principale, "
    "puis lance le combat."
)

def simuler_combat(champion_1_data: dict, champion_2_data: dict, terrain: str, api_key: str) -> str:
    client = Groq(api_key=api_key)

    champion_1_json = json.dumps(champion_1_data, ensure_ascii=False, indent=2)
    champion_2_json = json.dumps(champion_2_data, ensure_ascii=False, indent=2)

    system_prompt = (
        "Tu es à la fois un commentateur sportif épique et un arbitre impartial dans une arène de combat Pokémon.\n"
        "On va te fournir les fiches techniques de deux combattants au format JSON, ainsi que le terrain de combat.\n\n"
        "Règles importantes :\n"
        "- Tu dois analyser les Types, les Descriptions, la Personnalité et les Stats des deux combattants.\n"
        "- Le terrain doit avantager ou désavantager certains types (par exemple : l'Eau est avantagée sur un Océan, "
        "le Feu sur un Volcan, etc.).\n"
        "- Tu dois raconter le combat en 3 phases clairement identifiées : Début, Retournement, Fin.\n"
        "- Le ton doit être narratif, dynamique et logique, mais rester suffisamment concis.\n"
        "- Tu dois désigner un vainqueur cohérent avec ton analyse.\n"
        "- Termine OBLIGATOIREMENT par la phrase EXACTE : 'VAINQUEUR : [Nom du Pokémon]'.\n"
        "- Aucun texte après cette phrase. Pas d'explication supplémentaire."
    )

    user_prompt = (
        "Voici les données des combattants et le terrain de combat.\n\n"
        f"Terrain de combat : {terrain}\n\n"
        "Combattant 1 (Mon champion) - JSON :\n"
        "-----------------------------\n"
        f"{champion_1_json}\n"
        "-----------------------------\n\n"
        "Combattant 2 (L'adversaire) - JSON :\n"
        "-----------------------------\n"
        f"{champion_2_json}\n"
        "-----------------------------\n\n"
        "Consignes de sortie :\n"
        "1) Commence par une section 'Début du combat' et décris la mise en place et les premiers échanges.\n"
        "2) Continue avec une section 'Retournement de situation' où l'un des combattants prend l'avantage.\n"
        "3) Termine avec une section 'Fin du combat' où tu expliques comment le vainqueur s'impose.\n"
        "4) Termine par la ligne : VAINQUEUR : [Nom du Pokémon]\n"
        "Sans rien ajouter après cette ligne."
    )

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
    )

    story = completion.choices[0].message.content.strip()
    return story

# Titre principal
st.title("PokéArena - Le Duel de Données")
st.markdown(
    """
Bienvenue dans PokéArena.

Tu peux simuler un combat entre ton pokemon et celui d'un adversaire.

Pour ce faire : 

1. Colle le JSON de ton champion à gauche.
2. Colle le JSON de l'adversaire à droite.
3. Choisis un terrain de combat dans la barre latérale.
4. Nous ferons ensuite appel à un arbitre IA pour raconter l'affrontement.
"""
)

st.markdown("## Configuration des combattants")

# Deux colonnes : Mon Champion / L'Adversaire
col1, col2 = st.columns(2)

with col1:
    st.subheader("Mon Champion")
    champion_1_json_text = st.text_area(
        "JSON du champion 1",
        placeholder='Colle ici le JSON de ton champion, par exemple : {"Nom": "...", "Type": "...", ...}',
        height=250,
        key="champion_1_json",
    )

with col2:
    st.subheader("L'Adversaire")
    champion_2_json_text = st.text_area(
        "JSON du champion 2",
        placeholder='Colle ici le JSON de l\'adversaire',
        height=250,
        key="champion_2_json",
    )
    
champion_1_data = parse_champion_json(champion_1_json_text, "Mon Champion")
champion_2_data = parse_champion_json(champion_2_json_text, "L'Adversaire")

st.session_state.champion_1_data = champion_1_data
st.session_state.champion_2_data = champion_2_data

st.markdown("## Vérification des fiches combattants")

col_check_1, col_check_2 = st.columns(2)

with col_check_1:
    st.markdown("**Mon Champion**")
    if champion_1_data is not None:
        nom = champion_1_data.get("Nom", "")
        type_ = champion_1_data.get("Type", "")
        st.success(f"JSON valide. Nom : {nom} | Type : {type_}")
    else:
        st.info("En attente d'un JSON valide pour ton champion.")

with col_check_2:
    st.markdown("**L'Adversaire**")
    if champion_2_data is not None:
        nom = champion_2_data.get("Nom", "")
        type_ = champion_2_data.get("Type", "")
        st.success(f"JSON valide. Nom : {nom} | Type : {type_}")
    else:
        st.info("En attente d'un JSON valide pour l'adversaire.")


st.markdown("## Résumé avant combat")

st.write(f"Terrain sélectionné : **{terrain}**")

if champion_1_data is not None and champion_2_data is not None:
    st.success("Les deux fiches JSON sont valides. L'arbitre IA est prêt à juger le combat.")
else:
    st.info("Assure-toi que les deux JSON sont valides avant de lancer le duel.")

start_battle = st.button("Lancer le duel")

if start_battle:
    if champion_1_data is None or champion_2_data is None:
        st.error("Impossible de lancer le duel : un ou deux JSON sont invalides.")
    elif not groq_api_key:
        st.error("Merci de renseigner ta clé API Groq dans la barre latérale pour lancer le duel.")
    else:
        with st.spinner("L'arbitre IA analyse les fiches et le terrain..."):
            try:
                story = simuler_combat(
                    champion_1_data=champion_1_data,
                    champion_2_data=champion_2_data,
                    terrain=terrain,
                    api_key=groq_api_key,
                )

                st.markdown("## Récit du combat")
                st.write(story)

            except Exception as e:
                st.error(f"Erreur lors de la simulation du combat : {e}")
