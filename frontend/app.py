import streamlit as st
from styles.styles import apply_custom_css
from utils.state import init_session_state
from components.sidebar import render_sidebar
from components.history import render_history
from components.gallery import render_gallery
from components.image_view import render_image_view
from components.upload_image import upload_image
from datetime import datetime
from streamlit_scroll_to_top import scroll_to_here


# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="ImageFlow Pro - Plateforme de Traitement d'Images",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== INITIALISATION ====================
init_session_state()
apply_custom_css()

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

# ==================== CONTENU PRINCIPAL ====================
if st.session_state.current_image is not None:
    # ==================== SIDEBAR ====================
    render_sidebar()
    
    # Historique
    render_history()
    
    # Galerie
    render_gallery()
    
    # Vue principale
    render_image_view()

    st.markdown("---")
    
    # Bouton pour revenir à l'accueil - Design amélioré
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📤 Charger une nouvelle image", 
                     type="primary",
                     help="Retour à l'accueil pour uploader une nouvelle image", 
                     use_container_width=True):
            # Réinitialiser l'état pour revenir à l'accueil
            st.session_state.current_image = None
            st.session_state.original_image = None
            st.session_state.history = []
            st.session_state.history_index = 0
            st.session_state.operations_count = 0
            st.session_state.gallery = []
            #scroll to the header
            st.session_state.scroll_to_header = True 
            scroll_to_here(0, key='header')  # Scroll to the header of the page
            st.rerun()

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
    col_feat4, col_feat6 = st.columns(2)
    
    with col_feat4:
        st.markdown("""
        <div class="feature-card">
            <div class="icon-large">🔄</div>
            <h3>Historique Complet</h3>
            <p>Undo/redo illimité et gestion d'historique avancée.</p>
        </div>
        """, unsafe_allow_html=True)
    
    #with col_feat5:
    #    st.markdown(
    #    <div class="feature-card">
    #        <div class="icon-large">⚡</div>
    #        <h3>Traitement Batch</h3>
    #        <p>Traitez plusieurs images simultanément avec les mêmes paramètres.</p>
    #    </div>
    #    , unsafe_allow_html=True)
    
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
    <div style="text-align: center; padding: 2rem;">
        <h2>Prêt à commencer ?</h2>
        <p style="font-size: 1.2rem; margin-bottom: 2rem;">
            Importez votre première image ici pour découvrir toutes les fonctionnalités !
        </p>
        <div style="font-size: 3rem;">
            ↓
        </div>
    </div>
    """, unsafe_allow_html=True)

    upload_image()
# ==================== FOOTER ====================
#st.markdown("---")
col_foot1, col_foot2, col_foot3 = st.columns(3)

with col_foot1:
    st.markdown("**ImageFlow Pro v1.0**")
    st.caption("© 2025 - Plateforme de traitement d'images")

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