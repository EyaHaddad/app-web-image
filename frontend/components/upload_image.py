import streamlit as st
from PIL import Image
from datetime import datetime
from utils.helpers import image_to_bytes
from streamlit_scroll_to_top import scroll_to_here

def upload_image():    
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
                    
                    scroll_to_here(0, key='header')  # Scroll to the header of the page
                    st.rerun()
        
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")
    
    st.markdown("---")