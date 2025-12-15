import streamlit as st
from datetime import datetime
from utils.helpers import image_to_bytes

def render_gallery():
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
                        'timestamp': datetime.now(),
                        'preview': image_to_bytes(item['image'].resize((150, 150), 1))
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
