import os
import streamlit as st
import requests
from PIL import Image
import io
import base64
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Optional
import time
from datetime import datetime
# ==================== CONFIGURATION API CORRECTE ====================
API_ENDPOINTS = {
    "preprocess": "/preprocess",
    "histogram": "/histogram", 
    "segment": "/segment",  # Note: changé de segment_channels
    "detect_faces": "/detect_faces",
    "test": "/test"
}

def get_api_url(endpoint: str) -> str:
    """Retourne l'URL complète d'un endpoint API"""
    base_url = API_URL.rstrip('/')
    endpoint_path = API_ENDPOINTS.get(endpoint, endpoint)
    return f"{base_url}{endpoint_path}"
# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="ImageFlow Pro - Plateforme de Traitement d'Images",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded",
    #menu_items={
    #    'Get Help': 'https://github.com/your-repo',
    #    'Report a bug': "https://github.com/your-repo/issues",
    #    'About': "# ImageFlow Pro v1.0\nPlateforme avancée de traitement d'images"
    #}
)

# URL de l'API
try:
    API_URL = st.secrets["api_url"]
except Exception:
    API_URL = os.environ.get("API_URL", "http://localhost:8000/api")

# ==================== CSS PERSONNALISÉ AVANCÉ ====================
st.markdown("""
<style>
    /* Variables de couleurs */
    :root {
        --primary: #1e3a8a;       /* Dark blue */
        --secondary: #1e40af;     /* Medium blue */
        --accent: #3b82f6;        /* Bright blue */
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --light: #f8fafc;
        --dark: #0f172a;          /* Very dark blue */
        --gray: #64748b;
    }
    
    /* Application principale - Fond bleu foncé */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white !important;
    }
    
    /* Sidebar - Bleu foncé */
    .css-1d391kg, .css-1lcbmhc {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
        color: white !important;
    }
    
    /* Contenu de la sidebar */
    .css-1aumxhk {
        background: transparent !important;
        color: white !important;
    }
    
    /* Header - CORRIGÉ */
    .main-header {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        color: white;  
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #ffffff 0%, #93c5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    /* Cards */
    .feature-card {
        background: rgba(30, 41, 59, 0.8);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 5px solid var(--accent);
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
        background: rgba(30, 41, 59, 0.95);
    }
    
    /* Stats card */
    .stats-card {
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        color: white; 
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Boutons */
    .stButton > button {
        border-radius: 10px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        padding: 0.75rem 1.5rem;
        width: 100%;
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 14px rgba(0, 0, 0, 0.3);
        background: linear-gradient(90deg, var(--secondary) 0%, var(--accent) 100%) !important;
    }
    
    .primary-btn {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%) !important;
        color: white !important;
    }
    
    .secondary-btn {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 2px solid var(--accent) !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
        color: white !important;
    }
    
    /* Tous les éléments de la sidebar */
    section[data-testid="stSidebar"] div, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] h4, 
    section[data-testid="stSidebar"] h5, 
    section[data-testid="stSidebar"] h6 {
        color: white !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 0 2px;
        transition: all 0.3s ease;
        color: white !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%) !important;
        color: white !important; 
        border-color: var(--accent) !important;
        font-weight: bold;
    }
    
    /* Input fields */
    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        background: rgba(30, 41, 59, 0.8) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .stSelectbox div[data-baseweb="select"] {
        background: rgba(30, 41, 59, 0.8) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Sliders */
    .stSlider [data-baseweb="slider"] > div > div {
        background: var(--accent) !important;
    }
    
    .stSlider [data-baseweb="slider"] > div {
        background: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
    }
    
    /* Checkboxes et Radio */
    .stCheckbox label, .stRadio label {
        color: white !important;
    }
    
    /* Icons */
    .icon-large {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
        color: var(--accent);
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25em 0.6em;
        font-size: 75%;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 10px;
        background: var(--accent);
        color: white !important;
    }
    
    /* Tooltips */
    .tooltip-icon {
        cursor: help;
        color: var(--accent);
        margin-left: 5px;
    }
    
    /* Split view */
    .split-container {
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        margin: 2rem 0;
    }
    
    .split-line {
        position: absolute;
        width: 4px;
        height: 100%;
        background: var(--accent);
        left: 50%;
        transform: translateX(-50%);
        z-index: 10;
        cursor: col-resize;
        border-radius: 2px;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Texte général - TOUT EN BLANC */
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
    
    p, span, div {
        color: white !important;
    }
    
    /* Pour les métriques Streamlit */
    [data-testid="stMetric"] {
        color: white !important;
    }
    
    [data-testid="stMetricLabel"], 
    [data-testid="stMetricValue"], 
    [data-testid="stMetricDelta"] {
        color: white !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.8) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(15, 23, 42, 0.8) !important;
        color: white !important;
    }
    
    /* Tables */
    .stDataFrame, .stTable {
        background: rgba(30, 41, 59, 0.8) !important;
        color: white !important;
    }
    
    /* Séparateurs */
    hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Placeholder text */
    ::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.8);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--accent);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary);
    }
    
    /* Images avec bordure */
    .stImage {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Status messages */
    .stAlert {
        background: rgba(30, 41, 59, 0.9) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: var(--accent) !important;
    }
    
    /* Upload file */
    .stFileUploader {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 2px dashed var(--accent) !important;
        border-radius: 10px;
    }
    
    /* Code blocks */
    .stCodeBlock {
        background: rgba(15, 23, 42, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
</style>
""", unsafe_allow_html=True)

