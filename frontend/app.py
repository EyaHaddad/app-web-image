import os
import streamlit as st
import requests
from PIL import Image
import io

# Page d'accueil
#layout="centered"
st.set_page_config(page_title="Prétraitement d'images", page_icon="🖼️", layout="wide")

try:
    API_URL = st.secrets["api_url"]
except Exception:
    API_URL = os.environ.get("API_URL", "http://localhost:8000/api/preprocess")

st.title("Plateforme de prétraitement d'images")
st.write("Téléversez une image, appliquez des opérations de prétraitement puis visualisez/téléchargez le résultat.")

uploaded = st.file_uploader("Choisir une image", type=["png", "jpg", "jpeg", "bmp"])

col1, col2 = st.columns(2)

with col1:
    st.header("Image originale")
    if uploaded:
        image = Image.open(uploaded)
        st.image(image, use_column_width=True)
    else:
        st.info("Aucune image sélectionnée.")

with col2:
    st.header("Options de prétraitement")
    grayscale = st.checkbox("Convertir en niveaux de gris")
    equalize = st.checkbox("Égaliser l'histogramme")
    resize = st.checkbox("Redimensionner")
    rw = 0
    rh = 0
    if resize:
        rw = st.number_input("Largeur (px, 0 = automatique)", min_value=0, value=0)
        rh = st.number_input("Hauteur (px, 0 = automatique)", min_value=0, value=0)

    if st.button("Appliquer le prétraitement"):
        if not uploaded:
            st.error("Veuillez téléverser une image d'abord.")
        else:
            files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
            data = {
                "grayscale": str(grayscale).lower(),
                "equalize": str(equalize).lower(),
                "resize_width": str(int(rw) if rw else "0"),
                "resize_height": str(int(rh) if rh else "0"),
            }
            try:
                with st.spinner("Traitement en cours, veuillez patienter..."):
                    resp = requests.post(API_URL, files=files, data=data, timeout=30)
                if resp.status_code == 200:
                    result = Image.open(io.BytesIO(resp.content))
                    st.image(result, caption="Image prétraitée", use_column_width=True)
                    st.download_button("Télécharger (PNG)", data=resp.content, file_name="preprocessed.png", mime="image/png")
                else:
                    st.error(f"Erreur backend ({resp.status_code}): {resp.text}")
            except Exception as e:
                st.error(f"Échec de la requête: {e}")
