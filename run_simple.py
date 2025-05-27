import os
import webbrowser
import threading
import time
from flask import Flask

# Crear app Flask simple
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
    <head><title>Bar Yedra TPV</title></head>
    <body style="font-family: Arial; padding: 20px; background: #f0f0f0;">
        <h1 style="color: #2e7d32;">🍺 Bar Yedra - Sistema TPV</h1>
        <h2>¡Sistema funcionando correctamente!</h2>
        <p><a href="/products" style="background: #ff8c00; color: white; padding: 15px; text-decoration: none; border-radius: 5px;">Ver Productos</a></p>
    </body>
    </html>
    '''

@app.route('/products')
def products():
    return '''
    <html>
    <head><title>Productos - Bar Yedra</title></head>
    <body style="font-family: Arial; padding: 20px; background: #f0f0f0;">
        <h1>Productos del Bar</h1>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
            <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3>Café Solo</h3>
                <p>Precio: €1.50</p>
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <button style="flex: 1; padding: 12px; background: #ff8c00; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer;" onclick="alert('Editando Café Solo')">✏️ EDITAR</button>
                    <button style="flex: 1; padding: 12px; background: #dc3545; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer;" onclick="alert('Eliminando Café Solo')">🗑️ ELIMINAR</button>
                </div>
            </div>
            <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3>Café con Leche</h3>
                <p>Precio: €1.80</p>
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <button style="flex: 1; padding: 12px; background: #ff8c00; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer;" onclick="alert('Editando Café con Leche')">✏️ EDITAR</button>
                    <button style="flex: 1; padding: 12px; background: #dc3545; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer;" onclick="alert('Eliminando Café con Leche')">🗑️ ELIMINAR</button>
                </div>
            </div>
        </div>
        <p><a href="/" style="background: #2e7d32; color: white; padding: 10px; text-decoration: none; border-radius: 5px;">← Volver al Inicio</a></p>
    </body>
    </html>
    '''

def abrir_navegador():
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("🍺 BAR YEDRA - SISTEMA TPV")
    print("=" * 40)
    print("✅ Iniciando servidor...")
    
    threading.Thread(target=abrir_navegador, daemon=True).start()
    
    app.run(debug=False, host='127.0.0.1', port=5000)