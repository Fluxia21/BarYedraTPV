@echo off
echo =====================================
echo  INSTALANDO DEPENDENCIAS BAR YEDRA
echo =====================================
echo.

echo Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.8 primero
    pause
    exit /b 1
)

echo.
echo Instalando dependencias...
pip install flask
pip install flask-sqlalchemy
pip install gunicorn
pip install jinja2
pip install werkzeug
pip install psycopg2-binary
pip install openpyxl
pip install python-docx
pip install reportlab
pip install email-validator

echo.
echo =====================================
echo  INSTALACION COMPLETADA
echo =====================================
echo.
echo Ahora puedes ejecutar: iniciar_bar_yedra.bat
pause