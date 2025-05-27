@echo off
title Bar Yedra TPV - Sistema Completo
color 0A
cls

echo.
echo ===============================================
echo           BAR YEDRA - SISTEMA TPV
echo ===============================================
echo.
echo 🚀 Iniciando sistema...
echo.

REM Cambiar al directorio del archivo
cd /d "%~dp0"

REM Verificar que Python esté instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python no encontrado
    echo.
    echo Por favor instala Python 3.8 desde:
    echo https://www.python.org/downloads/release/python-3812/
    echo.
    pause
    exit /b 1
)

REM Ejecutar el sistema TPV
echo ✅ Python encontrado
echo ✅ Iniciando Bar Yedra TPV...
echo.
python bar_yedra_tpv.py

echo.
echo 🛑 Sistema cerrado
echo.
pause