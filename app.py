import os
import logging
import json
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "yedra-bar-secret-key-2024")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure SQLite database for local operation
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///yedra_bar.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Import models after db initialization
from models import Mesa, Producto, Pedido, Ticket

# Add custom Jinja2 filter for JSON parsing
@app.template_filter('from_json')
def from_json_filter(value):
    """Convert JSON string to Python object"""
    if value:
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return []
    return []

@app.route('/')
def index():
    """Main dashboard showing all tables by zone"""
    mesas_terraza = Mesa.query.filter_by(zona='Terraza').all()
    mesas_sala = Mesa.query.filter_by(zona='Sala').all()
    mesas_barra = Mesa.query.filter_by(zona='Barra').all()
    
    return render_template('index.html', 
                         mesas_terraza=mesas_terraza,
                         mesas_sala=mesas_sala,
                         mesas_barra=mesas_barra)

@app.route('/mesa/<int:mesa_id>')
def table_detail(mesa_id):
    """Table detail view for managing orders"""
    mesa = Mesa.query.get_or_404(mesa_id)
    productos = Producto.query.all()
    
    # Get current order for this table if exists
    pedido_actual = Pedido.query.filter_by(mesa_id=mesa_id, estado='abierto').first()
    
    return render_template('table_detail.html', 
                         mesa=mesa, 
                         productos=productos,
                         pedido_actual=pedido_actual)

@app.route('/add_to_order', methods=['POST'])
def add_to_order():
    """Add product to table order"""
    mesa_id = request.form.get('mesa_id')
    producto_id = request.form.get('producto_id')
    cantidad = int(request.form.get('cantidad', 1))
    
    mesa = Mesa.query.get_or_404(mesa_id)
    producto = Producto.query.get_or_404(producto_id)
    
    # Get or create current order
    pedido = Pedido.query.filter_by(mesa_id=mesa_id, estado='abierto').first()
    if not pedido:
        pedido = Pedido(mesa_id=mesa_id, total=0.0, estado='abierto')
        db.session.add(pedido)
        mesa.estado = 'ocupada'
    
    # Add product to order (simplified - storing as JSON-like string)
    if pedido.productos:
        import json
        productos_list = json.loads(pedido.productos)
    else:
        productos_list = []
    
    # Check if product already in order
    found = False
    for item in productos_list:
        if item['producto_id'] == int(producto_id):
            item['cantidad'] += cantidad
            item['subtotal'] = item['cantidad'] * item['precio']
            found = True
            break
    
    if not found:
        productos_list.append({
            'producto_id': int(producto_id),
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'cantidad': cantidad,
            'subtotal': cantidad * float(producto.precio)
        })
    
    import json
    pedido.productos = json.dumps(productos_list)
    pedido.total = sum(item['subtotal'] for item in productos_list)
    
    db.session.commit()
    flash(f'Añadido {cantidad}x {producto.nombre} al pedido', 'success')
    
    return redirect(url_for('table_detail', mesa_id=mesa_id))

@app.route('/close_order/<int:mesa_id>')
def close_order(mesa_id):
    """Close order and set table as ready to pay"""
    mesa = Mesa.query.get_or_404(mesa_id)
    pedido = Pedido.query.filter_by(mesa_id=mesa_id, estado='abierto').first()
    
    if pedido:
        pedido.estado = 'cerrado'
        mesa.estado = 'pagada'
        db.session.commit()
        flash('Pedido cerrado. Mesa lista para pagar.', 'success')
    
    return redirect(url_for('index'))

@app.route('/pay_order/<int:mesa_id>', methods=['POST'])
def pay_order(mesa_id):
    """Process payment for table"""
    forma_pago = request.form.get('forma_pago')
    mesa = Mesa.query.get_or_404(mesa_id)
    pedido = Pedido.query.filter_by(mesa_id=mesa_id, estado='cerrado').first()
    
    if pedido:
        pedido.forma_pago = forma_pago
        pedido.fecha_pago = datetime.now()
        pedido.estado = 'pagado'
        
        # Create ticket
        ticket = Ticket(pedido_id=pedido.id)
        db.session.add(ticket)
        
        # Free the table
        mesa.estado = 'libre'
        
        db.session.commit()
        flash(f'Pago procesado ({forma_pago}). Mesa liberada.', 'success')
    
    return redirect(url_for('index'))

