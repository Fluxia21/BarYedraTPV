@echo off
title Bar Yedra TPV - Sistema de Punto de Venta
color 0A
echo.
echo ===============================================
echo   BAR YEDRA - SISTEMA TPV
echo ===============================================
echo.
echo Verificando Python...

:: Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo.
    echo Por favor instala Python desde: https://python.org
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion
    pause
    exit /b 1
)

echo Python encontrado correctamente
echo.
echo Instalando dependencias necesarias...

:: Instalar dependencias
pip install flask flask-sqlalchemy openpyxl python-docx reportlab

echo.
echo Iniciando servidor...
echo.
echo INSTRUCCIONES:
echo - El navegador se abrira automaticamente
echo - Si no se abre, ve a: http://localhost:5000
echo - Para detener el servidor, presiona Ctrl+C
echo.

:: Ejecutar el servidor
python run_server.py

pause