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
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
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