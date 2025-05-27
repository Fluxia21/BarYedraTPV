#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bar Yedra TPV - Sistema completo para Windows 7
Compatible con Python 3.8
"""

import os
import sqlite3
import webbrowser
import threading
import time
import zipfile
import io
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import json

# Crear aplicación Flask
app = Flask(__name__)
app.secret_key = 'bar-yedra-2024-secret'

# Configuración de base de datos
DB_PATH = 'bar_yedra_tpv.db'

def crear_base_datos():
    """Crear y configurar base de datos SQLite"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabla productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT DEFAULT 'General',
            descripcion TEXT,
            foto_url TEXT,
            activo INTEGER DEFAULT 1,
            fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla mesas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER NOT NULL,
            zona TEXT NOT NULL,
            estado TEXT DEFAULT 'libre'
        )
    ''')
    
    # Tabla pedidos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mesa_id INTEGER,
            productos_json TEXT,
            total REAL DEFAULT 0,
            fecha_creacion TEXT,
            fecha_pago TEXT,
            forma_pago TEXT,
            estado TEXT DEFAULT 'abierto',
            FOREIGN KEY (mesa_id) REFERENCES mesas (id)
        )
    ''')
    
    # Insertar datos iniciales si no existen
    cursor.execute('SELECT COUNT(*) FROM productos')
    if cursor.fetchone()[0] == 0:
        productos_iniciales = [
            ('Café Solo', 1.50, 'Cafés', 'Café espresso tradicional', ''),
            ('Café con Leche', 1.80, 'Cafés', 'Café con leche caliente', ''),
            ('Cortado', 1.60, 'Cafés', 'Café cortado con leche', ''),
            ('Tostada con Tomate', 2.50, 'Desayunos', 'Tostada con tomate rallado', ''),
            ('Tostada con Mantequilla', 2.20, 'Desayunos', 'Tostada con mantequilla', ''),
            ('Bocadillo de Jamón', 4.00, 'Montados', 'Bocadillo de jamón serrano', ''),
            ('Bocadillo de Queso', 3.50, 'Montados', 'Bocadillo de queso', ''),
            ('Tortilla Española', 3.80, 'Platos Calientes', 'Tortilla de patatas casera', ''),
            ('Patatas Bravas', 4.50, 'Platos Calientes', 'Patatas con salsa brava', ''),
            ('Cerveza', 2.00, 'Bebidas', 'Cerveza de barril', ''),
            ('Agua', 1.50, 'Bebidas', 'Agua mineral', ''),
            ('Refresco', 2.20, 'Bebidas', 'Coca-Cola, Fanta, etc', ''),
        ]
        
        cursor.executemany(
            'INSERT INTO productos (nombre, precio, categoria, descripcion, foto_url) VALUES (?, ?, ?, ?, ?)',
            productos_iniciales
        )
    
    # Insertar mesas si no existen
    cursor.execute('SELECT COUNT(*) FROM mesas')
    if cursor.fetchone()[0] == 0:
        mesas_iniciales = [
            (1, 'Terraza'), (2, 'Terraza'), (3, 'Terraza'), (4, 'Terraza'),
            (5, 'Sala'), (6, 'Sala'), (7, 'Sala'), (8, 'Sala'),
            (9, 'Barra'), (10, 'Barra')
        ]
        
        cursor.executemany(
            'INSERT INTO mesas (numero, zona) VALUES (?, ?)',
            mesas_iniciales
        )
    
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente")

@app.route('/')
def index():
    """Página principal - mesas"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mesas ORDER BY zona, numero')
    mesas_raw = cursor.fetchall()
    conn.close()
    
    # Agrupar mesas por zona
    mesas_por_zona = {}
    for mesa in mesas_raw:
        zona = mesa[2]
        if zona not in mesas_por_zona:
            mesas_por_zona[zona] = []
        mesas_por_zona[zona].append({
            'id': mesa[0],
            'numero': mesa[1],
            'zona': mesa[2],
            'estado': mesa[3]
        })
    
    return render_template('index_tpv.html', mesas_por_zona=mesas_por_zona)

@app.route('/products')
def products():
    """Página de gestión de productos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE activo = 1 ORDER BY categoria, nombre')
    productos_raw = cursor.fetchall()
    conn.close()
    
    # Agrupar por categoría
    productos_por_categoria = {}
    for producto in productos_raw:
        categoria = producto[3]
        if categoria not in productos_por_categoria:
            productos_por_categoria[categoria] = []
        productos_por_categoria[categoria].append({
            'id': producto[0],
            'nombre': producto[1],
            'precio': producto[2],
            'categoria': producto[3],
            'descripcion': producto[4] or '',
            'foto_url': producto[5] or ''
        })
    
    return render_template('products_tpv.html', productos_por_categoria=productos_por_categoria)

