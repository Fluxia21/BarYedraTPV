@echo off
title Instalación de Dependencias - Bar Yedra TPV
color 0B
echo.
echo ===============================================
echo   INSTALACIÓN DE DEPENDENCIAS - BAR YEDRA
echo ===============================================
echo.
echo Instalando librerías necesarias...
echo.

pip install Flask==2.3.3
pip install Flask-SQLAlchemy==3.0.5
pip install Werkzeug==2.3.7
pip install Jinja2==3.1.2
pip install openpyxl==3.1.2
pip install python-docx==0.8.11
pip install reportlab==4.0.4
pip install SQLAlchemy==2.0.21

echo.
echo ===============================================
echo   INSTALACIÓN COMPLETADA
echo ===============================================
echo.
echo Ahora puedes ejecutar "iniciar_bar_yedra.bat"
echo para iniciar el sistema TPV
echo.
pause