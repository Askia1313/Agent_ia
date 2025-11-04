# Script PowerShell pour démarrer Docker et lancer les tests
# Usage: .\run_tests.ps1

Write-Host "🚀 Démarrage du système RAG et des tests" -ForegroundColor Cyan
Write-Host "=" * 80

# 1. Arrêter les conteneurs existants
Write-Host "`n🛑 Arrêt des conteneurs existants..." -ForegroundColor Yellow
docker compose down 2>$null

# 2. Démarrer Docker Compose en arrière-plan
Write-Host "`n🐳 Démarrage de Docker Compose..." -ForegroundColor Cyan
docker compose up --build -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Erreur lors du démarrage de Docker Compose" -ForegroundColor Red
    Write-Host "Vérifiez que Docker Desktop est démarré" -ForegroundColor Yellow
    exit 1
}

# 3. Attendre que les services soient prêts
Write-Host "`n⏳ Attente du démarrage des services (30 secondes)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# 4. Vérifier que l'API est accessible
Write-Host "`n🔍 Vérification de l'API..." -ForegroundColor Cyan
$maxRetries = 10
$retryCount = 0
$apiReady = $false

while ($retryCount -lt $maxRetries -and -not $apiReady) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health/" -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            $apiReady = $true
            Write-Host "✅ API accessible" -ForegroundColor Green
        }
    } catch {
        $retryCount++
        Write-Host "⏳ Tentative $retryCount/$maxRetries..." -ForegroundColor Yellow
        Start-Sleep -Seconds 3
    }
}

if (-not $apiReady) {
    Write-Host "`n❌ L'API n'est pas accessible après $maxRetries tentatives" -ForegroundColor Red
    Write-Host "`n📋 Logs du backend:" -ForegroundColor Yellow
    docker compose logs backend
    exit 1
}

# 5. Lancer les tests
Write-Host "`n🧪 Lancement des tests..." -ForegroundColor Cyan
Write-Host "=" * 80
python test_rag_system.py

# 6. Afficher les logs en cas d'erreur
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Les tests ont échoué" -ForegroundColor Red
    Write-Host "`n📋 Voulez-vous voir les logs Docker? (O/N)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq "O" -or $response -eq "o") {
        docker compose logs
    }
}

Write-Host "`n✅ Script terminé" -ForegroundColor Green
