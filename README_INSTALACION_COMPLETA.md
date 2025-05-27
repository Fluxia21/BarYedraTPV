# 🍺 Bar Yedra TPV - Guía de Instalación Completa

## 📋 Resumen del Sistema
Sistema de punto de venta completo para Bar Yedra, compatible con Windows 7 y Python 3.8.

## 📁 Estructura de Archivos Necesarios

```
BarYedra/
├── bar_yedra_tpv.py              # Sistema principal
├── INICIAR_BAR_YEDRA.bat         # Acceso directo principal
├── INSTALAR_DEPENDENCIAS.bat     # Instalador automático
├── templates/
│   ├── base_tpv.html             # Template base
│   ├── index_tpv.html            # Página de mesas
│   └── products_tpv.html         # Página de productos
└── README_INSTALACION_COMPLETA.md
```

## 🚀 Instalación Paso a Paso

### PASO 1: Instalar Python 3.8
1. Descargar: https://www.python.org/downloads/release/python-3812/
2. Archivo: `python-3.8.12-amd64.exe`
3. **IMPORTANTE**: Marcar "Add Python 3.8 to PATH"
4. Instalar con configuración predeterminada

### PASO 2: Crear los archivos
Crear una carpeta `C:\BarYedra\` y dentro crear todos los archivos listados abajo.

### PASO 3: Instalar dependencias
1. Ejecutar como administrador: `INSTALAR_DEPENDENCIAS.bat`
2. Esperar a que termine la instalación

### PASO 4: ¡Usar el sistema!
1. Doble clic en `INICIAR_BAR_YEDRA.bat`
2. Se abre automáticamente el navegador
3. Sistema TPV funcionando

## 📄 Código de los Archivos

### 1. INSTALAR_DEPENDENCIAS.bat
```batch
@echo off
title Instalador Bar Yedra TPV
color 0B
cls

echo ===============================================
echo    INSTALADOR DE DEPENDENCIAS BAR YEDRA
echo ===============================================
echo.

echo 🔍 Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Python no encontrado
    echo.
    echo Necesitas instalar Python 3.8 para Windows 7:
    echo https://www.python.org/downloads/release/python-3812/
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado correctamente
echo.
echo 📦 Instalando dependencias...
echo.

python -m pip install --upgrade pip
pip install flask==2.3.3

echo.
echo ✅ Instalación completada
echo.
echo 🎉 Ya puedes ejecutar: INICIAR_BAR_YEDRA.bat
echo.
pause
```

### 2. INICIAR_BAR_YEDRA.bat
```batch
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

cd /d "%~dp0"

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python no encontrado
    pause
    exit /b 1
)

echo ✅ Iniciando Bar Yedra TPV...
python bar_yedra_tpv.py

echo.
echo 🛑 Sistema cerrado
pause
```

## 💡 Alternativas para Obtener los Archivos

### Opción 1: Copiar y pegar
1. Copia el código de cada archivo desde el chat
2. Pégalo en Notepad
3. Guarda con el nombre correcto

### Opción 2: Descargar individual
1. Ve a cada archivo en el proyecto
2. Clic derecho → "Guardar como"
3. Guarda en la carpeta BarYedra

### Opción 3: Recrear desde cero
1. Usa este README como guía
2. Crea cada archivo manualmente
3. Copia el código proporcionado

## 📞 Soporte
Si tienes problemas:
1. Verifica que Python 3.8 esté instalado correctamente
2. Asegúrate de que todos los archivos estén en la carpeta correcta
3. Ejecuta como administrador los archivos .bat

## 🎯 Para el Dueño del Bar
Una vez instalado:
1. Crear acceso directo de `INICIAR_BAR_YEDRA.bat` en el escritorio
2. Renombrarlo a "🍺 Bar Yedra TPV"
3. Solo hacer doble clic cada día para abrir el sistema

## ✨ Características del Sistema
- ✅ Gestión de productos con botones de editar/eliminar
- ✅ Sistema de mesas por zonas
- ✅ Base de datos automática
- ✅ Interfaz táctil optimizada
- ✅ Compatible con Windows 7