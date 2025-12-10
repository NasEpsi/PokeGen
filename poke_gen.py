import streamlit as st
import pandas as pd

# Config 
st.set_page_config(
    page_title="PokéGen - Le laboratoire de Création",
    page_icon="🧬",
    layout="wide",
)

if "pokemons_df" not in st.session_state:
    st.session_state.pokemons_df = None 

# Sidebar

st.sidebar.title("Laboratoire")

groq_api_key = st.sidebar.text_input(
    "Clé API Groq",
    type="password",
    help="Colle ici ta clé API depuis console.groq.com"
)

nb_pokemons = st.sidebar.slider(
    "Nombre de Pokémon à générer",
    min_value=3,
    max_value=10,
    value=5
)

type_dominant = st.sidebar.text_input(
    "Type dominant",
    placeholder="Feu, Eau, Cyberpunk, Antique..."
)

