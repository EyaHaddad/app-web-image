import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("### 📊 Tableau de bord")   
        # Statistiques
        st.markdown(f"""
            <div class="stats-card">
                <div style="font-size: 2rem;">{st.session_state.operations_count}</div>
                <div>Opérations</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Aperçu de l'image en temps réel
        if st.session_state.current_image is not None:
            st.markdown("### 🖼️ Aperçu en temps réel")
            
            # Nom de l'opération actuelle
            if st.session_state.history and st.session_state.history_index < len(st.session_state.history):
                current_operation = st.session_state.history[st.session_state.history_index]['operation']
                st.markdown(f"**Opération:** `{current_operation}`")
            
            # Affichage de l'image
            st.image(
                st.session_state.current_image,
                use_container_width=True,
                caption="Image actuelle"
            )
            
            # Informations détaillées
            with st.expander("📋 Détails", expanded=False):
                img = st.session_state.current_image
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.metric("Largeur", f"{img.size[0]} px")
                    st.metric("Mode", img.mode)
                with col_info2:
                    st.metric("Hauteur", f"{img.size[1]} px")
                    st.metric("Pixels", f"{img.size[0] * img.size[1]:,}")

        st.markdown("---")
