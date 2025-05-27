#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bar Yedra TPV - Versión Simple para Windows 7
"""

import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import json

# Crear la aplicación Flask
app = Flask(__name__)
app.secret_key = 'bar-yedra-secret-key-2024'

# Base de datos SQLite simple
DB_FILE = 'bar_yedra.db'

def init_db():
    """Inicializar base de datos SQLite"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Crear tabla productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT DEFAULT 'General',
            descripcion TEXT,
            foto_url TEXT,
            activo BOOLEAN DEFAULT 1
        )
    ''')
    
    # Crear tabla mesas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER NOT NULL,
            zona TEXT NOT NULL,
            estado TEXT DEFAULT 'libre'
        )
    ''')
    
    # Crear tabla pedidos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mesa_id INTEGER,
            productos TEXT,
            total REAL DEFAULT 0,
            fecha_creacion TEXT,
            estado TEXT DEFAULT 'abierto'
        )
    ''')
    
    # Insertar productos de ejemplo si no existen
    cursor.execute('SELECT COUNT(*) FROM productos')
    if cursor.fetchone()[0] == 0:
        productos_ejemplo = [
            ('Café Solo', 1.50, 'Cafés', 'Café espresso tradicional'),
            ('Café con Leche', 1.80, 'Cafés', 'Café con leche caliente'),
            ('Tostada con Tomate', 2.50, 'Desayunos', 'Tostada de pan con tomate rallado'),
            ('Bocadillo de Jamón', 4.00, 'Montados', 'Bocadillo de jamón serrano'),
            ('Tortilla Española', 3.50, 'Platos Calientes', 'Tortilla de patatas casera'),
        ]
        
        for nombre, precio, categoria, descripcion in productos_ejemplo:
            cursor.execute(
                'INSERT INTO productos (nombre, precio, categoria, descripcion) VALUES (?, ?, ?, ?)',
                (nombre, precio, categoria, descripcion)
            )
    
    # Insertar mesas de ejemplo si no existen
    cursor.execute('SELECT COUNT(*) FROM mesas')
    if cursor.fetchone()[0] == 0:
        mesas_ejemplo = [
            (1, 'Terraza'), (2, 'Terraza'), (3, 'Terraza'),
            (4, 'Sala'), (5, 'Sala'), (6, 'Sala'),
            (7, 'Barra'), (8, 'Barra')
        ]
        
        for numero, zona in mesas_ejemplo:
            cursor.execute(
                'INSERT INTO mesas (numero, zona) VALUES (?, ?)',
                (numero, zona)
            )
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Página principal - mesas"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mesas ORDER BY zona, numero')
    mesas = cursor.fetchall()
    conn.close()
    
    # Agrupar mesas por zona
    mesas_por_zona = {}
    for mesa in mesas:
        zona = mesa[2]
        if zona not in mesas_por_zona:
            mesas_por_zona[zona] = []
        mesas_por_zona[zona].append({
            'id': mesa[0],
            'numero': mesa[1],
            'zona': mesa[2],
            'estado': mesa[3]
        })
    
    return render_template('index_simple.html', mesas_por_zona=mesas_por_zona)

@app.route('/products')
def products():
    """Página de productos"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE activo = 1 ORDER BY categoria, nombre')
    productos_raw = cursor.fetchall()
    conn.close()
    
    # Agrupar productos por categoría
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
    
    return render_template('products_simple.html', productos_por_categoria=productos_por_categoria)

@app.route('/add_product', methods=['POST'])
def add_product():
    """Añadir nuevo producto"""
    nombre = request.form['nombre']
    precio = float(request.form['precio'])
    categoria = request.form['categoria']
    descripcion = request.form.get('descripcion', '')
    foto_url = request.form.get('foto_url', '')
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO productos (nombre, precio, categoria, descripcion, foto_url) VALUES (?, ?, ?, ?, ?)',
        (nombre, precio, categoria, descripcion, foto_url)
    )
    conn.commit()
    conn.close()
    
    return redirect(url_for('products'))

@app.route('/update_product/<int:producto_id>', methods=['POST'])
def update_product(producto_id):
    """Actualizar producto"""
    nombre = request.form['nombre']
    precio = float(request.form['precio'])
    categoria = request.form['categoria']
    descripcion = request.form.get('descripcion', '')
    foto_url = request.form.get('foto_url', '')
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE productos SET nombre=?, precio=?, categoria=?, descripcion=?, foto_url=? WHERE id=?',
        (nombre, precio, categoria, descripcion, foto_url, producto_id)
    )
    conn.commit()
    conn.close()
    
    return redirect(url_for('products'))

@app.route('/delete_product/<int:producto_id>')
def delete_product(producto_id):
    """Eliminar producto"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id=?', (producto_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('products'))

if __name__ == '__main__':
    print("🍺 Inicializando Bar Yedra TPV...")
    init_db()
    print("✅ Base de datos lista")
    print("🚀 Iniciando servidor en http://localhost:5000")
    
    import webbrowser
    import threading
    import time
    
    def abrir_navegador():
        time.sleep(1)
        webbrowser.open('http://localhost:5000')
    
    threading.Thread(target=abrir_navegador).start()
    
    app.run(debug=False, host='127.0.0.1', port=5000)