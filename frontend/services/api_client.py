import os
import streamlit as st
import requests
import io
from PIL import Image
from utils.helpers import image_to_bytes

# URL de l'API
try:
    API_URL = st.secrets["api_url"]
except Exception:
    API_URL = os.environ.get("API_URL", "http://localhost:8000/api")

API_ENDPOINTS = {
    "preprocess": "/preprocess",
    "histogram": "/histogram", 
    "segment": "/segment",
    "detect_faces": "/detect_faces",
    "crop": "/crop",
    "test": "/test"
}

def get_api_url(endpoint: str) -> str:
    """Retourne l'URL complète d'un endpoint API"""
    base_url = API_URL.rstrip('/')
    endpoint_path = API_ENDPOINTS.get(endpoint, endpoint)
    return f"{base_url}{endpoint_path}"

def apply_operation(current_image: Image.Image, endpoint: str, params: dict, on_success=None):
    """Applique une opération via l'API
    
    Args:
        current_image: L'image PIL actuelle
        endpoint: L'endpoint API (ex: "/preprocess", "/histogram")
        params: Les paramètres à passer
        on_success: Callback optionnel après succès
    
    Returns:
        Image.Image si c'est une image, bytes si c'est binaire (ex: PNG), ou None si erreur
    """
    try:
        if current_image:
            files = {
                'file': ('image.png', image_to_bytes(current_image), 'image/png')
            }
            
            # Déterminer l'URL endpoint
            if endpoint.startswith('/'):
                url = f"{API_URL.rstrip('/')}{endpoint}"
            else:
                url = get_api_url(endpoint)
            
            with st.spinner("⏳ Traitement..."):
                response = requests.post(
                    url,
                    files=files,
                    data=params,
                    timeout=30
                )
                
                content_type = response.headers.get('Content-Type', '')

                if response.status_code == 200:
                    # Gérer les réponses image
                    if content_type.startswith('image/'):
                        try:
                            # Vérifier si on demande un téléchargement (ex: histogram PNG)
                            if params.get('download') == 'true' or endpoint == '/histogram':
                                # Retourner les bytes bruts pour le download
                                return response.content
                            else:
                                # Retourner l'image PIL
                                result = Image.open(io.BytesIO(response.content))
                                st.toast(f"✅ Opération réussie!", icon="✅")
                                if on_success:
                                    on_success(result, endpoint, params)
                                return result
                        except Exception:
                            st.error("❌ La réponse du backend n'est pas une image valide.")
                            return None
                    else:
                        # 200 mais corps non-image (ex: JSON de debug)
                        try:
                            payload = response.json()
                            st.error(f"❌ Réponse inattendue (JSON): {payload}")
                        except Exception:
                            st.error(f"❌ Réponse inattendue du backend (type {content_type}).")
                        return None
                else:
                    # Statut non 200: essayer de montrer un message clair
                    try:
                        payload = response.json()
                        detail = payload.get('detail') if isinstance(payload, dict) else payload
                        st.error(f"❌ Erreur API ({response.status_code}): {detail}")
                    except Exception:
                        st.error(f"❌ Erreur API ({response.status_code}): {response.text}")
                    return None
    except requests.exceptions.ConnectionError:
        st.error("🔌 Impossible de se connecter au backend. Vérifiez qu'il est démarré.")
        return None
    except Exception as e:
        st.error(f"⚠️ Erreur: {str(e)}")
        return None
