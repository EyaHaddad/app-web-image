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

### Environnements virtuels (avec `uv`)

Ce projet utilise le gestionnaire `uv` pour créer et gérer des environnements virtuels et les dépendances. Voici les commandes courantes et leur rôle :

- `uv init` — initialise l'environnement / la configuration du projet.
- `uv add <package>` — ajoute une dépendance au projet.
- `uv sync` — installe / synchronise les dépendances déclarées.
- `uv run <command>` — exécute une commande à l'intérieur de l'environnement créé.

Pour l'exécution des parties :
# Backend
cd backend
uv sync
uv run uvicorn backend.app.main:app --reload

# Frontend (nouveau terminal)
cd frontend
uv sync
uv run streamlit run app.py

Remarques :
- `uv run` est la façon recommandée d'exécuter les serveurs (remplace l'appel direct à `uvicorn` / `streamlit` si vous souhaitez l'isoler dans l'environnement géré par `uv`).

### Commandes alternatives (sans `uv`)

 # Lancer le backend
    uvicorn backend.app.main:app --reload

 # Lancer le frontend (nouveau terminal)
    streamlit run frontend\app.py

 ## Notes
 - Par défaut, le frontend tente d'appeler `http://localhost:8000/api/preprocess`. Si votre backend tourne ailleurs, définissez `api_url` dans `streamlit secrets` ou modifiez `API_URL` dans `frontend/app.py`.
