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
        
        # Add products organized by business priority
        productos_iniciales = [
            # CAFÉS Y BEBIDAS CALIENTES (Principal consumo)
            ('Café Solo', 1.60, 'Cafés', 1),
            ('Café con Leche', 1.80, 'Cafés', 2),
            ('Cortado', 1.30, 'Cafés', 3),
            ('Café Bombón', 2.00, 'Cafés', 4),
            ('Café con Leche Helado', 1.90, 'Cafés', 5),
            ('Café para Llevar', 1.70, 'Cafés', 6),
            ('Descafeinado Solo', 1.60, 'Cafés', 7),
            ('Descafeinado con Leche', 1.80, 'Cafés', 8),
            ('Carajillo', 2.50, 'Cafés', 9),
            
            # DESAYUNOS COMPLETOS (Alto consumo)
            ('Desayuno Clásico', 3.50, 'Desayunos', 1),
            ('Desayuno Especial', 4.50, 'Desayunos', 2),
            ('Café + Tostada', 3.20, 'Desayunos', 3),
            ('Café + 2 Churros', 2.70, 'Desayunos', 4),
            ('ColaCao + Churros', 3.30, 'Desayunos', 5),
            ('Chocolate + Churros', 3.50, 'Desayunos', 6),
            ('Zumo + Tostada', 4.20, 'Desayunos', 7),
            
            # BOCADILLOS FRÍOS (Alto consumo)
            ('Bocadillo Jamón York', 4.50, 'Bocadillos Fríos', 1),
            ('Bocadillo Jamón Serrano', 5.50, 'Bocadillos Fríos', 2),
            ('Bocadillo Queso', 3.50, 'Bocadillos Fríos', 3),
            ('Bocadillo Chorizo', 4.00, 'Bocadillos Fríos', 4),
            ('Bocadillo Lomo', 4.80, 'Bocadillos Fríos', 5),
            ('Bocadillo Atún', 4.20, 'Bocadillos Fríos', 6),
            ('Bocadillo Mixto', 4.00, 'Bocadillos Fríos', 7),
            
            # MONTADOS CALIENTES (Alto consumo)
            ('Montado Jamón y Queso', 5.50, 'Montados Calientes', 1),
            ('Montado Lomo y Queso', 5.80, 'Montados Calientes', 2),
            ('Montado York y Queso', 4.80, 'Montados Calientes', 3),
            ('Montado Chorizo', 4.50, 'Montados Calientes', 4),
            ('Montado Tortilla', 4.20, 'Montados Calientes', 5),
            ('Montado Bacon', 5.20, 'Montados Calientes', 6),
            
            # TOSTADAS Y BOLLERÍA (Alto consumo)
            ('Tostada con Tomate', 2.50, 'Tostadas', 1),
            ('Tostada con Mantequilla', 2.00, 'Tostadas', 2),
            ('Tostada con Mermelada', 2.30, 'Tostadas', 3),
            ('Tostada con Aceite', 2.00, 'Tostadas', 4),
            ('Churro', 0.80, 'Tostadas', 5),
            ('Porra', 0.90, 'Tostadas', 6),
            ('Croissant', 1.50, 'Tostadas', 7),
            ('Magdalena', 1.20, 'Tostadas', 8),
            
            # BEBIDAS FRÍAS (Consumo medio)
            ('Agua Mineral', 1.50, 'Bebidas Frías', 1),
            ('Coca Cola', 2.00, 'Bebidas Frías', 2),
            ('Fanta Naranja', 2.00, 'Bebidas Frías', 3),
            ('Sprite', 2.00, 'Bebidas Frías', 4),
            ('Aquarius', 2.20, 'Bebidas Frías', 5),
            ('Zumo Naranja Natural', 2.80, 'Bebidas Frías', 6),
            ('Zumo Tomate', 2.00, 'Bebidas Frías', 7),
            ('Nestea', 2.20, 'Bebidas Frías', 8),
            
            # CERVEZAS (Consumo medio)
            ('Cerveza Estrella', 2.50, 'Cervezas', 1),
            ('Cerveza Mahou', 2.50, 'Cervezas', 2),
            ('Cerveza sin Alcohol', 2.20, 'Cervezas', 3),
            ('Caña', 1.80, 'Cervezas', 4),
            ('Tercio', 2.80, 'Cervezas', 5),
            
            # INFUSIONES (Consumo medio)
            ('Té', 1.50, 'Infusiones', 1),
            ('Manzanilla', 1.50, 'Infusiones', 2),
            ('Poleo', 1.50, 'Infusiones', 3),
            ('Tila', 1.50, 'Infusiones', 4),
            ('Chocolate', 2.30, 'Infusiones', 5),
            ('ColaCao', 2.50, 'Infusiones', 6),
            
            # TAPAS RÁPIDAS (Consumo ocasional)
            ('Tortilla Española', 3.50, 'Tapas', 1),
            ('Tortilla Francesa', 3.00, 'Tapas', 2),
            ('Aceitunas', 2.00, 'Tapas', 3),
            ('Patatas Bravas', 3.50, 'Tapas', 4),
            ('Croquetas (6 uds)', 4.50, 'Tapas', 5),
            
            # SUPLEMENTOS Y EXTRAS
            ('Extra Tomate', 0.30, 'Suplementos', 1),
            ('Extra Aceite', 0.30, 'Suplementos', 2),
            ('Leche sin Lactosa', 0.20, 'Suplementos', 3),
            ('Extra Queso', 0.50, 'Suplementos', 4),
            ('Extra Jamón', 1.00, 'Suplementos', 5),
        ]
        
        # Create products with proper categorization
        for item in productos_iniciales:
            if len(item) == 5:  # New format with category and order
                nombre, precio, categoria, orden = item[0], item[1], item[2], item[3]
            else:  # Old format - skip these
                continue
                
            producto = Producto(
                nombre=nombre,
                precio=precio,
                categoria=categoria,
                orden=orden,
                activo=True,
                stock_actual=50,
                stock_minimo=5
            )
            db.session.add(producto)
        
        print(f"Added {len(productos_iniciales)} products")
        
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
