"""
Guide de test rapide pour la fonctionnalité Cropping
====================================================

Pour tester la nouvelle fonctionnalité de cropping, suivez ces étapes:

1. DÉMARRER L'APPLICATION
   
   Backend:
   ```
   uv run uvicorn backend.app.main:app --reload
   ```
   
   Frontend:
   ```
   streamlit run frontend/app.py
   ```

2. CHARGER UNE IMAGE
   
   - Cliquez sur "Charger une image"
   - Sélectionnez une image (PNG, JPG, BMP, TIFF, WebP)
   - L'image apparaît sur la page

3. NAVIGUER VERS LE TAB CROPPING
   
   - Cliquez sur l'onglet "✂️ Cropping" (2e onglet)
   - Vous verrez les paramètres de cropping et un aperçu

4. TESTER LES SLIDERS
   
   - Ajustez la position X (gauche)
   - Ajustez la position Y (haut)
   - Ajustez la largeur
   - Ajustez la hauteur
   - Observez l'aperçu en temps réel

5. TESTER LES PRÉSETS
   
   - Cliquez sur "🟩 Carré (1:1)"
   - Cliquez sur "🎬 16:9"
   - Cliquez sur "📱 9:16 (Portrait)"
   - Cliquez sur "🖼️ 4:3"
   - Vérifiez que les dimensions changent

6. APPLIQUER LE CROP
   
   - Cliquez sur "✂️ Appliquer le Crop"
   - L'image se met à jour
   - Vérifiez l'historique (le crop apparaît)

7. TESTER UNDO/REDO
   
   - Naviguez dans l'historique pour voir les étapes
   - Retournez au cropping original

8. EXPORTER L'IMAGE
   
   - Allez à l'onglet "💾 Export"
   - Téléchargez l'image croppée

POINTS DE VÉRIFICATION:
========================
✅ L'onglet Cropping s'affiche
✅ Les sliders fonctionnent (0 à limites de l'image)
✅ L'aperçu en temps réel est correct
✅ Les présets changent les dimensions
✅ Le bouton "Appliquer le Crop" fonctionne
✅ L'image s'met à jour après le crop
✅ L'historique enregistre le crop
✅ Le réinitialiser retourne à l'originale
✅ Le cropping peut être combiné avec d'autres opérations

ERREURS ATTENDUES À GÉRER:
============================
❌ Backend non démarré → Message "Impossible de se connecter au backend"
❌ Fichier trop volumineux → Message "File too large (max 10MB)"
❌ Région invalide → Message "Crop region has invalid dimensions"

"""

# Exemple d'utilisation en Python du endpoint crop:

import requests
from PIL import Image
import io

# Configuration
API_URL = "http://localhost:8000/api"
IMAGE_PATH = "test_image.png"

# Charger l'image
with open(IMAGE_PATH, 'rb') as f:
    files = {'file': ('test_image.png', f, 'image/png')}
    data = {
        'x': '100',
        'y': '50',
        'width': '400',
        'height': '300'
    }
    
    # Appeler l'API
    response = requests.post(
        f"{API_URL}/crop",
        files=files,
        data=data
    )
    
    # Sauvegarder le résultat
    if response.status_code == 200:
        cropped_image = Image.open(io.BytesIO(response.content))
        cropped_image.save('cropped_result.png')
        print("✅ Crop appliqué avec succès!")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.json())
