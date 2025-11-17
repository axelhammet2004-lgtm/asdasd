@echo off
chcp 65001 >nul
title Servidor HTTPS Flasher Wilobu v2.1

echo.
echo ===================================================================
echo    SERVIDOR HTTPS PARA FLASHER WILOBU v2.1
echo ===================================================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado
    echo.
    echo Descarga Python desde: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Iniciando servidor HTTPS...
echo.
python server_https.py

pause
