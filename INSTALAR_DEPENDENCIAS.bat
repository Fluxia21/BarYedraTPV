@echo off
title Instalador Bar Yedra TPV
color 0B
cls

echo ===============================================
echo    INSTALADOR DE DEPENDENCIAS BAR YEDRA
echo ===============================================
echo.

REM Verificar Python
echo 🔍 Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Python no encontrado
    echo.
    echo Necesitas instalar Python 3.8 para Windows 7:
    echo https://www.python.org/downloads/release/python-3812/
    echo.
    echo IMPORTANTE: Durante la instalacion marca
    echo "Add Python 3.8 to PATH"
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado correctamente
echo.

echo 📦 Instalando dependencias necesarias...
echo.

REM Actualizar pip primero
echo Actualizando pip...
python -m pip install --upgrade pip

echo.
echo Instalando Flask...
pip install flask==2.3.3

echo.
echo ✅ Todas las dependencias instaladas correctamente
echo.
echo ===============================================
echo           INSTALACION COMPLETADA
echo ===============================================
echo.
echo 🎉 Ya puedes ejecutar: INICIAR_BAR_YEDRA.bat
echo.
pause