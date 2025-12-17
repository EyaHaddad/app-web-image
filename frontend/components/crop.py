import streamlit as st
from PIL import Image
import io
import requests
from streamlit_cropper import st_cropper

def render_crop_preview(image: Image.Image, x: int, y: int, width: int, height: int):
    """Affiche un aperçu du cropping avec rectangle de sélection"""
    # Créer une copie de l'image pour afficher le rectangle
    preview_img = image.copy()
    
    # Ajouter un rectangle autour de la région de crop
    from PIL import ImageDraw
    draw = ImageDraw.Draw(preview_img)
    
    # Calcul des coordonnées réelles
    x2 = min(x + width, image.size[0])
    y2 = min(y + height, image.size[1])
    
    # Assombrir la zone en dehors du crop
    overlay = Image.new('RGBA', preview_img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # Zone en haut
    overlay_draw.rectangle([(0, 0), (preview_img.size[0], y)], fill=(0, 0, 0, 150))
    # Zone en bas
    overlay_draw.rectangle([(0, y2), (preview_img.size[0], preview_img.size[1])], fill=(0, 0, 0, 150))
    # Zone à gauche
    overlay_draw.rectangle([(0, y), (x, y2)], fill=(0, 0, 0, 150))
    # Zone à droite
    overlay_draw.rectangle([(x2, y), (preview_img.size[0], y2)], fill=(0, 0, 0, 150))
    
    # Convertir l'image en RGB si nécessaire pour la fusion
    if preview_img.mode != 'RGBA':
        preview_img = preview_img.convert('RGBA')
    
    # Fusionner l'overlay
    preview_img = Image.alpha_composite(preview_img, overlay)
    
    # Dessiner le rectangle de sélection
    draw = ImageDraw.Draw(preview_img)
    draw.rectangle([(x, y), (x2, y2)], outline=(0, 255, 0), width=3)
    
    return preview_img


def render_crop():
    """Composant principal pour le cropping d'images"""
    
    if st.session_state.current_image is None:
        st.warning("⚠️ Veuillez charger une image d'abord.")
        return
    
    st.markdown("### ✂️ Outil de Cropping")
    
    # Mode de sélection
    st.markdown("#### 🎮 Mode de sélection")
    selection_mode = st.radio(
        "Choisissez votre mode de sélection",
        ["🖱️ Sélection interactive", "🎚️ Sélection par sliders"],
        horizontal=True,
        help="Sélection interactive : déplacez et redimensionnez avec la souris\nSliders : utilisez les curseurs pour définir précisément la zone"
    )
    
    img_width, img_height = st.session_state.current_image.size
    
    # Mode interactif avec la souris
    if selection_mode == "🖱️ Sélection interactive":
        st.markdown("---")
        
        col_main, col_side = st.columns([2, 1])
        
        with col_side:
            st.markdown("#### 🎯 Présets")
            
            # Initialiser le ratio d'aspect
            if 'aspect_ratio' not in st.session_state:
                st.session_state.aspect_ratio = None
            
            # Présets de ratio
            if st.button("🆓 Libre", use_container_width=True, help="Sélection libre sans contrainte de ratio"):
                st.session_state.aspect_ratio = None
                st.rerun()
            
            if st.button("🟩 Carré (1:1)", use_container_width=True):
                st.session_state.aspect_ratio = (1, 1)
                st.rerun()
            
            if st.button("🎬 16:9", use_container_width=True):
                st.session_state.aspect_ratio = (16, 9)
                st.rerun()
            
            if st.button("📱 9:16", use_container_width=True):
                st.session_state.aspect_ratio = (9, 16)
                st.rerun()
            
            if st.button("🖼️ 4:3", use_container_width=True):
                st.session_state.aspect_ratio = (4, 3)
                st.rerun()
            
            if st.button("📸 3:2", use_container_width=True):
                st.session_state.aspect_ratio = (3, 2)
                st.rerun()
            
            st.markdown("---")
            st.markdown("#### ℹ️ Instructions")
            st.info(
                "🖱️ **Déplacez** le rectangle\n\n"
                "↔️ **Redimensionnez** depuis les coins\n\n"
                "🎯 Cliquez sur un **preset** pour fixer le ratio"
            )
        
        with col_main:
            st.markdown("#### 🖼️ Sélectionnez la zone à cropper")
            
            # Utiliser st_cropper pour la sélection interactive
            cropped_img = st_cropper(
                st.session_state.current_image,
                realtime_update=True,
                box_color='#00FF00',
                aspect_ratio=st.session_state.aspect_ratio
            )
            
            # Récupérer les dimensions de l'image croppée
            if cropped_img is not None:
                crop_width, crop_height = cropped_img.size
                # Stocker l'image croppée temporairement
                st.session_state.temp_cropped = cropped_img
                # Les coordonnées exactes ne sont pas disponibles avec st_cropper
                # On utilisera directement l'image retournée
                crop_x, crop_y = 0, 0
            else:
                crop_x, crop_y = 0, 0
                crop_width, crop_height = img_width, img_height
            
            # Affichage des informations
            st.markdown("#### 📊 Informations de sélection")
            info_col1, info_col2, info_col3, info_col4 = st.columns(4)
            
            with info_col1:
                st.metric("Image originale", f"{img_width}×{img_height} px")
            
            with info_col2:
                st.metric("Région sélectionnée", f"{crop_width}×{crop_height} px")
            
            with info_col3:
                crop_area = crop_width * crop_height
                original_area = img_width * img_height
                percentage = (crop_area / original_area * 100) if original_area > 0 else 0
                st.metric("% conservé", f"{percentage:.1f}%")
            
            with info_col4:
                ratio = crop_width / crop_height if crop_height > 0 else 0
                st.metric("Rapport", f"{ratio:.2f}")
    
    # Mode sliders (ancien mode)
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("---")
            st.markdown("#### 📐 Paramètres de cropping")
            
            # Initialiser les valeurs par défaut
            default_width = min(400, img_width // 2)
            default_height = min(400, img_height // 2)
            
            # Récupérer les valeurs du preset s'il existe
            if 'crop_preset' in st.session_state and st.session_state.crop_preset is not None:
                default_x = st.session_state.crop_preset.get('x', 0)
                default_y = st.session_state.crop_preset.get('y', 0)
                default_width = st.session_state.crop_preset.get('width', default_width)
                default_height = st.session_state.crop_preset.get('height', default_height)
                # Nettoyer le preset après utilisation
                st.session_state.crop_preset = None
            else:
                default_x = 0
                default_y = 0
            
            col_x, col_y = st.columns(2)
            
            with col_x:
                crop_x = st.slider(
                    "Position X (gauche)",
                    min_value=0,
                    max_value=max(0, img_width - 1),
                    value=default_x,
                    help="Coordonnée horizontale du coin supérieur gauche"
                )
            
            with col_y:
                crop_y = st.slider(
                    "Position Y (haut)",
                    min_value=0,
                    max_value=max(0, img_height - 1),
                    value=default_y,
                    help="Coordonnée verticale du coin supérieur gauche"
                )
            
            col_w, col_h = st.columns(2)
            
            with col_w:
                crop_width = st.slider(
                    "Largeur",
                    min_value=1,
                    max_value=img_width - crop_x,
                    value=default_width,
                    help="Largeur de la région à cropper"
                )
            
            with col_h:
                crop_height = st.slider(
                    "Hauteur",
                    min_value=1,
                    max_value=img_height - crop_y,
                    value=default_height,
                    help="Hauteur de la région à cropper"
                )
            
            # Affichage des informations
            st.markdown("#### 📊 Informations")
            info_col1, info_col2, info_col3, info_col4 = st.columns(4)
            
            with info_col1:
                st.metric("Image originale", f"{img_width}×{img_height} px")
            
            with info_col2:
                st.metric("Région crop", f"{crop_width}×{crop_height} px")
            
            with info_col3:
                crop_area = crop_width * crop_height
                original_area = img_width * img_height
                percentage = (crop_area / original_area * 100) if original_area > 0 else 0
                st.metric("% conservé", f"{percentage:.1f}%")
            
            with info_col4:
                st.metric("Rapport", f"{crop_width/crop_height:.2f}")
            
        with col2:
            st.markdown("---")
            st.markdown("#### 🎯 Présets")
            
            # Présets courants
            if st.button("🟩 Carré (1:1)", use_container_width=True):
                size = min(crop_width, crop_height)
                st.session_state.crop_preset = {
                    'x': crop_x,
                    'y': crop_y,
                    'width': size,
                    'height': size
                }
                st.rerun()
            
            if st.button("🎬 16:9", use_container_width=True):
                if crop_width / crop_height != 16 / 9:
                    new_height = int(crop_width * 9 / 16)
                    if new_height <= img_height - crop_y:
                        st.session_state.crop_preset = {
                            'x': crop_x,
                            'y': crop_y,
                            'width': crop_width,
                            'height': new_height
                        }
                        st.rerun()
            
            if st.button("📱 9:16 (Portrait)", use_container_width=True):
                if crop_height / crop_width != 16 / 9:
                    new_width = int(crop_height * 9 / 16)
                    if new_width <= img_width - crop_x:
                        st.session_state.crop_preset = {
                            'x': crop_x,
                            'y': crop_y,
                            'width': new_width,
                            'height': crop_height
                        }
                        st.rerun()
            
            if st.button("🖼️ 4:3", use_container_width=True):
                new_height = int(crop_width * 3 / 4)
                if new_height <= img_height - crop_y:
                    st.session_state.crop_preset = {
                        'x': crop_x,
                        'y': crop_y,
                        'width': crop_width,
                        'height': new_height
                    }
                    st.rerun()
        
        # Aperçu du cropping pour le mode sliders
        st.markdown("---")
        st.markdown("#### 👁️ Aperçu")
        
        preview_cols = st.columns(2)
        
        with preview_cols[0]:
            st.markdown("**Image originale**")
            preview_img = render_crop_preview(
                st.session_state.current_image,
                crop_x, crop_y, crop_width, crop_height
            )
            st.image(preview_img, use_container_width=True)
        
        with preview_cols[1]:
            st.markdown("**Aperçu du résultat**")
            # Créer un aperçu du résultat final
            x2 = min(crop_x + crop_width, img_width)
            y2 = min(crop_y + crop_height, img_height)
            cropped_preview = st.session_state.current_image.crop((crop_x, crop_y, x2, y2))
            st.image(cropped_preview, use_container_width=True)
    
    # Boutons d'action
    st.markdown("#### ⚙️ Actions")
    
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        if st.button("✂️ Appliquer le Crop", 
                    type="primary",
                    use_container_width=True,
                    help="Cropper l'image avec les paramètres définis"):
            # Si on est en mode interactif et qu'on a une image croppée temporaire
            if selection_mode == "🖱️ Sélection interactive (souris)" and 'temp_cropped' in st.session_state and st.session_state.temp_cropped is not None:
                apply_crop_direct(st.session_state.temp_cropped)
            else:
                apply_crop(crop_x, crop_y, crop_width, crop_height)
    
    with action_col2:
        if st.button("🔄 Réinitialiser", 
                    use_container_width=True,
                    help="Rétablir l'image originale"):
            st.session_state.current_image = st.session_state.original_image.copy()
            st.session_state.history = []
            st.session_state.history_index = 0
            st.rerun()


def apply_crop_direct(cropped_image: Image.Image):
    """Applique directement l'image croppée (mode interactif)"""
    try:
        from components.history import add_to_history
        
        # Mettre à jour l'état et l'historique
        st.session_state.current_image = cropped_image
        add_to_history(
            cropped_image,
            "Crop interactif",
            {
                'width': cropped_image.size[0],
                'height': cropped_image.size[1]
            }
        )
        st.session_state.operations_count += 1
        
        # Nettoyer l'image temporaire
        if 'temp_cropped' in st.session_state:
            del st.session_state.temp_cropped
        
        st.toast("✅ Crop appliqué avec succès!", icon="✅")
        st.rerun()
    
    except Exception as e:
        st.error(f"⚠️ Erreur: {str(e)}")


def apply_crop(x: int, y: int, width: int, height: int):
    """Applique le cropping via l'API"""
    try:
        from utils.helpers import image_to_bytes
        from components.history import add_to_history
        
        # Récupérer l'URL de l'API
        try:
            api_url = st.secrets["api_url"]
        except Exception:
            import os
            api_url = os.environ.get("API_URL", "http://localhost:8000/api")
        
        # Préparer les données
        files = {
            'file': ('image.png', image_to_bytes(st.session_state.current_image), 'image/png')
        }
        
        params = {
            'x': str(x),
            'y': str(y),
            'width': str(width),
            'height': str(height)
        }
        
        with st.spinner("✂️ Application du crop..."):
            response = requests.post(
                f"{api_url}/crop",
                files=files,
                data=params,
                timeout=30
            )
            
            if response.status_code == 200:
                # Charger l'image cropée
                cropped_image = Image.open(io.BytesIO(response.content))
                
                # Mettre à jour l'état et l'historique
                st.session_state.current_image = cropped_image
                add_to_history(
                    cropped_image,
                    "Crop",
                    {
                        'x': x,
                        'y': y,
                        'width': width,
                        'height': height
                    }
                )
                st.session_state.operations_count += 1
                
                st.toast("✅ Crop appliqué avec succès!", icon="✅")
                st.rerun()
            else:
                try:
                    error_detail = response.json().get('detail', response.text)
                except Exception:
                    error_detail = response.text
                st.error(f"❌ Erreur lors du crop: {error_detail}")
    
    except requests.exceptions.ConnectionError:
        st.error("🔌 Impossible de se connecter au backend. Vérifiez qu'il est démarré.")
    except Exception as e:
        st.error(f"⚠️ Erreur: {str(e)}")
