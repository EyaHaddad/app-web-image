import streamlit as st
import numpy as np
import plotly.graph_objects as go
from PIL import Image
from datetime import datetime
import io
from utils.helpers import create_split_view, image_to_bytes
from utils.visualization import display_histogram
from services.api_client import apply_operation
from components.history import add_to_history

def render_image_view():
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
                        apply_operation("Conversions couleur", params, st.session_state.current_image, on_success_callback)
            
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
                        apply_operation("Seuillage", params, st.session_state.current_image, on_success_callback)
            
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
                        apply_operation(f"Filtre {blur_type}", params, st.session_state.current_image, on_success_callback)
            
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
                        apply_operation("Redimensionnement", params, st.session_state.current_image, on_success_callback)
        
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
                        apply_operation("Transformations géométriques", params, st.session_state.current_image, on_success_callback)
            
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
                        apply_operation("Ajustements visuels", params, st.session_state.current_image, on_success_callback)
            
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
                    apply_operation(f"Détection {edge_method}", params, st.session_state.current_image, on_success_callback)
        
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

def on_success_callback(result_image, operation_type, params):
    """Callback called when an operation is successful"""
    add_to_history(result_image, operation_type, params)
