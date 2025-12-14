 # App Web de Traitement d'Image (prétraitement)

 Ce dépôt contient une petite plateforme web pour téléverser, prétraiter et visualiser des images.

 ## Structure
 - `backend/` : API FastAPI pour prétraitement d'images
 - `frontend/` : page Streamlit pour téléversement et visualisation

 ## Backend (FastAPI)
 - Endpoint: `POST /api/preprocess`
 - Paramètres: `grayscale` (bool), `equalize` (bool), `resize_width` (int), `resize_height` (int)
 - Renvoie l'image prétraitée au format PNG.

 ## Frontend (Streamlit)
 - Page `frontend/app.py` : interface pour téléverser l'image et appeler le backend.

 ## Commandes (PowerShell)

 # Créer des environnements virtuels et installer dépendances
 python -m venv .venv_backend; .\.venv_backend\Scripts\Activate.ps1; pip install -r backend\requirements.txt

 python -m venv .venv_frontend; .\.venv_frontend\Scripts\Activate.ps1; pip install -r frontend\requirements.txt

 # Lancer le backend
 .\.venv_backend\Scripts\Activate.ps1; uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

 # Lancer le frontend (nouveau terminal)
 .\.venv_frontend\Scripts\Activate.ps1; streamlit run frontend\app.py

 ## Notes
 - Par défaut, le frontend tente d'appeler `http://localhost:8000/api/preprocess`. Si votre backend tourne ailleurs, définissez `api_url` dans `streamlit secrets` ou modifiez `API_URL` dans `frontend/app.py`.
