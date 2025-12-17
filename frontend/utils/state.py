import streamlit as st
from datetime import datetime

def init_session_state():
    """Initialise l'état de la session"""
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
        #'batch_queue': []
    }
    
    for key, default_value in DEFAULT_STATES.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
