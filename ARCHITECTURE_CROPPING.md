"""
ARCHITECTURE DE LA FONCTIONNALITÉ CROPPING
============================================

Diagramme du flux de données:

┌─────────────────────────────────────────────────────────────────┐
│                     FRONTEND (Streamlit)                        │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  app.py                                                   │  │
│  │  - Initialise l'app Streamlit                            │  │
│  └──────────────┬───────────────────────────────────────────┘  │
│                 │                                                │
│  ┌──────────────▼───────────────────────────────────────────┐  │
│  │  image_view.py                                            │  │
│  │  - Crée les onglets (Tab 1 à Tab 6)                      │  │
│  │  - Tab 2 = Cropping (appelle render_crop)               │  │
│  └──────────────┬───────────────────────────────────────────┘  │
│                 │                                                │
│  ┌──────────────▼───────────────────────────────────────────┐  │
│  │  crop.py (NOUVEAU)                                        │  │
│  │                                                            │  │
│  │  ┌─ render_crop()                                         │  │
│  │  │  - Interface principale                               │  │
│  │  │  - Sliders pour X, Y, Width, Height                  │  │
│  │  │  - Boutons présets                                    │  │
│  │  │  - Aperçu en temps réel                               │  │
│  │  │  - Boutons d'action (Appliquer, Réinitialiser)       │  │
│  │  └─ render_crop_preview()                                │  │
│  │     - Affiche l'image avec sélection                     │  │
│  │  └─ apply_crop()                                         │  │
│  │     - Fait appel à l'API                                 │  │
│  │     - Met à jour l'historique                            │  │
│  └──────────────┬───────────────────────────────────────────┘  │
│                 │                                                │
│  ┌──────────────▼───────────────────────────────────────────┐  │
│  │  api_client.py                                            │  │
│  │  - Centralise les appels API                             │  │
│  │  - API_ENDPOINTS = {..., "crop": "/crop"}               │  │
│  └──────────────┬───────────────────────────────────────────┘  │
└─────────────────┼───────────────────────────────────────────────┘
                  │
                  │ HTTP POST /api/crop
                  │ (multipart/form-data)
                  │ - file (image)
                  │ - x, y, width, height (params)
                  │
┌─────────────────▼───────────────────────────────────────────────┐
│                     BACKEND (FastAPI)                           │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  main.py                                                  │  │
│  │  - Configure l'app FastAPI                              │  │
│  │  - Enregistre les routers (preprocess, etc.)            │  │
│  └──────────────┬───────────────────────────────────────────┘  │
│                 │                                                │
│  ┌──────────────▼───────────────────────────────────────────┐  │
│  │  api/preprocess.py                                        │  │
│  │                                                            │  │
│  │  @router.post("/crop")  (NOUVEAU)                        │  │
│  │  async def crop_image_endpoint(...)                      │  │
│  │    ├─ Valide le fichier                                 │  │
│  │    ├─ Parse les paramètres (x, y, width, height)       │  │
│  │    ├─ Appelle processor.crop_image()                   │  │
│  │    └─ Retourne l'image PNG                              │  │
│  │                                                            │  │
│  └──────────────┬───────────────────────────────────────────┘  │
│                 │                                                │
│  ┌──────────────▼───────────────────────────────────────────┐  │
│  │  infrastructure/image_processor.py                        │  │
│  │                                                            │  │
│  │  class ImageProcessor(IImageProcessor):                  │  │
│  │    ...                                                    │  │
│  │    def crop_image(self, image_bytes, x, y, w, h):      │  │
│  │      ├─ Ouvre l'image avec PIL                         │  │
│  │      ├─ Valide les coordonnées                         │  │
│  │      ├─ Appelle img.crop((x, y, x+w, y+h))           │  │
│  │      ├─ Sauvegarde en PNG                              │  │
│  │      └─ Retourne les bytes                              │  │
│  │                                                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘


FLUX D'EXÉCUTION DÉTAILLÉ:
===========================

1. Utilisateur arrive sur le tab Cropping
   └─ render_crop() s'exécute

2. Utilisateur ajuste les sliders ou clique sur un preset
   └─ Streamlit re-run
   └─ L'aperçu s'met à jour (render_crop_preview)

3. Utilisateur clique "Appliquer le Crop"
   └─ apply_crop(x, y, width, height) s'exécute
   └─ image_to_bytes() convertit l'image courante
   └─ requests.post() envoie à /api/crop
   
4. Backend reçoit la requête
   └─ crop_image_endpoint() valide
   └─ processor.crop_image() effectue le crop
   └─ Retourne l'image croppée en PNG
   
5. Frontend reçoit la réponse
   └─ PIL.Image.open() charge l'image
   └─ add_to_history() enregistre dans l'historique
   └─ st.session_state.current_image = cropped_image
   └─ st.rerun() rafraîchit l'interface
   
6. L'utilisateur voit l'image croppée
   └─ Peut appliquer d'autres transformations
   └─ Peut exporter l'image


STRUCTURE DES DONNÉES:
======================

Request (Frontend → Backend):
{
  "files": {
    "file": (image_bytes, "image/png")
  },
  "data": {
    "x": "100",        # Position gauche
    "y": "50",         # Position haut
    "width": "400",    # Largeur de la région
    "height": "300"    # Hauteur de la région
  }
}

Response (Backend → Frontend):
- Status: 200 OK
- Content-Type: image/png
- Body: PNG image bytes


Session State (Frontend):
{
  "current_image": PIL.Image,
  "original_image": PIL.Image,
  "history": [
    {
      "image": PIL.Image,
      "operation": "Crop",
      "params": {"x": 100, "y": 50, "width": 400, "height": 300},
      "timestamp": datetime
    },
    ...
  ],
  "history_index": 0,
  "operations_count": 1
}


DÉPENDANCES:
=============

Backend:
- FastAPI (server)
- PIL/Pillow (image processing)
- cv2 (optional, pour les transformations avancées)

Frontend:
- Streamlit (UI)
- PIL/Pillow (image display)
- requests (HTTP calls)
- numpy (optional, pour les calculs)


POINTS D'EXTENSION:
====================

1. Support du cropping libre (drawable area)
   └─ Utiliser streamlit-drawable-canvas

2. Aspect ratio locking
   └─ Ajouter checkbox "Lock ratio"

3. Présets personnalisés
   └─ Sauvegarder des présets utilisateur

4. Cropping en temps réel
   └─ WebSocket au lieu de HTTP POST

5. Cropping intelligent (détection de contenu)
   └─ Utiliser des modèles ML pour déterminer le meilleur crop

6. Multi-crop
   └─ Cropper plusieurs régions en une seule opération
"""