@app.route('/add_product', methods=['POST'])
def add_product():
    """Añadir nuevo producto"""
    try:
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        categoria = request.form['categoria']
        descripcion = request.form.get('descripcion', '')
        foto_url = request.form.get('foto_url', '')
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO productos (nombre, precio, categoria, descripcion, foto_url) VALUES (?, ?, ?, ?, ?)',
            (nombre, precio, categoria, descripcion, foto_url)
        )
        conn.commit()
        conn.close()
        
        flash(f'Producto "{nombre}" añadido correctamente', 'success')
    except Exception as e:
        flash(f'Error al añadir producto: {str(e)}', 'error')
    
    return redirect(url_for('products'))

@app.route('/update_product/<int:producto_id>', methods=['POST'])
def update_product(producto_id):
    """Actualizar producto existente"""
    try:
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        categoria = request.form['categoria']
        descripcion = request.form.get('descripcion', '')
        foto_url = request.form.get('foto_url', '')
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE productos SET nombre=?, precio=?, categoria=?, descripcion=?, foto_url=? WHERE id=?',
            (nombre, precio, categoria, descripcion, foto_url, producto_id)
        )
        conn.commit()
        conn.close()
        
        flash(f'Producto actualizado correctamente', 'success')
    except Exception as e:
        flash(f'Error al actualizar producto: {str(e)}', 'error')
    
    return redirect(url_for('products'))

