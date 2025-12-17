# Script de démarrage de l'application ImageFlow Pro avec la fonctionnalité Cropping
# Compatible Windows PowerShell

Write-Host "╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     ImageFlow Pro - Application de Traitement d'Images              ║" -ForegroundColor Cyan
Write-Host "║         Avec nouvelle fonctionnalité: CROPPING                      ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Configuration
$PROJECT_PATH = "c:\Users\Administrator\Documents\Institut\ING-2\Traitement-Image\App_Web_Image"

# Vérification du répertoire
Write-Host "[1/4] Vérification du répertoire..." -ForegroundColor Yellow
if (-not (Test-Path $PROJECT_PATH)) {
    Write-Host "❌ Le répertoire n'existe pas: $PROJECT_PATH" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Répertoire trouvé" -ForegroundColor Green
Write-Host ""

# Navigation vers le répertoire
Write-Host "[2/4] Navigation vers le répertoire du projet..." -ForegroundColor Yellow
Set-Location $PROJECT_PATH
Write-Host "✅ Dans le répertoire: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# Affichage des instructions
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║ INSTRUCTIONS POUR DÉMARRER L'APPLICATION                           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "🖥️  TERMINAL 1 - BACKEND (FastAPI)" -ForegroundColor Green
Write-Host "────────────────────────────────────" -ForegroundColor Green
Write-Host "Exécutez cette commande:" -ForegroundColor White
Write-Host ""
Write-Host "    cd `"$PROJECT_PATH`"" -ForegroundColor Cyan
Write-Host "    uv run uvicorn backend.app.main:app --reload" -ForegroundColor Cyan
Write-Host ""
Write-Host "Attendez que le message s'affiche:" -ForegroundColor White
Write-Host "    ✅ Uvicorn running on http://127.0.0.1:8000" -ForegroundColor Green
Write-Host ""
Write-Host "Vous pouvez accéder à:" -ForegroundColor White
Write-Host "    • API Docs (Swagger): http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "    • ReDoc: http://localhost:8000/redoc" -ForegroundColor Yellow
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

Write-Host "🌐 TERMINAL 2 - FRONTEND (Streamlit)" -ForegroundColor Green
Write-Host "────────────────────────────────────" -ForegroundColor Green
Write-Host "Exécutez cette commande:" -ForegroundColor White
Write-Host ""
Write-Host "    cd `"$PROJECT_PATH`"" -ForegroundColor Cyan
Write-Host "    streamlit run frontend/app.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "L'application s'ouvrira automatiquement à:" -ForegroundColor White
Write-Host "    http://localhost:8501" -ForegroundColor Yellow
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

Write-Host "📝 UTILISER LA NOUVELLE FONCTIONNALITÉ CROPPING" -ForegroundColor Magenta
Write-Host "─────────────────────────────────────────────" -ForegroundColor Magenta
Write-Host "1. Charger une image via le bouton de téléchargement" -ForegroundColor White
Write-Host "2. Cliquer sur l'onglet `"✂️ Cropping`" (2e onglet)" -ForegroundColor White
Write-Host "3. Ajuster les paramètres:" -ForegroundColor White
Write-Host "   • Sliders: Position X/Y, Largeur, Hauteur" -ForegroundColor White
Write-Host "   • Présets: Carré, 16:9, 9:16, 4:3" -ForegroundColor White
Write-Host "4. Prévisualiser le résultat (avant/après)" -ForegroundColor White
Write-Host "5. Cliquer `"✂️ Appliquer le Crop`"" -ForegroundColor White
Write-Host "6. L'image est mise à jour et prête pour d'autres transformations" -ForegroundColor White
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

Write-Host "🧪 TESTER L'API DIRECTEMENT" -ForegroundColor Blue
Write-Host "──────────────────────────" -ForegroundColor Blue
Write-Host "Vous pouvez tester l'endpoint /crop à partir de:" -ForegroundColor White
Write-Host ""
Write-Host "1. Swagger UI (recommandé):" -ForegroundColor Yellow
Write-Host "   http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "   • Trouver l'endpoint POST /crop" -ForegroundColor White
Write-Host "   • Cliquer `"Try it out`"" -ForegroundColor White
Write-Host "   • Charger une image et définir les paramètres" -ForegroundColor White
Write-Host ""
Write-Host "2. Via PowerShell:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   `$form = @{" -ForegroundColor Cyan
Write-Host "       'file' = Get-Item 'path\to\image.png'" -ForegroundColor Cyan
Write-Host "       'x' = '100'" -ForegroundColor Cyan
Write-Host "       'y' = '50'" -ForegroundColor Cyan
Write-Host "       'width' = '400'" -ForegroundColor Cyan
Write-Host "       'height' = '300'" -ForegroundColor Cyan
Write-Host "   }" -ForegroundColor Cyan
Write-Host "   Invoke-RestMethod -Uri 'http://localhost:8000/api/crop' \"" -ForegroundColor Cyan
Write-Host "       -Method Post -Form `$form -OutFile 'result.png'" -ForegroundColor Cyan
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

Write-Host "📚 DOCUMENTATION" -ForegroundColor Magenta
Write-Host "───────────────" -ForegroundColor Magenta
Write-Host "Consultez les fichiers suivants pour plus d'informations:" -ForegroundColor White
Write-Host ""
Write-Host "1. RESUME_CROPPING.md" -ForegroundColor Yellow
Write-Host "   └─ Résumé complet des implémentations" -ForegroundColor Gray
Write-Host ""
Write-Host "2. CROP_FEATURE.md" -ForegroundColor Yellow
Write-Host "   └─ Documentation détaillée de la fonctionnalité" -ForegroundColor Gray
Write-Host ""
Write-Host "3. TEST_CROPPING.md" -ForegroundColor Yellow
Write-Host "   └─ Guide de test avec exemples" -ForegroundColor Gray
Write-Host ""
Write-Host "4. ARCHITECTURE_CROPPING.md" -ForegroundColor Yellow
Write-Host "   └─ Diagrammes d'architecture et flux de données" -ForegroundColor Gray
Write-Host ""
Write-Host "5. EXEMPLE_VISUEL_CROPPING.md" -ForegroundColor Yellow
Write-Host "   └─ Aperçu visuel de l'interface" -ForegroundColor Gray
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

Write-Host "⚠️  DÉPANNAGE" -ForegroundColor Red
Write-Host "───────────" -ForegroundColor Red
Write-Host ""
Write-Host "Problème: `"Impossible de se connecter au backend`"" -ForegroundColor Yellow
Write-Host "Solution: Assurez-vous que le backend (uvicorn) est démarré sur le port 8000" -ForegroundColor Gray
Write-Host ""
Write-Host "Problème: `"Module not found`"" -ForegroundColor Yellow
Write-Host "Solution: Assurez-vous d'avoir exécuté 'uv sync' et les dépendances installées" -ForegroundColor Gray
Write-Host ""
Write-Host "Problème: `"Address already in use`"" -ForegroundColor Yellow
Write-Host "Solution: Le port 8000 (ou 8501) est déjà utilisé." -ForegroundColor Gray
Write-Host "          Tuez le processus: Stop-Process -Name python -Force" -ForegroundColor Gray
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

Write-Host "✅ Prêt? Ouvrez deux terminaux et exécutez les commandes ci-dessus!" -ForegroundColor Green
Write-Host ""

# Option pour démarrer automatiquement
$response = Read-Host "Voulez-vous que je démarre le backend maintenant? (oui/non)"
if ($response -eq "oui" -or $response -eq "o" -or $response -eq "yes" -or $response -eq "y") {
    Write-Host ""
    Write-Host "Démarrage du backend..." -ForegroundColor Green
    Write-Host ""
    & uv run uvicorn backend.app.main:app --reload
} else {
    Write-Host ""
    Write-Host "OK, démarrez manuellement le backend et le frontend comme indiqué ci-dessus." -ForegroundColor Yellow
    Write-Host ""
}
