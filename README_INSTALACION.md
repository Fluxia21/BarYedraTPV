# Bar Yedra TPV - Instalación Independiente

## Sistema de Punto de Venta para Windows 7 + Google Chrome

### 📋 Requisitos del Sistema
- Windows 7 o superior
- Google Chrome (recomendado) o Firefox
- Python 3.7 o superior
- Conexión a internet (solo para instalación inicial)

### 🔧 Instalación Paso a Paso

#### 1. Instalar Python
1. Descargar Python desde: https://www.python.org/downloads/
2. **IMPORTANTE**: Durante la instalación, marcar ✅ "Add Python to PATH"
3. Ejecutar como administrador si es necesario

#### 2. Verificar Instalación de Python
Abrir "Símbolo del sistema" (cmd) y escribir:
```
python --version
```
Debe mostrar la versión instalada (ej: Python 3.8.10)

#### 3. Preparar la Aplicación
1. Descargar todos los archivos del sistema Bar Yedra
2. Colocar en una carpeta (ej: C:\BarYedra)
3. Asegurarse que estos archivos estén presentes:
   - `app.py`
   - `models.py`
   - `init_db.py`
   - `run_server.py`
   - `iniciar_bar_yedra.bat`
   - `dependencias.txt`
   - Carpeta `templates/`
   - Carpeta `static/`

#### 4. Instalación Automática
1. Hacer doble clic en `iniciar_bar_yedra.bat`
2. El sistema instalará automáticamente las dependencias
3. Se abrirá el navegador con la aplicación

#### 5. Instalación Manual (si falla la automática)
Abrir "Símbolo del sistema" en la carpeta de la aplicación:
```
pip install -r dependencias.txt
python run_server.py
```

### 🚀 Uso Diario

#### Iniciar la Aplicación
- Hacer doble clic en `iniciar_bar_yedra.bat`
- O ejecutar: `python run_server.py`
- El navegador se abrirá automáticamente en: http://localhost:5000

#### Detener la Aplicación
- Presionar `Ctrl + C` en la ventana del servidor
- O cerrar la ventana del comando

### 📁 Estructura de Archivos
```
BarYedra/
├── app.py                    # Aplicación principal
├── models.py                 # Base de datos
├── init_db.py               # Inicialización
├── run_server.py            # Servidor independiente
├── iniciar_bar_yedra.bat    # Inicio automático Windows
├── dependencias.txt         # Lista de librerías
├── yedra_bar.db            # Base de datos (se crea automáticamente)
├── templates/              # Plantillas HTML
│   ├── layout.html
│   ├── index.html
│   ├── table_detail.html
│   ├── products.html
│   ├── inventory.html
│   ├── reports.html
│   └── ...
└── static/                 # Archivos CSS/JS
    ├── css/
    ├── js/
    └── img/
```

### 🔧 Solución de Problemas

#### "Python no está instalado"
- Reinstalar Python marcando "Add to PATH"
- Reiniciar el ordenador
- Verificar con: `python --version`

#### "Error al instalar dependencias"
- Verificar conexión a internet
- Ejecutar como administrador:
```
pip install --upgrade pip
pip install flask flask-sqlalchemy openpyxl python-docx reportlab
```

#### "No se abre el navegador"
- Abrir manualmente: http://localhost:5000
- Verificar que no haya otro programa usando el puerto 5000

#### "Error de base de datos"
- Borrar el archivo `yedra_bar.db`
- Reiniciar la aplicación para regenerar la base de datos

### 💡 Características Destacadas
- ✅ Funciona sin internet (después de la instalación)
- ✅ Base de datos local SQLite
- ✅ Interfaz optimizada para pantallas táctiles
- ✅ Compatible con Windows 7 y Chrome
- ✅ Backup automático de datos
- ✅ Reportes en Excel, Word y PDF

### 📞 Uso del Sistema
1. **Inicio**: Vista de mesas por zonas (Terraza, Sala, Barra)
2. **Pedidos**: Gestión de comandas por mesa
3. **Productos**: Administración del catálogo
4. **Inventario**: Control de stock
5. **Reportes**: Análisis de ventas semanales y mensuales
6. **Caja**: Gestión diaria de pagos

### 🔒 Seguridad
- Acceso solo desde el ordenador local (127.0.0.1)
- Base de datos protegida localmente
- Sin dependencias externas en funcionamiento

### 📝 Notas Importantes
- La aplicación NO requiere conexión a internet para funcionar
- Los datos se guardan localmente en `yedra_bar.db`
- Para hacer backup: copiar el archivo `yedra_bar.db`
- Compatible con cualquier navegador moderno (Chrome recomendado)