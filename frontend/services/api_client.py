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
    "test": "/test"
}

def get_api_url(endpoint: str) -> str:
    """Retourne l'URL complète d'un endpoint API"""
    base_url = API_URL.rstrip('/')
    endpoint_path = API_ENDPOINTS.get(endpoint, endpoint)
    return f"{base_url}{endpoint_path}"

def apply_operation(operation_type: str, params: dict, current_image: Image.Image, on_success=None):
    """Applique une opération via l'API"""
    try:
        if current_image:
            files = {
                'file': ('image.png', image_to_bytes(current_image), 'image/png')
            }
            
            with st.spinner(f"⏳ Application de {operation_type}..."):
                response = requests.post(
                    get_api_url("preprocess"),  
                    files=files,
                    data=params,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = Image.open(io.BytesIO(response.content))
                    
                    # Notification de succès
                    st.toast(f"✅ {operation_type} appliqué avec succès!", icon="✅")
                    
                    if on_success:
                        on_success(result, operation_type, params)
                        
                    return result
                else:
                    st.error(f"❌ Erreur API: {response.text}")
                    return None
    except requests.exceptions.ConnectionError:
        st.error("🔌 Impossible de se connecter au backend. Vérifiez qu'il est démarré.")
        return None
    except Exception as e:
        st.error(f"⚠️ Erreur: {str(e)}")
        return None