# ==================== INITIALISATION DU STATE ====================
DEFAULT_STATES = {
    'history': [],
    'history_index': -1,
    'current_image': None,
    'original_image': None,
    'gallery': [],
    'processed_image': None,
    'operations_count': 0,
    'session_start': datetime.now(),
    'favorites': [],
    'presets': {},
    'batch_queue': []
}

for key, default_value in DEFAULT_STATES.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

# ==================== FONCTIONS UTILITAIRES ====================

def image_to_bytes(image: Image.Image, format: str = 'PNG') -> bytes:
    """Convertit une image PIL en bytes avec format spécifique"""
    buf = io.BytesIO()
    image.save(buf, format=format, optimize=True)
    buf.seek(0)
    return buf.getvalue()

def add_to_history(image: Image.Image, operation: str, params: dict = None):
    """Ajoute une image à l'historique avec métadonnées"""
    timestamp = datetime.now()
    
    if st.session_state.history_index < len(st.session_state.history) - 1:
        st.session_state.history = st.session_state.history[:st.session_state.history_index + 1]
    
    history_entry = {
        'image': image.copy(),
        'operation': operation,
        'params': params or {},
        'timestamp': timestamp,
        'preview': image_to_bytes(image.resize((150, 150), Image.LANCZOS))
    }
    
    st.session_state.history.append(history_entry)
    st.session_state.history_index = len(st.session_state.history) - 1
    st.session_state.current_image = image.copy()
    st.session_state.operations_count += 1

def undo():
    """Annule la dernière opération"""
    if st.session_state.history_index > 0:
        st.session_state.history_index -= 1
        st.session_state.current_image = st.session_state.history[st.session_state.history_index]['image'].copy()
        return True
    return False

def redo():
    """Rétablit l'opération suivante"""
    if st.session_state.history_index < len(st.session_state.history) - 1:
        st.session_state.history_index += 1
        st.session_state.current_image = st.session_state.history[st.session_state.history_index]['image'].copy()
        return True
    return False

def reset_to_original():
    """Réinitialise à l'image originale"""
    if st.session_state.original_image:
        st.session_state.current_image = st.session_state.original_image.copy()
        st.session_state.history = [{
            'image': st.session_state.original_image.copy(),
            'operation': 'Original',
            'params': {},
            'timestamp': st.session_state.session_start,
            'preview': image_to_bytes(st.session_state.original_image.resize((150, 150), Image.LANCZOS))
        }]
        st.session_state.history_index = 0
        return True
    return False

def display_histogram(image: Image.Image, mode: str = "interactive"):
    """Affiche l'histogramme d'une image avec Plotly"""
    img_array = np.array(image)
    
    if mode == "simple":
        fig, ax = plt.subplots(figsize=(10, 4))
        if len(img_array.shape) == 2:
            ax.hist(img_array.ravel(), bins=256, color='gray', alpha=0.7)
            ax.set_title("Histogramme (Niveaux de gris)")
        else:
            colors = ['red', 'green', 'blue']
            for i, color in enumerate(colors):
                ax.hist(img_array[:,:,i].ravel(), bins=256, color=color, alpha=0.5, label=color)
            ax.set_title("Histogramme RGB")
            ax.legend()
        ax.set_xlabel("Valeur de pixel")
        ax.set_ylabel("Fréquence")
        st.pyplot(fig)
    else:
        # Mode interactif avec Plotly
        fig = go.Figure()
        
        if len(img_array.shape) == 2:
            hist, bins = np.histogram(img_array.flatten(), bins=256, range=[0, 256])
            fig.add_trace(go.Bar(
                x=list(range(256)),
                y=hist,
                name='Intensité',
                marker_color='gray',
                opacity=0.7
            ))
            title = "Histogramme (Niveaux de gris)"
        else:
            colors = ['red', 'green', 'blue']
            color_names = ['Rouge', 'Vert', 'Bleu']
            for i, (color, name) in enumerate(zip(colors, color_names)):
                hist, bins = np.histogram(img_array[:,:,i].flatten(), bins=256, range=[0, 256])
                fig.add_trace(go.Scatter(
                    x=list(range(256)),
                    y=hist,
                    mode='lines',
                    name=name,
                    line=dict(color=color, width=2),
                    fill='tozeroy',
                    fillcolor=f'rgba({int(color=="red")*255}, {int(color=="green")*255}, {int(color=="blue")*255}, 0.1)'
                ))
            title = "Histogramme RGB"
        
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=20, color='var(--dark)')
            ),
            xaxis_title="Valeur de pixel (0-255)",
            yaxis_title="Fréquence",
            height=350,
            showlegend=True,
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='var(--dark)'),
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig

def create_split_view(original_img, processed_img, show_labels=True):
    """Crée une vue divisée pour comparer avant/après"""
    from PIL import ImageDraw
    
    # Créer une image composite
    width1, height1 = original_img.size
    width2, height2 = processed_img.size
    
    # Redimensionner pour avoir la même hauteur
    max_height = max(height1, height2)
    scale1 = max_height / height1
    scale2 = max_height / height2
    
    new_width1 = int(width1 * scale1)
    new_width2 = int(width2 * scale2)
    
    original_resized = original_img.resize((new_width1, max_height), Image.LANCZOS)
    processed_resized = processed_img.resize((new_width2, max_height), Image.LANCZOS)
    
    # Créer l'image composite
    total_width = new_width1 + new_width2 + 10  # +10 pour l'espace
    composite = Image.new('RGB', (total_width, max_height), (240, 240, 240))
    
    composite.paste(original_resized, (0, 0))
    composite.paste(processed_resized, (new_width1 + 10, 0))
    
    # Ajouter des labels
    if show_labels:
        draw = ImageDraw.Draw(composite)
        from PIL import ImageFont
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        draw.text((10, 10), "AVANT", fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0), font=font)
        draw.text((new_width1 + 20, 10), "APRÈS", fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0), font=font)
    
    return composite

