import streamlit as st
from datetime import datetime
from utils.helpers import image_to_bytes
from PIL import Image

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

def render_history():
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
