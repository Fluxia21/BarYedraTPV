#!/usr/bin/env python3
"""
Database initialization script for Bar Yedra TPV System
Run this script to set up the database with initial data
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Mesa, Producto, Pedido, Ticket

def init_database():
    """Initialize the database with tables and sample data"""
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Check if data already exists
        if Mesa.query.count() > 0:
            print("Database already contains data. Skipping initialization.")
            return
        
        print("Adding tables...")
        
        # Create tables for each zone
        zonas_mesas = {
            'Terraza': 6,  # 6 tables in terrace
            'Sala': 8,     # 8 tables in main room
            'Barra': 4     # 4 bar spots
        }
        
        mesa_count = 0
        for zona, num_mesas in zonas_mesas.items():
            for i in range(1, num_mesas + 1):
                mesa = Mesa(numero=i, zona=zona, estado='libre')
                db.session.add(mesa)
                mesa_count += 1
        
        print(f"Added {mesa_count} tables")
        
        # Add sample products with realistic bar prices
        productos_iniciales = [
            # Cafés
            ('Café solo', 1.60),
            ('Café con leche', 1.80),
            ('Café con leche sin lactosa', 1.80),
            ('Café con leche y hielo', 1.70),
            ('Café para llevar', 1.70),
            ('Café bombón', 2.00),
            ('Cortado', 1.30),
            ('TERRAZA CAFÉ CON LECHE', 1.50),
            ('TERRAZA CAFÉ CON LECHE HIELO', 1.70),
            ('TERRAZA CAFÉ CON 2CHUR', 2.50),
            
            # Tés e Infusiones
            ('Infusión', 2.00),
            ('ColaCao infusión', 3.30),
            ('Taza de chocolate', 2.30),
            ('Té', 1.20),
            ('Manzanilla', 1.20),
            ('Poleo', 1.20),
            ('Té Verde', 1.30),
            
            # Desayunos
            ('Café con 2 churros', 2.70),
            ('Churro o porra', 0.80),
            ('Churro o porra TERRAZA UN', 0.80),
            ('DESAYUNO CLÁSICO', 3.00),
            ('DESAYUNO ESPECIAL', 4.70),
            ('TERRAZA DESAYUNO', 2.80),
            ('TERRAZA DESAY. COLA CAO', 3.10),
            ('Vaso de leche', 1.60),
            ('Zumo de naranja', 2.80),
            ('BOLLERÍA', 1.70),
            ('Mantequilla o mermelada', 0.30),
            ('Suplemento aceite o tomate', 0.30),
            ('Suplemento leche sin lactosa', 0.20),
            
            # Bebidas Frías
            ('Agua Mineral', 1.50),
            ('Agua con Gas', 1.60),
            ('Coca Cola', 2.00),
            ('Fanta Naranja', 2.00),
            ('Sprite', 2.00),
            ('Aquarius', 2.20),
            ('Zumo Natural Naranja', 2.50),
            ('Zumo Tomate', 2.00),
            
            # Bebidas Alcohólicas
            ('Cerveza Estrella', 2.50),
            ('Cerveza Mahou', 2.50),
            ('Cerveza sin Alcohol', 2.20),
            ('Vino Tinto', 2.00),
            ('Vino Blanco', 2.00),
            ('Vino Rosado', 2.00),
            ('Jerez', 2.50),
            ('Whisky', 4.00),
            ('Vodka', 3.50),
            ('Gin Tonic', 4.50),
            ('Rum Cola', 4.00),
            
            # Tapas y Comida
            ('Tostada con Tomate', 2.50),
            ('Tostada con Mantequilla', 2.00),
            ('Bocadillo Jamón York', 4.50),
            ('Bocadillo Jamón Serrano', 5.50),
            ('Bocadillo Chorizo', 4.00),
            ('Bocadillo Queso', 3.50),
            ('Bocadillo Tortilla', 4.00),
            ('Tortilla Española', 3.50),
            ('Tortilla Francesa', 3.00),
            ('Patatas Bravas', 3.00),
            ('Aceitunas', 2.00),
            ('Aceitunas Rellenas', 2.50),
            ('Almendras', 2.50),
            ('Jamón Serrano', 8.50),
            ('Queso Manchego', 6.00),
            ('Croquetas (6 uds)', 4.50),
            ('Calamares', 6.00),
            ('Boquerones', 4.50),
            
            # Raciones
            ('Ensalada Mixta', 5.50),
            ('Ensalada de Tomate', 4.50),
            ('Gambas al Ajillo', 8.50),
            ('Pulpo a la Gallega', 9.50),
            ('Paella (por persona)', 12.00),
            ('Pescado del Día', 10.00),
            ('Solomillo', 15.00),
            
            # Postres
            ('Flan Casero', 3.00),
            ('Natillas', 2.50),
            ('Helado (3 bolas)', 3.50),
            ('Fruta del Tiempo', 3.00),
            ('Tarta del Día', 3.50),
            
            # Helados
            ('KIKOS', 3.10),
            ('Dulce de leche', 3.10),
            ('Hazell Roll', 2.70),
            ('Ibizza Roll', 2.70),
            ('Crik Crak', 2.70),
            ('LACASITOS (snack)', 2.70),
            ('LACASITOS (helado)', 3.10),
            ('GOL', 2.60),
            ('Granini', 2.10),
            ('Mint lolly', 2.10),
            ('Cacaolat', 3.00),
            ('Mini polos', 2.60),
            ('FORMAT XL', 3.10),
            ('Polos fresa', 2.10),
            ('Polos limón', 2.10),
            ('Trina naranja', 2.60),
            ('CONO SIN AZÚCARES AÑADIDOS', 3.10),
            ('DONUTS', 3.00),
            ('CHUPACHUPS', 3.00),
            ('DANONINO', 2.60),
        ]
        
        producto_count = 0
        
        # Definir categorías automáticas basadas en los productos
        categorias_productos = {
            'Cafés': ['Café solo', 'Café con leche', 'Café con leche sin lactosa', 'Café con leche y hielo', 'Café para llevar', 'Café bombón', 'Cortado', 'Carajillo', 'Descafeinado', 'TERRAZA CAFÉ CON LECHE', 'TERRAZA CAFÉ CON LECHE HIELO', 'TERRAZA CAFÉ CON 2CHUR'],
            'Tés e Infusiones': ['Infusión', 'ColaCao infusión', 'Taza de chocolate', 'Té', 'Manzanilla', 'Poleo', 'Tila', 'Té Verde'],
            'Desayunos': ['Café con 2 churros', 'Churro o porra', 'Churro o porra TERRAZA UN', 'DESAYUNO CLÁSICO', 'DESAYUNO ESPECIAL', 'TERRAZA DESAYUNO', 'TERRAZA DESAY. COLA CAO', 'Vaso de leche', 'Zumo de naranja', 'BOLLERÍA', 'Mantequilla o mermelada', 'Suplemento aceite o tomate', 'Suplemento leche sin lactosa'],
            'Refrescos': ['Coca Cola', 'Coca Cola Zero', 'Fanta Naranja', 'Fanta Limón', 'Sprite', 'Aquarius', 'Nestea', 'Agua'],
            'Cervezas': ['Cerveza Caña', 'Cerveza Botellín', 'Cerveza Sin Alcohol'],
            'Vinos': ['Vino Tinto', 'Vino Blanco', 'Vino Rosado'],
            'Licores Premium': ['Anís', 'Pacharán', 'Licor de Hierbas', 'Brandy', 'Coñac', 'Jerez', 'Whisky', 'Vodka', 'Gin Tonic', 'Rum Cola'],
            'Tapas y Comida': ['Tostada con Tomate', 'Tostada con Mantequilla', 'Bocadillo Jamón York', 'Bocadillo Jamón Serrano', 'Bocadillo Chorizo', 'Bocadillo Queso', 'Bocadillo Tortilla', 'Tortilla Española', 'Tortilla Francesa', 'Patatas Bravas', 'Aceitunas', 'Aceitunas Rellenas', 'Almendras', 'Jamón Serrano', 'Queso Manchego', 'Croquetas (6 uds)', 'Calamares', 'Boquerones'],
            'Raciones': ['Ensalada Mixta', 'Ensalada de Tomate', 'Gambas al Ajillo', 'Pulpo a la Gallega', 'Paella (por persona)', 'Pescado del Día', 'Solomillo'],
            'Postres': ['Flan Casero', 'Natillas', 'Helado (3 bolas)', 'Fruta del Tiempo', 'Tarta del Día'],
            'HELADOS': ['KIKOS', 'Dulce de leche', 'Hazell Roll', 'Ibizza Roll', 'Crik Crak', 'LACASITOS (snack)', 'LACASITOS (helado)', 'GOL', 'Granini', 'Mint lolly', 'Cacaolat', 'Mini polos', 'FORMAT XL', 'Polos fresa', 'Polos limón', 'Trina naranja', 'CONO SIN AZÚCARES AÑADIDOS', 'DONUTS', 'CHUPACHUPS', 'DANONINO']
        }
        
        for nombre, precio in productos_iniciales:
            # Determinar la categoría del producto
            categoria = 'General'  # Categoría por defecto
            for cat, productos in categorias_productos.items():
                if nombre in productos:
                    categoria = cat
                    break
            
            producto = Producto(nombre=nombre, precio=precio, categoria=categoria, activo=True)
            db.session.add(producto)
            producto_count += 1
        
        print(f"Added {producto_count} products")
        
        # Commit all changes
        db.session.commit()
        
        print("Database initialization completed successfully!")
        print("\nSummary:")
        print(f"- {mesa_count} tables created across 3 zones")
        print(f"- {producto_count} products added to catalog")
        print("\nZone distribution:")
        for zona, num in zonas_mesas.items():
            print(f"  - {zona}: {num} tables")
        
        print("\nYou can now start the application with: python main.py")

def reset_database():
    """Reset the database (drop all tables and recreate)"""
    with app.app_context():
        print("WARNING: This will delete all data!")
        confirm = input("Are you sure you want to reset the database? (yes/no): ")
        
        if confirm.lower() == 'yes':
            print("Dropping all tables...")
            db.drop_all()
            print("Recreating tables...")
            init_database()
        else:
            print("Database reset cancelled.")

def show_stats():
    """Show database statistics"""
    with app.app_context():
        mesas_count = Mesa.query.count()
        productos_count = Producto.query.count()
        pedidos_count = Pedido.query.count()
        tickets_count = Ticket.query.count()
        
        print("Database Statistics:")
        print(f"- Tables: {mesas_count}")
        print(f"- Products: {productos_count}")
        print(f"- Orders: {pedidos_count}")
        print(f"- Tickets: {tickets_count}")
        
        print("\nTable status:")
        for estado in ['libre', 'ocupada', 'pagada']:
            count = Mesa.query.filter_by(estado=estado).count()
            print(f"- {estado.title()}: {count}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'reset':
            reset_database()
        elif command == 'stats':
            show_stats()
        else:
            print("Usage: python init_db.py [reset|stats]")
    else:
        init_database()
