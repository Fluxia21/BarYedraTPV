#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor independiente para Bar Yedra TPV
Compatible con Windows 7 y navegadores modernos
"""

import os
import sys
import time
import threading
import webbrowser
from app import app, db

def create_database():
    """Crear la base de datos si no existe"""
    with app.app_context():
        try:
            db.create_all()
            print("✅ Base de datos inicializada correctamente")
        except Exception as e:
            print(f"⚠️  Error al crear la base de datos: {e}")

def open_browser():
    """Abrir el navegador automáticamente después de un delay"""
    time.sleep(2)  # Esperar 2 segundos para que el servidor inicie
    url = "http://localhost:5000"
    try:
        webbrowser.open(url)
        print(f"🌐 Abriendo navegador en: {url}")
    except Exception as e:
        print(f"⚠️  No se pudo abrir el navegador automáticamente: {e}")
        print(f"   Abre manualmente: {url}")

def run_server():
    """Ejecutar el servidor Flask"""
    print("=" * 50)
    print("🍺 BAR YEDRA - SISTEMA TPV")
    print("=" * 50)
    print("🚀 Iniciando servidor...")
    
    # Crear base de datos
    create_database()
    
    # Abrir navegador en un hilo separado
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Configurar Flask
    app.config['DEBUG'] = False
    app.config['ENV'] = 'production'
    
    print("✅ Servidor iniciado correctamente")
    print("📱 Accede desde el navegador en: http://localhost:5000")
    print("🔴 Para cerrar: Presiona Ctrl+C o cierra esta ventana")
    print("=" * 50)
    
    try:
        # Ejecutar servidor Flask
        app.run(
            host='127.0.0.1',  # Solo localhost para seguridad
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error del servidor: {e}")
        input("Presiona Enter para cerrar...")

if __name__ == "__main__":
    run_server()