# 📋 Documentation - Nouvelle Fonctionnalité: Cropping d'Images

## 📌 Résumé

Une nouvelle fonctionnalité de **cropping d'images** a été ajoutée à l'application ImageFlow Pro. Cette fonctionnalité permet aux utilisateurs de cropper/découper des régions spécifiques d'une image via une interface interactive.

---

## 🔧 Architecture

### Backend (FastAPI)

#### 1. **Nouvelle méthode dans `ImageProcessor`** 
   - **Fichier**: `backend/app/infrastructure/image_processor.py`
   - **Méthode**: `crop_image(image_bytes, x, y, width, height)`
   - **Fonctionnalité**: 
     - Accepte les coordonnées (x, y) et les dimensions (width, height)
     - Valide que la région de crop reste dans les limites de l'image
     - Retourne l'image croppée en format PNG
     - Gère les erreurs de dépassement de limites

#### 2. **Nouvel endpoint API**
   - **Fichier**: `backend/app/api/preprocess.py`
   - **Endpoint**: `POST /api/crop`
   - **Paramètres**:
     ```
     - file: Image (multipart/form-data)
     - x: int (position gauche en pixels)
     - y: int (position haut en pixels)
     - width: int (largeur de la région)
     - height: int (hauteur de la région)
     ```
   - **Réponse**: Image PNG croppée

### Frontend (Streamlit)

#### 1. **Nouveau composant: `crop.py`**
   - **Fichier**: `frontend/components/crop.py`
   - **Fonctions principales**:
     - `render_crop_preview()`: Affiche un aperçu avec rectangle de sélection
     - `render_crop()`: Interface principale du cropping
     - `apply_crop()`: Appelle l'API et met à jour l'image

#### 2. **Fonctionnalités de l'interface**:
   - ✂️ **Sliders interactifs** pour:
     - Position X (gauche)
     - Position Y (haut)
     - Largeur de crop
     - Hauteur de crop
   
   - 📊 **Informations en temps réel**:
     - Dimensions de l'image originale
     - Taille de la région de crop
     - Pourcentage conservé
     - Ratio de la région
   
   - 🎯 **Présets rapides**:
     - Carré (1:1)
     - 16:9
     - 9:16 (Portrait)
     - 4:3
   
   - 👁️ **Aperçu en temps réel**:
     - Image originale avec sélection
     - Aperçu du résultat final
   
   - ⚙️ **Actions**:
     - Bouton "Appliquer le Crop"
     - Bouton "Réinitialiser"

#### 3. **Intégration dans `image_view.py`**
   - Nouveau onglet **"✂️ Cropping"** ajouté comme 2e onglet
   - Les onglets existants ont été décalés:
     - Tab 1: 🏠 Vue d'ensemble
     - Tab 2: ✂️ **Cropping** (NOUVEAU)
     - Tab 3: 🎨 Prétraitement (anciennement Tab 2)
     - Tab 4: 🔧 Transformations (anciennement Tab 3)
     - Tab 5: 📊 Analyse (anciennement Tab 4)
     - Tab 6: 💾 Export (anciennement Tab 6)

#### 4. **Mise à jour d'`api_client.py`**
   - Ajout du endpoint "crop" dans `API_ENDPOINTS`
   - Permet une meilleure organisation des appels API

---

## 🚀 Utilisation

### Pour un utilisateur:

1. **Charger une image** via le bouton de téléchargement
2. **Naviguer vers l'onglet "✂️ Cropping"**
3. **Ajuster les paramètres**:
   - Utiliser les sliders pour définir la région
   - OU utiliser les présets pour des formats courants
4. **Prévisualiser** les deux images côte à côte
5. **Appliquer le crop** via le bouton "Appliquer le Crop"
6. L'image est mise à jour dans l'historique et prête pour d'autres transformations

---

## 📝 Exemples de code

### Backend - Appel à la méthode crop_image:
```python
result = processor.crop_image(image_bytes, x=100, y=100, width=400, height=300)
```

### Frontend - Utilisation du composant:
```python
from components.crop import render_crop

# Dans un onglet ou section
with tab_crop:
    render_crop()
```

---

## 🔌 Intégration avec l'historique

- Chaque crop appliqué est enregistré dans l'historique
- Les utilisateurs peuvent naviguer l'historique avec undo/redo
- Les paramètres du crop sont sauvegardés: `{x, y, width, height}`
- Le compteur d'opérations est incrémenté

---

## ⚠️ Validation et Gestion d'erreurs

### Backend:
- ✅ Validation de la taille du fichier (max 10MB)
- ✅ Validation du type MIME (image/*)
- ✅ Vérification que les coordonnées ne dépassent pas les limites
- ✅ Gestion des dimensions minimales

### Frontend:
- ✅ Limitation des sliders selon la taille de l'image
- ✅ Messages d'erreur utilisateur-friendly
- ✅ Gestion de la déconnexion au backend
- ✅ Validation des paramètres entiers

---

## 📂 Fichiers modifiés

1. ✅ `backend/app/infrastructure/image_processor.py` - Méthode crop_image ajoutée
2. ✅ `backend/app/api/preprocess.py` - Endpoint /crop ajouté
3. ✅ `frontend/components/crop.py` - **Nouveau fichier**
4. ✅ `frontend/components/image_view.py` - Onglet cropping ajouté
5. ✅ `frontend/services/api_client.py` - Endpoint crop ajouté

---

## 🎨 Design

- Interface cohérente avec le reste de l'application
- Icônes emoji pour une meilleure UX
- Feedback utilisateur en temps réel
- Aperçu visuel avec zone d'assombrissement

---

## 🔮 Améliorations futures possibles

- Cropping libre (drawrect en cliquant)
- Aspect ratio locked
- Drag & drop pour la sélection
- Présets personnalisés
- Export direct avec watermark
- EXIF data preservation

---

## ✅ Tests recommandés

- [ ] Charger une petite image (100x100px)
- [ ] Charger une grande image (4000x3000px)
- [ ] Tester tous les présets
- [ ] Tester undo/redo après crop
- [ ] Tester export après crop
- [ ] Tester avec images sans alpha channel
