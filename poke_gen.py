import streamlit as st
import pandas as pd
import json
from groq import Groq


# Config 
st.set_page_config(
    page_title="PokéGen - Le laboratoire de Création",
    page_icon="🧬",
    layout="wide",
)

if "pokemons_df" not in st.session_state:
    st.session_state.pokemons_df = None 
    
# Function to generate pokemons with the Groq API
def generate_pokemons_with_groq(api_key: str, nb_pokemons: int, type_dominant: str | None = None):
    client = Groq(api_key=api_key)
    type_hint = ""
    if type_dominant:
        type_hint = f" Ces Pokémon doivent partager un type dominant ou une esthétique '{type_dominant}'."

    system_prompt = (
        "Tu es une API de base de données Pokémon. "
        "Tu dois répondre UNIQUEMENT avec un objet JSON valide, sans texte autour, "
        "sans explication, sans commentaire.\n\n"
        "Le JSON doit avoir la structure suivante :\n"
        "{\n"
        '  "pokemons": [\n'
        "    {\n"
        '      "Nom": "Nom du Pokémon",\n'
        '      "Type": "Type principal ou mélange de types",\n'
        '      "Description": "Description courte du Pokémon",\n'
        '      "Personnalite": "Description de sa personnalité",\n'
        '      "Stats": "Résumé rapide de ses forces et faiblesses"\n'
        "    }\n"
        "  ]\n"
        "}\n\n"
        "Tous les champs doivent être des chaînes de caractères (string). "
        "La réponse DOIT être un JSON sérialisable, sans commentaires, sans trailing commas."
    )

    user_prompt = (
        f"Génère une liste de {nb_pokemons} Pokémon entièrement inédits.{type_hint}\n"
        "Chaque Pokémon doit avoir un style unique et une personnalité différentes."
    )

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.9,
        )

        raw_content = completion.choices[0].message.content
        data = json.loads(raw_content)
        pokemons_list = data.get("pokemons", [])

        if not isinstance(pokemons_list, list):
            raise ValueError("Le champ 'pokemons' n'est pas une liste.")

        return pokemons_list

    except json.JSONDecodeError as e:
        st.error(f"Erreur de parsing JSON : {e}")
        st.code(raw_content)
        return []
    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API Groq : {e}")
        return []


# Sidebar

st.sidebar.title("Laboratoire")

groq_api_key = st.sidebar.text_input(
    "Clé API Groq",
    type="password",
    placeholder="Colle ici ta clé API"
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

# Page principale
st.title("PokéGen - Le Laboratoire de Création")
st.markdown(
    """
    Bienvenue dans le laboratoire de PokéGen.

    Avec PokéGen, tu peux générer des Pokémon en utilisant l'IA Groq.
    
    Analyser leur personnalité et trouver leur compagnon idéale.
    
    Ensuite, tu peux exporter leur carte d'identité genétique en JSON pour les combats.

    Pour commencer : 
    - Renseigne ta clé API Groq dans la barre latérale.
    - Détermine le nombre de Pokémon à générer.
    - Optionnellement, renseigne le type dominant.
    - Génère tes Pokémons.
    - Exporte leurs cartes d'identité génétique en JSON.
    """
)

st.markdown("## Génération de Pokémon")

generate_button = st.button("Générer de nouveaux Pokémon")

if generate_button:
    if not groq_api_key:
        st.error("Merci de renseigner ta clé API Groq dans la barre latérale avant de générer des Pokémon.")
    else:
        with st.spinner("Génération de nouveaux Pokémon en cours..."):
            pokemons_list = generate_pokemons_with_groq(
                api_key=groq_api_key,
                nb_pokemons=nb_pokemons,
                type_dominant=type_dominant if type_dominant.strip() else None,
            )

            if pokemons_list:
                df = pd.DataFrame(pokemons_list)

                for col in ["Nom", "Type", "Description", "Personnalite", "Stats"]:
                    if col not in df.columns:
                        df[col] = ""

                st.session_state.pokemons_df = df

                st.success(f"{len(df)} Pokémon générés avec succès !")
            else:
                st.warning("Aucun Pokémon n'a pu être généré. Vérifie ton prompt ou réessaie.")


# Print the generated pokemons
if st.session_state.pokemons_df is not None:
    st.markdown("### Pokémon déjà générés")
    st.dataframe(st.session_state.pokemons_df)
else:
    st.info("Aucun Pokémon généré pour le moment.")


