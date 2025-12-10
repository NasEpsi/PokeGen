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

st.sidebar.markdown("---")
st.sidebar.info(
    "Colle les JSON de ton champion et de son adversaire dans la page principale, "
    "puis lance le combat."
)