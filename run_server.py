#!/usr/bin/env python3
"""
Servidor independiente para Bar Yedra TPV
Compatible con Windows 7 y navegadores modernos
"""

import os
import sys
import webbrowser
import threading
import time
from app import app, db

def create_database():
    """Crear la base de datos si no existe"""
    with app.app_context():
        db.create_all()
        print("✓ Base de datos inicializada")

def open_browser():
    """Abrir el navegador automáticamente después de un delay"""
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

def run_server():
    """Ejecutar el servidor Flask"""
    print("=" * 50)
    print("  BAR YEDRA - SISTEMA TPV")
    print("=" * 50)
    print("Iniciando servidor...")
    
    # Crear base de datos
    create_database()
    
    # Abrir navegador en un hilo separado
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    print("✓ Servidor ejecutándose en: http://localhost:5000")
    print("✓ Presiona Ctrl+C para detener el servidor")
    print("=" * 50)
    
    try:
        # Ejecutar servidor Flask
        app.run(
            host='127.0.0.1',  # Solo acceso local para seguridad
            port=5000,
            debug=False,  # Desactivar debug para producción
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n✓ Servidor detenido correctamente")
    except Exception as e:
        print(f"❌ Error al iniciar servidor: {e}")
        input("Presiona Enter para continuar...")

if __name__ == "__main__":
    run_server()