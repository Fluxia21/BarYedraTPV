@echo off
title Bar Yedra TPV - Sistema de Punto de Venta
color 0A
echo.
echo =====================================
echo    BAR YEDRA - SISTEMA TPV
echo =====================================
echo.
echo Iniciando servidor...
echo.

cd /d "%~dp0"
python run_server.py

echo.
echo El servidor se ha cerrado.
echo Presiona cualquier tecla para salir...
pause >nul