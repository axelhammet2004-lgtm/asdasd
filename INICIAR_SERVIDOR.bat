@echo off
chcp 65001 >nul
title Servidor Web Flasher Wilobu v2.1

echo.
echo ===================================================================
echo    SERVIDOR WEB DE FLASHEO WILOBU v2.1
echo ===================================================================
echo.
echo Iniciando servidor HTTP en puerto 8080...
echo.
echo ===================================================================
echo    INSTRUCCIONES:
echo ===================================================================
echo.
echo 1. Abre Google Chrome o Microsoft Edge
echo 2. Navega a: http://localhost:8080
echo 3. Conecta tu ESP32 al USB
echo 4. Haz clic en 'INSTALAR FIRMWARE'
echo.
echo ===================================================================
echo.
echo Servidor corriendo... (Presiona Ctrl+C para detener)
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado o no esta en PATH
    echo.
    echo Instala Python desde: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Iniciar servidor HTTP
python -m http.server 8080

pause