@app.route('/delete_product/<int:producto_id>')
def delete_product(producto_id):
    """Eliminar producto"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Obtener nombre del producto antes de eliminarlo
        cursor.execute('SELECT nombre FROM productos WHERE id=?', (producto_id,))
        resultado = cursor.fetchone()
        nombre = resultado[0] if resultado else 'Producto'
        
        cursor.execute('DELETE FROM productos WHERE id=?', (producto_id,))
        conn.commit()
        conn.close()
        
        flash(f'Producto "{nombre}" eliminado correctamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar producto: {str(e)}', 'error')
    
    return redirect(url_for('products'))

def abrir_navegador():
    """Abrir navegador automáticamente"""
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:5000')
        print("🌐 Navegador abierto automáticamente")
    except:
        print("⚠️  Abre manualmente: http://localhost:5000")

@app.route('/download_sistema_completo')
def download_sistema_completo():
    """Crear y descargar ZIP con todo el sistema TPV"""
    import zipfile
    import io
    
    # Crear ZIP en memoria
    memoria = io.BytesIO()
    
    with zipfile.ZipFile(memoria, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        
        # 1. Sistema principal Python
        codigo_principal = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sqlite3, webbrowser, threading, time
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
import json

app = Flask(__name__)
app.secret_key = 'bar-yedra-2024-secret'
DB_PATH = 'bar_yedra_tpv.db'

def crear_base_datos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(\\'''CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        categoria TEXT DEFAULT 'General',
        descripcion TEXT,
        foto_url TEXT,
        activo INTEGER DEFAULT 1
    )\\''')
    
    cursor.execute(\\'''CREATE TABLE IF NOT EXISTS mesas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero INTEGER NOT NULL,
        zona TEXT NOT NULL,
        estado TEXT DEFAULT 'libre'
    )\\''')
    
    cursor.execute('SELECT COUNT(*) FROM productos')
    if cursor.fetchone()[0] == 0:
        productos = [
            ('Café Solo', 1.50, 'Cafés', 'Café espresso tradicional'),
            ('Café con Leche', 1.80, 'Cafés', 'Café con leche caliente'),
            ('Tostada con Tomate', 2.50, 'Desayunos', 'Tostada con tomate rallado'),
            ('Bocadillo de Jamón', 4.00, 'Montados', 'Bocadillo de jamón serrano'),
            ('Tortilla Española', 3.80, 'Platos Calientes', 'Tortilla de patatas casera'),
            ('Cerveza', 2.00, 'Bebidas', 'Cerveza de barril'),
        ]
        cursor.executemany('INSERT INTO productos (nombre, precio, categoria, descripcion) VALUES (?, ?, ?, ?)', productos)
    
    cursor.execute('SELECT COUNT(*) FROM mesas')
    if cursor.fetchone()[0] == 0:
        mesas = [(1, 'Terraza'), (2, 'Terraza'), (3, 'Sala'), (4, 'Sala'), (5, 'Barra'), (6, 'Barra')]
        cursor.executemany('INSERT INTO mesas (numero, zona) VALUES (?, ?)', mesas)
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mesas ORDER BY zona, numero')
    mesas_raw = cursor.fetchall()
    conn.close()
    
    mesas_por_zona = {}
    for mesa in mesas_raw:
        zona = mesa[2]
        if zona not in mesas_por_zona:
            mesas_por_zona[zona] = []
        mesas_por_zona[zona].append({'id': mesa[0], 'numero': mesa[1], 'zona': mesa[2], 'estado': mesa[3]})
    
    return render_template('index_tpv.html', mesas_por_zona=mesas_por_zona)

@app.route('/products')
def products():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE activo = 1 ORDER BY categoria, nombre')
    productos_raw = cursor.fetchall()
    conn.close()
    
    productos_por_categoria = {}
    for producto in productos_raw:
        categoria = producto[3]
        if categoria not in productos_por_categoria:
            productos_por_categoria[categoria] = []
        productos_por_categoria[categoria].append({
            'id': producto[0], 'nombre': producto[1], 'precio': producto[2],
            'categoria': producto[3], 'descripcion': producto[4] or '', 'foto_url': producto[5] or ''
        })
    
    return render_template('products_tpv.html', productos_por_categoria=productos_por_categoria)

@app.route('/add_product', methods=['POST'])
def add_product():
    try:
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        categoria = request.form['categoria']
        descripcion = request.form.get('descripcion', '')
        foto_url = request.form.get('foto_url', '')
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO productos (nombre, precio, categoria, descripcion, foto_url) VALUES (?, ?, ?, ?, ?)',
                      (nombre, precio, categoria, descripcion, foto_url))
        conn.commit()
        conn.close()
        flash(f'Producto "{nombre}" añadido correctamente', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('products'))

@app.route('/update_product/<int:producto_id>', methods=['POST'])
def update_product(producto_id):
    try:
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        categoria = request.form['categoria']
        descripcion = request.form.get('descripcion', '')
        foto_url = request.form.get('foto_url', '')
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('UPDATE productos SET nombre=?, precio=?, categoria=?, descripcion=?, foto_url=? WHERE id=?',
                      (nombre, precio, categoria, descripcion, foto_url, producto_id))
        conn.commit()
        conn.close()
        flash('Producto actualizado correctamente', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('products'))

@app.route('/delete_product/<int:producto_id>')
def delete_product(producto_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT nombre FROM productos WHERE id=?', (producto_id,))
        resultado = cursor.fetchone()
        nombre = resultado[0] if resultado else 'Producto'
        cursor.execute('DELETE FROM productos WHERE id=?', (producto_id,))
        conn.commit()
        conn.close()
        flash(f'Producto "{nombre}" eliminado correctamente', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('products'))

def abrir_navegador():
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:5000')
        print("🌐 Navegador abierto automáticamente")
    except:
        print("⚠️  Abre manualmente: http://localhost:5000")

def main():
    print("=" * 50)
    print("🍺 BAR YEDRA - SISTEMA TPV")
    print("=" * 50)
    crear_base_datos()
    threading.Thread(target=abrir_navegador, daemon=True).start()
    print("🚀 Servidor iniciado en: http://localhost:5000")
    print("=" * 50)
    try:
        app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\\n🛑 Servidor detenido")

if __name__ == '__main__':
    main()'''

        # 2. Archivo de inicio
        inicio_bat = '''@echo off
title Bar Yedra TPV
color 0A
cls
echo ===============================================
echo           BAR YEDRA - SISTEMA TPV
echo ===============================================
echo.
echo 🚀 Iniciando sistema...
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
pause'''

        # 3. Instalador
        instalador_bat = '''@echo off
title Instalador Bar Yedra TPV
color 0B
cls
echo ===============================================
echo    INSTALADOR DE DEPENDENCIAS BAR YEDRA
echo ===============================================
echo.
python --version
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python no encontrado
    echo Instala Python 3.8 desde:
    echo https://www.python.org/downloads/release/python-3812/
    pause
    exit /b 1
)
echo ✅ Python encontrado
echo 📦 Instalando dependencias...
python -m pip install flask==2.3.3
echo ✅ Instalación completada
echo 🎉 Ya puedes ejecutar: INICIAR_BAR_YEDRA.bat
pause'''

        # Leer templates existentes
        try:
            with open('templates/base_tpv.html', 'r', encoding='utf-8') as f:
                base_html = f.read()
            with open('templates/index_tpv.html', 'r', encoding='utf-8') as f:
                index_html = f.read()
            with open('templates/products_tpv.html', 'r', encoding='utf-8') as f:
                products_html = f.read()
        except:
            # Templates básicos si no se pueden leer
            base_html = '''<!DOCTYPE html><html><head><title>Bar Yedra TPV</title><style>body{font-family:Arial;background:#f5f5f5}.header{background:#2e7d32;color:white;padding:20px;text-align:center}.nav{background:#1b5e20;padding:15px;text-align:center}.nav a{color:white;text-decoration:none;padding:10px 20px;margin:0 10px;background:#4caf50;border-radius:5px}</style></head><body><div class="header"><h1>🍺 Bar Yedra TPV</h1></div><div class="nav"><a href="/">🏠 Mesas</a><a href="/products">📦 Productos</a></div><div style="max-width:1200px;margin:20px auto;padding:0 20px">{% block content %}{% endblock %}</div></body></html>'''
            index_html = '''{% extends "base_tpv.html" %}{% block content %}<h2>🍽️ Gestión de Mesas</h2>{% for zona, mesas in mesas_por_zona.items() %}<h3>{{ zona }}</h3><div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:15px">{% for mesa in mesas %}<div style="background:#d4edda;border:2px solid #4caf50;border-radius:8px;padding:20px;text-align:center"><div style="font-size:24px;font-weight:bold">Mesa {{ mesa.numero }}</div><div style="background:#4caf50;color:white;padding:5px;border-radius:20px;margin-top:10px">✅ {{ mesa.estado }}</div></div>{% endfor %}</div>{% endfor %}{% endblock %}'''
            products_html = '''{% extends "base_tpv.html" %}{% block content %}<style>.product-card{background:white;border:2px solid #ddd;border-radius:10px;padding:20px;margin:10px}.product-buttons{display:flex;gap:10px;margin-top:15px}.btn-edit-orange{flex:1;padding:12px;background:#ff8c00;color:white;border:none;border-radius:6px;font-weight:bold;cursor:pointer}.btn-delete-red{flex:1;padding:12px;background:#dc3545;color:white;border:none;border-radius:6px;font-weight:bold;cursor:pointer}</style><h2>📦 Productos</h2>{% for categoria, productos in productos_por_categoria.items() %}<h3>{{ categoria }}</h3>{% for producto in productos %}<div class="product-card"><h4>{{ producto.nombre }}</h4><p>€{{ "%.2f"|format(producto.precio) }}</p><p>{{ producto.descripcion }}</p><div class="product-buttons"><button class="btn-edit-orange" onclick="alert('Editar {{ producto.nombre }}')">✏️ EDITAR</button><button class="btn-delete-red" onclick="if(confirm('¿Eliminar {{ producto.nombre }}?')) window.location.href='/delete_product/{{ producto.id }}'">🗑️ ELIMINAR</button></div></div>{% endfor %}{% endfor %}{% endblock %}'''

        # Añadir archivos al ZIP
        zip_file.writestr('bar_yedra_tpv.py', codigo_principal)
        zip_file.writestr('INICIAR_BAR_YEDRA.bat', inicio_bat)
        zip_file.writestr('INSTALAR_DEPENDENCIAS.bat', instalador_bat)
        zip_file.writestr('templates/base_tpv.html', base_html)
        zip_file.writestr('templates/index_tpv.html', index_html)
        zip_file.writestr('templates/products_tpv.html', products_html)
        
        # README de instalación
        readme = '''# 🍺 Bar Yedra TPV - Instalación

## Pasos para instalar:
1. Instalar Python 3.8 desde: https://www.python.org/downloads/release/python-3812/
   (Marcar "Add Python 3.8 to PATH")
2. Ejecutar como administrador: INSTALAR_DEPENDENCIAS.bat
3. Usar diariamente: INICIAR_BAR_YEDRA.bat

## Para el dueño del bar:
- Crear acceso directo de INICIAR_BAR_YEDRA.bat en el escritorio
- Solo hacer doble clic cada día para abrir el sistema TPV
'''
        zip_file.writestr('README_INSTALACION.md', readme)
    
    memoria.seek(0)
    return send_file(
        memoria,
        mimetype='application/zip',
        as_attachment=True,
        download_name='BarYedra_TPV_Sistema_Completo.zip'
    )

def main():
    """Función principal"""
    print("=" * 50)
    print("🍺 BAR YEDRA - SISTEMA TPV")
    print("=" * 50)
    print("🔧 Preparando sistema...")
    
    # Crear base de datos
    crear_base_datos()
    
    # Abrir navegador en hilo separado
    threading.Thread(target=abrir_navegador, daemon=True).start()
    
    print("🚀 Servidor iniciado en: http://localhost:5000")
    print("🔴 Para cerrar: Presiona Ctrl+C o cierra esta ventana")
    print("=" * 50)
    
    try:
        app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("Presiona Enter para cerrar...")

if __name__ == '__main__':
    main()