def apply_operation(operation_type: str, params: dict):
    """Applique une opération via l'API"""
    try:
        if st.session_state.current_image:
            files = {
                'file': ('image.png', image_to_bytes(st.session_state.current_image), 'image/png')
            }
            
            with st.spinner(f"⏳ Application de {operation_type}..."):
                # 
                response = requests.post(
                    f"{API_URL}/preprocess",  
                    files=files,
                    data=params,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = Image.open(io.BytesIO(response.content))
                    add_to_history(result, operation_type, params)
                    
                    # Notification de succès
                    st.toast(f"✅ {operation_type} appliqué avec succès!", icon="✅")
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
    
def save_preset(name: str, params: dict):
    """Sauvegarde un preset de paramètres"""
    st.session_state.presets[name] = {
        'params': params,
        'created_at': datetime.now(),
        'usage_count': 0
    }
    st.success(f"✅ Preset '{name}' sauvegardé!")

def load_preset(name: str):
    """Charge un preset de paramètres"""
    if name in st.session_state.presets:
        preset = st.session_state.presets[name]
        preset['usage_count'] += 1
        return preset['params']
    return None

# ==================== EN-TÊTE ====================
st.markdown("""
<div class="main-header fade-in">
    <h1 class="main-title"> ImageFlow Pro</h1>
    <p class="subtitle">Plateforme avancée de traitement et d'analyse d'images</p>
    <div style="text-align: center; margin-top: 1rem;">
        <span class="badge">⚡ Temps réel</span>
        <span class="badge">🎨 15+ filtres</span>
        <span class="badge">📊 Analyse avancée</span>
        <span class="badge">🔒 Sécurisé</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR AVANCÉE ====================
with st.sidebar:
    st.markdown("### 📊 Tableau de bord")
    
    # Statistiques
    col_stats1, col_stats2 = st.columns(2)
    with col_stats1:
        st.markdown(f"""
        <div class="stats-card">
            <div style="font-size: 2rem;">{st.session_state.operations_count}</div>
            <div>Opérations</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stats2:
        st.markdown(f"""
        <div class="stats-card">
            <div style="font-size: 2rem;">{len(st.session_state.gallery)}</div>
            <div>Images</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Upload avec drag & drop amélioré
    st.markdown("### 📤 Importer une image")
    
    uploaded_file = st.file_uploader(
        "Glissez-déposez ou cliquez pour parcourir",
        type=['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp'],
        help="Formats supportés: PNG, JPG, JPEG, BMP, TIFF, WEBP (max 20 MB)",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        try:
            # Vérification de la taille
            file_size = len(uploaded_file.getvalue())
            max_size = 20 * 1024 * 1024  # 20 MB
            
            if file_size > max_size:
                st.error("⚠️ Fichier trop grand (max 20 MB)")
            else:
                image = Image.open(uploaded_file)
                
                # Informations détaillées
                with st.expander("📋 Détails de l'image", expanded=True):
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.metric("Dimensions", f"{image.size[0]} × {image.size[1]}")
                        st.metric("Mode", image.mode)
                    with col_info2:
                        st.metric("Taille", f"{file_size / 1024:.1f} KB")
                        st.metric("Format", uploaded_file.type.split('/')[-1].upper())
                
                # Initialisation
                if st.button("🎯 Utiliser cette image", type="primary", use_container_width=True):
                    st.session_state.original_image = image.copy()
                    st.session_state.current_image = image.copy()
                    st.session_state.history = [{
                        'image': image.copy(),
                        'operation': 'Original',
                        'params': {},
                        'timestamp': datetime.now(),
                        'preview': image_to_bytes(image.resize((150, 150), Image.LANCZOS))
                    }]
                    st.session_state.history_index = 0
                    
                    # Ajouter à la galerie
                    if not any(item['name'] == uploaded_file.name for item in st.session_state.gallery):
                        if len(st.session_state.gallery) < 50:
                            st.session_state.gallery.append({
                                'name': uploaded_file.name,
                                'image': image.copy(),
                                'uploaded_at': datetime.now(),
                                'size': file_size
                            })
                    
                    st.rerun()
        
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")
    
    st.markdown("---")
    
    # Historique avancé
    if st.session_state.history:
        st.markdown("### 📜 Historique des opérations")
        
        # Timeline
        with st.expander("🕐 Timeline", expanded=False):
            for idx, item in enumerate(reversed(st.session_state.history[-10:])):
                actual_idx = len(st.session_state.history) - idx - 1
                icon = "⏺️" if actual_idx == st.session_state.history_index else "○"
                
                col_time1, col_time2 = st.columns([1, 4])
                with col_time1:
                    st.write(f"**{icon}**")
                with col_time2:
                    st.write(f"{item['operation']}")
                    st.caption(f"{item['timestamp'].strftime('%H:%M:%S')}")
        
        # Contrôles d'historique
        col_hist1, col_hist2, col_hist3 = st.columns(3)
        with col_hist1:
            if st.button("⏪", disabled=st.session_state.history_index <= 0, 
                        help="Annuler", use_container_width=True):
                if undo():
                    st.rerun()
        
        with col_hist2:
            if st.button("🔄", help="Réinitialiser", use_container_width=True):
                if reset_to_original():
                    st.rerun()
        
        with col_hist3:
            if st.button("⏩", disabled=st.session_state.history_index >= len(st.session_state.history) - 1,
                        help="Rétablir", use_container_width=True):
                if redo():
                    st.rerun()
    
    st.markdown("---")
    
    # Galerie améliorée
    if st.session_state.gallery:
        st.markdown("### 🖼️ Galerie")
        
        search_term = st.text_input("🔍 Rechercher", placeholder="Nom de l'image...")
        
        filtered_gallery = [img for img in st.session_state.gallery 
                          if search_term.lower() in img['name'].lower()] if search_term else st.session_state.gallery
        
        for idx, item in enumerate(filtered_gallery[:10]):  # Limite à 10 pour la performance
            col_gal1, col_gal2, col_gal3 = st.columns([3, 1, 1])
            
            with col_gal1:
                if st.button(f"📷 {item['name'][:25]}", 
                           key=f"gal_btn_{idx}",
                           use_container_width=True):
                    st.session_state.original_image = item['image'].copy()
                    st.session_state.current_image = item['image'].copy()
                    st.session_state.history = [{
                        'image': item['image'].copy(),
                        'operation': 'Original',
                        'params': {},
                        'timestamp': datetime.now()
                    }]
                    st.session_state.history_index = 0
                    st.rerun()
            
            with col_gal2:
                if st.button("⭐", key=f"fav_{idx}", 
                           help="Ajouter aux favoris",
                           use_container_width=True):
                    if item['name'] not in st.session_state.favorites:
                        st.session_state.favorites.append(item['name'])
                        st.success("✓ Ajouté aux favoris")
            
            with col_gal3:
                if st.button("🗑️", key=f"del_{idx}",
                           help="Supprimer",
                           use_container_width=True):
                    st.session_state.gallery.pop(idx)
                    st.rerun()

# ==================== CONTENU PRINCIPAL ====================
if st.session_state.current_image is not None:
    # Navigation par onglets
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏠 Vue d'ensemble",
        "🎨 Prétraitement",
        "🔧 Transformations", 
        "📊 Analyse",
        "⚡ Batch & Presets",
        "💾 Export"
    ])
    
    # ==================== TAB 1: VUE D'ENSEMBLE ====================
    with tab1:
        st.markdown("### 👁️ Aperçu de l'image")
        
        # Vue split avec curseur
        col_view1, col_view2 = st.columns(2)
        
        with col_view1:
            st.markdown("#### Image originale")
            st.image(st.session_state.original_image, 
                    use_container_width=True,
                    caption=f"Dimensions: {st.session_state.original_image.size[0]}×{st.session_state.original_image.size[1]}")
        
   
        # Bouton pour vue split
        if st.button("🔍 Vue comparée côte à côte", use_container_width=True):
            split_view = create_split_view(st.session_state.original_image, 
                                          st.session_state.current_image)
            st.image(split_view, use_container_width=True, 
                    caption="Comparaison avant/après")
        
        # Métriques rapides
        st.markdown("### 📈 Métriques")
        col_met1, col_met2, col_met3 = st.columns(3)
        
        with col_met1:
            original_pixels = st.session_state.original_image.size[0] * st.session_state.original_image.size[1]
            current_pixels = st.session_state.current_image.size[0] * st.session_state.current_image.size[1]
            st.metric("Pixels", f"{current_pixels:,}", 
                     delta=f"{(current_pixels - original_pixels):+,}")
        
        with col_met2:
            # Calcul de la différence moyenne
            original_arr = np.array(st.session_state.original_image.convert('RGB'))
            current_arr = np.array(st.session_state.current_image.convert('RGB'))
            if original_arr.shape == current_arr.shape:
                diff = np.abs(original_arr.astype(float) - current_arr.astype(float)).mean()
                st.metric("Différence moyenne", f"{diff:.1f}%")
        
        with col_met3:
            operations_applied = len([h for h in st.session_state.history 
                                    if h['operation'] != 'Original'])
            st.metric("Opérations appliquées", operations_applied)
    
    # ==================== TAB 2: PRÉTRAITEMENT ====================
    with tab2:
        st.markdown("### 🎨 Opérations de prétraitement")
        
        # Accordéon pour les différentes catégories
        with st.expander("🌓 Conversions de couleur", expanded=True):
            col_conv1, col_conv2 = st.columns(2)
            
            with col_conv1:
                grayscale = st.checkbox("Niveaux de gris", 
                                       help="Convertir l'image en niveaux de gris")
                equalize = st.checkbox("Égalisation d'histogramme",
                                      help="Améliore le contraste par égalisation")
                normalize = st.checkbox("Normalisation",
                                       help="Normalise les valeurs de pixels entre 0 et 255")
            
            with col_conv2:
                if st.button("Appliquer les conversions", 
                           type="primary",
                           use_container_width=True):
                    params = {
                        'grayscale': str(grayscale).lower(),
                        'equalize': str(equalize).lower(),
                        'normalize': str(normalize).lower()
                    }
                    apply_operation("Conversions couleur", params)
        
        with st.expander("🎯 Seuillage", expanded=True):
            col_thresh1, col_thresh2 = st.columns(2)
            
            with col_thresh1:
                apply_threshold = st.checkbox("Activer le seuillage")
                if apply_threshold:
                    threshold_value = st.slider("Seuil", 0, 255, 127, 
                                               help="Valeur de seuil (0-255)")
                    threshold_type = st.selectbox(
                        "Type de seuillage",
                        ["binary", "binary_inv", "adaptive_mean", "adaptive_gaussian", "otsu"],
                        format_func=lambda x: {
                            "binary": "Binaire standard",
                            "binary_inv": "Binaire inversé", 
                            "adaptive_mean": "Adaptatif (moyenne)",
                            "adaptive_gaussian": "Adaptatif (gaussien)",
                            "otsu": "Otsu (automatique)"
                        }[x]
                    )
            
            with col_thresh2:
                if apply_threshold and st.button("Appliquer seuillage",
                                               type="primary",
                                               use_container_width=True):
                    params = {
                        'threshold': str(threshold_value),
                        'threshold_type': threshold_type
                    }
                    apply_operation("Seuillage", params)
        
        with st.expander("🌫️ Filtres", expanded=True):
            col_filt1, col_filt2 = st.columns(2)
            
            with col_filt1:
                blur_type = st.selectbox(
                    "Type de filtre",
                    ["gaussian", "median", "bilateral", "none"],
                    format_func=lambda x: {
                        "gaussian": "Flou gaussien",
                        "median": "Flou médian",
                        "bilateral": "Flou bilatéral",
                        "none": "Aucun filtre"
                    }[x]
                )
                
                if blur_type != "none":
                    blur_kernel = st.slider("Intensité", 3, 31, 5, step=2,
                                           help="Taille du kernel (impair)")
                    sigma = st.slider("Sigma", 0.1, 5.0, 1.0) if blur_type == "gaussian" else None
            
            with col_filt2:
                if blur_type != "none" and st.button("Appliquer filtre",
                                                   type="primary",
                                                   use_container_width=True):
                    params = {
                        'blur_type': blur_type,
                        'blur_kernel': str(blur_kernel)
                    }
                    apply_operation(f"Filtre {blur_type}", params)
        
        with st.expander("📐 Redimensionnement", expanded=True):
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                resize_option = st.radio(
                    "Mode de redimensionnement",
                    ["Proportions", "Dimensions exactes", "Pourcentage"]
                )
                
                if resize_option == "Proportions":
                    maintain_ratio = st.checkbox("Maintenir le ratio", True)
                    new_width = st.number_input("Largeur (px)", 
                                              min_value=10, 
                                              max_value=5000,
                                              value=st.session_state.current_image.size[0])
                    if maintain_ratio:
                        ratio = st.session_state.current_image.size[1] / st.session_state.current_image.size[0]
                        new_height = int(new_width * ratio)
                        st.write(f"Hauteur: {new_height}px (auto)")
                    else:
                        new_height = st.number_input("Hauteur (px)",
                                                   min_value=10,
                                                   max_value=5000,
                                                   value=st.session_state.current_image.size[1])
                
                elif resize_option == "Dimensions exactes":
                    new_width = st.number_input("Largeur (px)", 
                                              min_value=10, 
                                              max_value=5000)
                    new_height = st.number_input("Hauteur (px)",
                                               min_value=10,
                                               max_value=5000)
                
                else:  # Pourcentage
                    percentage = st.slider("Pourcentage", 10, 500, 100)
                    new_width = int(st.session_state.current_image.size[0] * percentage / 100)
                    new_height = int(st.session_state.current_image.size[1] * percentage / 100)
                    st.write(f"Nouvelles dimensions: {new_width}×{new_height}px")
            
            with col_res2:
                if st.button("Redimensionner", type="primary", use_container_width=True):
                    params = {
                        'resize_width': str(new_width),
                        'resize_height': str(new_height)
                    }
                    apply_operation("Redimensionnement", params)
    
    # ==================== TAB 3: TRANSFORMATIONS ====================
    with tab3:
        st.markdown("###  Transformations géométriques et visuelles")
        
        col_trans1, col_trans2 = st.columns(2)
        
        with col_trans1:
            st.markdown("#### 🔄 Rotation et symétrie")
            
            rotate_angle = st.slider("Angle de rotation", -180, 180, 0,
                                    help="Rotation en degrés (-180 à 180)")
            
            flip_type = st.selectbox(
                "Retournement",
                ["none", "horizontal", "vertical", "both"],
                format_func=lambda x: {
                    "none": "Aucun",
                    "horizontal": "Horizontal",
                    "vertical": "Vertical",
                    "both": "Les deux"
                }[x]
            )
            
            if st.button("Appliquer transformations géométriques",
                        type="primary",
                        use_container_width=True):
                params = {}
                if rotate_angle != 0:
                    params['rotate_angle'] = str(rotate_angle)
                if flip_type != "none":
                    params['flip'] = flip_type
                
                if params:
                    apply_operation("Transformations géométriques", params)
        
        with col_trans2:
            st.markdown("#### ☀️ Ajustements visuels")
            
            brightness = st.slider("Luminosité", -100, 100, 0,
                                  help="Ajuste la luminosité globale")
            
            contrast = st.slider("Contraste", 0.1, 3.0, 1.0, 0.1,
                                help="Augmente ou diminue le contraste")
            
            saturation = st.slider("Saturation", 0.0, 3.0, 1.0, 0.1,
                                  help="Intensité des couleurs")
            
            if st.button("Appliquer ajustements visuels",
                        type="primary",
                        use_container_width=True):
                params = {}
                if brightness != 0:
                    params['brightness'] = str(brightness)
                if contrast != 1.0:
                    params['contrast'] = str(contrast)
                
                if params:
                    apply_operation("Ajustements visuels", params)
        
        # Détection de contours
        st.markdown("#### 🔍 Détection de contours")
        
        col_edge1, col_edge2 = st.columns(2)
        
        with col_edge1:
            edge_method = st.selectbox(
                "Méthode",
                ["canny", "sobel", "sobel_x", "sobel_y", "laplacian"],
                format_func=lambda x: {
                    "canny": "Canny (recommandé)",
                    "sobel": "Sobel (gradients)",
                    "sobel_x": "Sobel X (horizontal)",
                    "sobel_y": "Sobel Y (vertical)",
                    "laplacian": "Laplacian (2D)"
                }[x]
            )
            
            if edge_method == "canny":
                canny_low = st.slider("Seuil bas", 0, 255, 50)
                canny_high = st.slider("Seuil haut", 0, 255, 150)
        
        with col_edge2:
            if st.button("Détecter les contours",
                        type="primary",
                        use_container_width=True):
                params = {'edge_detection': edge_method}
                apply_operation(f"Détection {edge_method}", params)
    
    # ==================== TAB 4: ANALYSE ====================
    with tab4:
        st.markdown("### 📊 Analyse approfondie")
        
        col_anal1, col_anal2 = st.columns(2)
        
        with col_anal1:
            st.markdown("#### 📈 Histogramme interactif")
            
            hist_mode = st.radio(
                "Mode d'affichage",
                ["RGB complet", "Par canal"],
                horizontal=True
            )
            
            if hist_mode == "RGB complet":
                fig = display_histogram(st.session_state.current_image, "interactive")
                st.plotly_chart(fig, use_container_width=True)
            elif hist_mode == "Par canal":
                # Afficher les histogrammes par canal séparément
                tabs_r, g, b = st.tabs(["🔴 Rouge", "🟢 Vert", "🔵 Bleu"])
                
                img_array = np.array(st.session_state.current_image.convert('RGB'))
                
                with tabs_r:
                    fig_r = go.Figure()
                    hist_r = np.histogram(img_array[:,:,0].flatten(), bins=256, range=[0, 256])[0]
                    fig_r.add_trace(go.Bar(x=list(range(256)), y=hist_r, marker_color='red'))
                    fig_r.update_layout(title="Canal Rouge", height=300)
                    st.plotly_chart(fig_r, use_container_width=True)
                
                with g:
                    fig_g = go.Figure()
                    hist_g = np.histogram(img_array[:,:,1].flatten(), bins=256, range=[0, 256])[0]
                    fig_g.add_trace(go.Bar(x=list(range(256)), y=hist_g, marker_color='green'))
                    fig_g.update_layout(title="Canal Vert", height=300)
                    st.plotly_chart(fig_g, use_container_width=True)
                
                with b:
                    fig_b = go.Figure()
                    hist_b = np.histogram(img_array[:,:,2].flatten(), bins=256, range=[0, 256])[0]
                    fig_b.add_trace(go.Bar(x=list(range(256)), y=hist_b, marker_color='blue'))
                    fig_b.update_layout(title="Canal Bleu", height=300)
                    st.plotly_chart(fig_b, use_container_width=True)
        
       
            st.markdown("---")
            st.markdown("#### 📊 Statistiques")
            
            # Calculer les statistiques
            img_array = np.array(st.session_state.current_image.convert('RGB'))
            
            col_stats1, col_stats2 = st.columns(2)
            with col_stats1:
                st.metric("Moyenne", f"{img_array.mean():.1f}")
                st.metric("Écart-type", f"{img_array.std():.1f}")
            
            with col_stats2:
                st.metric("Minimum", f"{img_array.min()}")
                st.metric("Maximum", f"{img_array.max()}")
    
    # ==================== TAB 5: BATCH & PRESETS ====================
    with tab5:
        st.markdown("### ⚡ Traitement par lots et presets")
        
        col_batch1, col_batch2 = st.columns(2)
        
        with col_batch1:
            st.markdown("#### 📁 Traitement batch")
            
            batch_files = st.file_uploader(
                "Sélectionnez plusieurs images",
                type=['png', 'jpg', 'jpeg'],
                accept_multiple_files=True,
                help="Sélectionnez jusqu'à 10 images"
            )
            
            if batch_files and len(batch_files) > 0:
                st.info(f"{len(batch_files)} image(s) sélectionnée(s)")
                
                # Configuration du traitement batch
                batch_operation = st.selectbox(
                    "Opération à appliquer",
                    ["Conversion niveaux de gris", "Redimensionnement", "Seuillage", "Rotation"]
                )
                
                if st.button("🚀 Lancer le traitement batch", 
                           type="primary",
                           use_container_width=True):
                    progress_bar = st.progress(0)
                    results = []
                    
                    for idx, file in enumerate(batch_files):
                        try:
                            # Traiter chaque image
                            image = Image.open(file)
                            # Ici, vous ajouteriez l'appel API pour chaque image
                            results.append({
                                'name': file.name,
                                'status': 'success',
                                'message': 'Traitement réussi'
                            })
                            
                            progress_bar.progress((idx + 1) / len(batch_files))
                            
                        except Exception as e:
                            results.append({
                                'name': file.name,
                                'status': 'error',
                                'message': str(e)
                            })
                    
                    # Afficher les résultats
                    st.success(f"Traitement terminé : {len([r for r in results if r['status'] == 'success'])}/{len(results)} réussis")
                    
                    with st.expander("📋 Détails des résultats"):
                        for result in results:
                            emoji = "✅" if result['status'] == 'success' else "❌"
                            st.write(f"{emoji} {result['name']}: {result['message']}")
        
        with col_batch2:
            st.markdown("#### 💾 Presets sauvegardés")
            
            # Gestion des presets
            preset_name = st.text_input("Nom du preset", 
                                       placeholder="Ex: 'Contraste élevé'")
            
            col_preset1, col_preset2 = st.columns(2)
            with col_preset1:
                if st.button("💾 Sauvegarder preset", 
                           use_container_width=True,
                           disabled=not preset_name):
                    # Ici, vous sauvegarderiez les paramètres actuels
                    st.success(f"Preset '{preset_name}' sauvegardé!")
            
            with col_preset2:
                if st.session_state.presets:
                    selected_preset = st.selectbox(
                        "Charger un preset",
                        list(st.session_state.presets.keys())
                    )
                    
                    if st.button("📂 Charger preset",
                               use_container_width=True,
                               disabled=not selected_preset):
                        # Charger les paramètres du preset
                        st.info(f"Preset '{selected_preset}' chargé")
            
            # Liste des presets
            if st.session_state.presets:
                st.markdown("**Mes presets:**")
                for name, preset in st.session_state.presets.items():
                    col_p1, col_p2 = st.columns([3, 1])
                    with col_p1:
                        st.write(f"• {name}")
                        st.caption(f"Créé le {preset.get('created_at', 'N/A')}")
                    with col_p2:
                        if st.button("🗑️", key=f"del_preset_{name}"):
                            del st.session_state.presets[name]
                            st.rerun()
    
    # ==================== TAB 6: EXPORT ====================
    with tab6:
        st.markdown("### 💾 Exportation et téléchargement")
        
        col_exp1, col_exp2 = st.columns(2)
        
       
        
        with col_exp2:
            st.markdown("#### 📋 Rapport d'analyse")
            
            if st.button("📊 Générer un rapport", 
                        use_container_width=True,
                        type="primary"):
                # Créer un rapport détaillé
                report = f"""
                # Rapport d'analyse d'image
                ## ImageFlow Pro
                Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                
                ### Informations générales
                - Dimensions: {st.session_state.current_image.size[0]}×{st.session_state.current_image.size[1]} pixels
                - Mode: {st.session_state.current_image.mode}
                - Opérations appliquées: {len(st.session_state.history) - 1}
                - Taille estimée: {len(image_to_bytes(st.session_state.current_image)) / 1024:.1f} KB
                
                ### Historique des opérations
                """
                
                for idx, item in enumerate(st.session_state.history):
                    if item['operation'] != 'Original':
                        report += f"- {idx}. {item['operation']} ({item['timestamp'].strftime('%H:%M:%S')})\n"
                
                # Télécharger le rapport
                st.download_button(
                    label="📄 Télécharger le rapport",
                    data=report,
                    file_name="rapport_analyse.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            st.markdown("---")
            st.markdown("#### 🖼️ Galerie d'export")
            
            # Miniatures des images de l'historique
            if st.session_state.history:
                cols = st.columns(min(4, len(st.session_state.history)))
                for idx, item in enumerate(st.session_state.history[:4]):
                    with cols[idx % 4]:
                        # Créer une miniature
                        thumb = item['image'].resize((100, 100), Image.LANCZOS)
                        st.image(thumb, caption=f"Étape {idx}")
                        
                        # Bouton de téléchargement pour chaque étape
                        buf_step = io.BytesIO()
                        item['image'].save(buf_step, format="PNG")
                        buf_step.seek(0)
                        
                        st.download_button(
                            label=f"📥 Étape {idx}",
                            data=buf_step,
                            file_name=f"etape_{idx}.png",
                            mime="image/png",
                            key=f"dl_step_{idx}",
                            use_container_width=True
                        )

else:
    # ==================== PAGE D'ACCUEIL ====================
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem;">
        <h1 style="font-size: 4rem; margin-bottom: 1rem;"> Bienvenue sur ImageFlow Pro</h1>
        <p style="font-size: 1.5rem; color: var(--gray); margin-bottom: 3rem;">
            La plateforme ultime pour le traitement et l'analyse d'images
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features grid
    col_feat1, col_feat2, col_feat3 = st.columns(3)
    
    with col_feat1:
        st.markdown("""
        <div class="feature-card">
            <div class="icon-large">⚡</div>
            <h3>Traitement Rapide</h3>
            <p>Transformations en temps réel avec prévisualisation instantanée.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_feat2:
        st.markdown("""
        <div class="feature-card">
            <div class="icon-large">🎨</div>
            <h3>15+ Filtres</h3>
            <p>Une collection complète de filtres et transformations avancées.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_feat3:
        st.markdown("""
        <div class="feature-card">
            <div class="icon-large">📊</div>
            <h3>Analyse Avancée</h3>
            <p>Histogrammes interactifs, segmentation RGB et statistiques détaillées.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Deuxième ligne de features
    col_feat4, col_feat5, col_feat6 = st.columns(3)
    
    with col_feat4:
        st.markdown("""
        <div class="feature-card">
            <div class="icon-large">🔄</div>
            <h3>Historique Complet</h3>
            <p>Undo/redo illimité et gestion d'historique avancée.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_feat5:
        st.markdown("""
        <div class="feature-card">
            <div class="icon-large">⚡</div>
            <h3>Traitement Batch</h3>
            <p>Traitez plusieurs images simultanément avec les mêmes paramètres.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_feat6:
        st.markdown("""
        <div class="feature-card">
            <div class="icon-large">💾</div>
            <h3>Export Multi-format</h3>
            <p>Exportez en PNG, JPEG, WebP avec qualité ajustable.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Guide de démarrage
    st.markdown("---")
    st.markdown("### 🚀 Guide de démarrage rapide")
    
    guide_col1, guide_col2, guide_col3 = st.columns(3)
    
    with guide_col1:
        st.markdown("""
        #### 1. Importez
        Utilisez la barre latérale pour importer une image depuis votre ordinateur.
        
        **Formats supportés:**
        - PNG, JPG, JPEG
        - BMP, TIFF
        - WebP
        """)
    
    with guide_col2:
        st.markdown("""
        #### 2. Traitez
        Explorez les différents onglets pour appliquer des transformations:
        
        **Onglets disponibles:**
        -  Prétraitement
        -  Transformations
        -  Analyse
        -  Batch & Presets
        """)
    
    with guide_col3:
        st.markdown("""
        #### 3. Exportez
        Téléchargez vos images traitées dans différents formats:
        
        **Options d'export:**
        - PNG (qualité maximale)
        - JPEG (compressé)
        - WebP (moderne)
        - Rapport d'analyse
        """)
    
    # Dernière section avec CTA
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <h2>Prêt à commencer ?</h2>
        <p style="font-size: 1.2rem; margin-bottom: 2rem;">
            Importez votre première image dans la barre latérale pour découvrir toutes les fonctionnalités !
        </p>
        <div style="font-size: 3rem; margin: 2rem 0;">
            ↓
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("---")
col_foot1, col_foot2, col_foot3 = st.columns(3)

with col_foot1:
    st.markdown("**ImageFlow Pro v1.0**")
    st.caption("© 2024 - Plateforme de traitement d'images")

with col_foot2:
    st.markdown("**Performance**")
    st.caption(f"Temps de session: {(datetime.now() - st.session_state.session_start).seconds // 60} min")

with col_foot3:
    st.markdown("**Support**")
    st.caption("Reportez les bugs sur GitHub")

# ==================== JAVASCRIPT POUR AMÉLIORATIONS ====================
st.markdown("""
<script>
// Ajouter des animations smooth
document.addEventListener('DOMContentLoaded', function() {
    // Animation pour les cards
    const cards = document.querySelectorAll('.feature-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Tooltips personnalisés
    const tooltips = document.querySelectorAll('.tooltip-icon');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', function() {
            const title = this.getAttribute('title');
            if (title) {
                // Créer un tooltip personnalisé
                const tooltipEl = document.createElement('div');
                tooltipEl.className = 'custom-tooltip';
                tooltipEl.textContent = title;
                tooltipEl.style.cssText = `
                    position: absolute;
                    background: #333;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 4px;
                    font-size: 12px;
                    z-index: 1000;
                `;
                document.body.appendChild(tooltipEl);
                
                const rect = this.getBoundingClientRect();
                tooltipEl.style.top = (rect.top - tooltipEl.offsetHeight - 5) + 'px';
                tooltipEl.style.left = (rect.left + rect.width / 2 - tooltipEl.offsetWidth / 2) + 'px';
                
                this._tooltipEl = tooltipEl;
                this.removeAttribute('title');
            }
        });
        
        tooltip.addEventListener('mouseleave', function() {
            if (this._tooltipEl) {
                this._tooltipEl.remove();
                this._tooltipEl = null;
            }
        });
    });
});
</script>
""", unsafe_allow_html=True)