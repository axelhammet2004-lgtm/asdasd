# Servidor Web Local para Flashear ESP32
# Ejecuta este script y abre Chrome en: http://localhost:8080

$Port = 8080
$Path = "$PSScriptRoot"

Write-Host ""
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host "   SERVIDOR WEB DE FLASHEO WILOBU v2.1" -ForegroundColor Yellow
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Iniciando servidor HTTP en puerto $Port..." -ForegroundColor Green
Write-Host "Carpeta: $Path" -ForegroundColor Gray
Write-Host ""
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host "   INSTRUCCIONES:" -ForegroundColor Yellow
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Abre Google Chrome o Microsoft Edge" -ForegroundColor White
Write-Host "2. Navega a: http://localhost:$Port" -ForegroundColor Green
Write-Host "3. Conecta tu ESP32 al USB" -ForegroundColor White
Write-Host "4. Haz clic en 'INSTALAR FIRMWARE'" -ForegroundColor White
Write-Host ""
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Servidor corriendo... (Presiona Ctrl+C para detener)" -ForegroundColor Yellow
Write-Host ""

# Iniciar servidor HTTP simple
try {
    Push-Location $Path
    python -m http.server $Port
} catch {
    Write-Host "ERROR: Python no esta instalado o no esta en PATH" -ForegroundColor Red
    Write-Host "Instala Python desde: https://www.python.org/downloads/" -ForegroundColor Yellow
} finally {
    Pop-Location
}