@app.route('/print_receipt/<int:pedido_id>')
def print_receipt(pedido_id):
    """Generate printable receipt"""
    pedido = Pedido.query.get_or_404(pedido_id)
    mesa = Mesa.query.get(pedido.mesa_id)
    
    import json
    productos_list = json.loads(pedido.productos) if pedido.productos else []
    
    return render_template('receipt_print.html', 
                         pedido=pedido, 
                         mesa=mesa,
                         productos=productos_list)

@app.route('/cash_register')
def cash_register():
    """Daily cash register view"""
    today = date.today()
    
    # Get today's paid orders
    pedidos_hoy = Pedido.query.filter(
        db.func.date(Pedido.fecha_pago) == today,
        Pedido.estado == 'pagado'
    ).all()
    
    total_efectivo = sum(p.total for p in pedidos_hoy if p.forma_pago == 'efectivo')
    total_tarjeta = sum(p.total for p in pedidos_hoy if p.forma_pago == 'tarjeta')
    total_dia = total_efectivo + total_tarjeta
    
    return render_template('cash_register.html',
                         pedidos_hoy=pedidos_hoy,
                         total_efectivo=total_efectivo,
                         total_tarjeta=total_tarjeta,
                         total_dia=total_dia,
                         fecha=today)

@app.route('/close_cash_register', methods=['POST'])
def close_cash_register():
    """Close daily cash register"""
    today = date.today()
    
    # Archive today's data (in a real system, you might move to archive table)
    pedidos_hoy = Pedido.query.filter(
        db.func.date(Pedido.fecha_pago) == today,
        Pedido.estado == 'pagado'
    ).all()
    
    if pedidos_hoy:
        flash(f'Caja cerrada. {len(pedidos_hoy)} pedidos archivados.', 'success')
    else:
        flash('No hay pedidos para cerrar hoy.', 'info')
    
    return redirect(url_for('cash_register'))

@app.route('/products')
def products():
    """Product management view"""
    productos = Producto.query.filter_by(activo=True).order_by(Producto.categoria, Producto.orden, Producto.nombre).all()
    
    # Agrupar productos por categoría
    productos_por_categoria = {}
    for producto in productos:
        if producto.categoria not in productos_por_categoria:
            productos_por_categoria[producto.categoria] = []
        productos_por_categoria[producto.categoria].append(producto)
    
    return render_template('products.html', productos_por_categoria=productos_por_categoria)

@app.route('/add_product', methods=['POST'])
def add_product():
    """Add new product with photo, category and description"""
    nombre = request.form.get('nombre')
    precio = float(request.form.get('precio'))
    categoria = request.form.get('categoria', 'General')
    foto_url = request.form.get('foto_url', '')
    descripcion = request.form.get('descripcion', '')
    
    producto = Producto(
        nombre=nombre, 
        precio=precio,
        categoria=categoria,
        foto_url=foto_url,
        descripcion=descripcion
    )
    db.session.add(producto)
    db.session.commit()
    
    flash(f'Producto {nombre} añadido correctamente en {categoria}', 'success')
    return redirect(url_for('products'))

@app.route('/delete_product/<int:producto_id>')
def delete_product(producto_id):
    """Delete product"""
    producto = Producto.query.get_or_404(producto_id)
    db.session.delete(producto)
    db.session.commit()
    
    flash(f'Producto {producto.nombre} eliminado', 'success')
    return redirect(url_for('products'))

# Create tables and initialize data
with app.app_context():
    db.create_all()
    
    # Initialize sample data if tables are empty
    if Mesa.query.count() == 0:
        # Create tables for each zone
        zonas = {
            'Terraza': 6,  # 6 tables in terrace
            'Sala': 8,     # 8 tables in main room
            'Barra': 4     # 4 bar spots
        }
        
        for zona, num_mesas in zonas.items():
            for i in range(1, num_mesas + 1):
                mesa = Mesa(numero=i, zona=zona, estado='libre')
                db.session.add(mesa)
        
        # Add sample products
        productos_iniciales = [
            ('Café Solo', 1.20),
            ('Café con Leche', 1.40),
            ('Cortado', 1.30),
            ('Té', 1.20),
            ('Agua', 1.50),
            ('Coca Cola', 2.00),
            ('Cerveza', 2.50),
            ('Vino Tinto', 2.00),
            ('Vino Blanco', 2.00),
            ('Tostada con Tomate', 2.50),
            ('Bocadillo Jamón', 4.50),
            ('Tortilla Española', 3.50),
            ('Patatas Bravas', 3.00),
            ('Aceitunas', 2.00),
        ]
        
        for nombre, precio in productos_iniciales:
            producto = Producto(nombre=nombre, precio=precio)
            db.session.add(producto)
        
        db.session.commit()
        print("Database initialized with sample data")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
