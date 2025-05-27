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
from models import Mesa, Producto, Pedido, Ticket, MovimientoStock

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
    productos = Producto.query.filter_by(activo=True).order_by(Producto.categoria, Producto.orden, Producto.nombre).all()
    
    # Agrupar productos por categoría
    productos_por_categoria = {}
    productos_dict = {}
    for producto in productos:
        if producto.categoria not in productos_por_categoria:
            productos_por_categoria[producto.categoria] = []
        productos_por_categoria[producto.categoria].append(producto)
        productos_dict[producto.id] = producto
    
    # Get current order for this table if exists
    pedido_actual = Pedido.query.filter_by(mesa_id=mesa_id, estado='abierto').first()
    
    return render_template('table_detail.html', 
                         mesa=mesa, 
                         productos_por_categoria=productos_por_categoria,
                         productos_dict=productos_dict,
                         pedido_actual=pedido_actual)

@app.route('/add_to_order', methods=['POST'])
def add_to_order():
    """Add product to table order - accumulates by rounds"""
    mesa_id = int(request.form.get('mesa_id'))
    producto_id = int(request.form.get('producto_id'))
    cantidad = int(request.form.get('cantidad', 1))
    
    mesa = Mesa.query.get_or_404(mesa_id)
    producto = Producto.query.get_or_404(producto_id)
    
    # Get or create current order
    pedido = Pedido.query.filter_by(mesa_id=mesa_id, estado='abierto').first()
    if not pedido:
        pedido = Pedido(
            mesa_id=mesa_id, 
            productos='{}',
            total=0.0, 
            estado='abierto'
        )
        db.session.add(pedido)
        mesa.estado = 'ocupada'
        db.session.flush()  # Get the ID
    
    # Update products (storing as JSON with product_id as key and quantity as value)
    import json
    if pedido.productos:
        productos_dict = json.loads(pedido.productos)
    else:
        productos_dict = {}
    
    # Add or update product quantity (accumulate by rounds)
    producto_id_str = str(producto_id)
    if producto_id_str in productos_dict:
        productos_dict[producto_id_str] += cantidad
    else:
        productos_dict[producto_id_str] = cantidad
    
    # Save updated products and calculate total
    pedido.productos = json.dumps(productos_dict)
    
    # Calculate total
    total = 0
    for pid, qty in productos_dict.items():
        prod = Producto.query.get(int(pid))
        if prod:
            total += float(prod.precio) * qty
    
    pedido.total = total
    
    db.session.commit()
    return '', 200  # Return success for AJAX call

@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    """Update product quantity in current order"""
    mesa_id = int(request.form.get('mesa_id'))
    producto_id = int(request.form.get('producto_id'))
    change = int(request.form.get('change'))
    
    pedido = Pedido.query.filter_by(mesa_id=mesa_id, estado='abierto').first()
    if not pedido:
        return '', 404
    
    import json
    productos_dict = json.loads(pedido.productos) if pedido.productos else {}
    producto_id_str = str(producto_id)
    
    if producto_id_str in productos_dict:
        productos_dict[producto_id_str] += change
        if productos_dict[producto_id_str] <= 0:
            del productos_dict[producto_id_str]
    
    # Recalculate total
    total = 0
    for pid, qty in productos_dict.items():
        prod = Producto.query.get(int(pid))
        if prod:
            total += float(prod.precio) * qty
    
    pedido.productos = json.dumps(productos_dict)
    pedido.total = total
    
    # If no products left, delete the order
    if not productos_dict:
        mesa = Mesa.query.get(mesa_id)
        mesa.estado = 'libre'
        db.session.delete(pedido)
    
    db.session.commit()
    return '', 200

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

@app.route('/pay_order/<int:mesa_id>')
def pay_order(mesa_id):
    """Process payment for table with method selection"""
    payment_method = request.args.get('payment_method', 'efectivo')
    mesa = Mesa.query.get_or_404(mesa_id)
    
    # Look for closed or open order to pay
    pedido = Pedido.query.filter_by(mesa_id=mesa_id).filter(
        Pedido.estado.in_(['cerrado', 'abierto'])
    ).first()
    
    if not pedido:
        flash('No hay pedido para pagar en esta mesa', 'error')
        return redirect(url_for('index'))
    
    # Process payment
    pedido.forma_pago = payment_method
    pedido.fecha_pago = datetime.utcnow()
    pedido.estado = 'pagado'
    
    # Create ticket for automatic printing
    ticket = Ticket(
        pedido_id=pedido.id
    )
    db.session.add(ticket)
    
    # Free the table
    mesa.estado = 'libre'
    
    db.session.commit()
    flash(f'Pago procesado ({payment_method}). Ticket generado automáticamente.', 'success')
    
    # Automatically redirect to print receipt
    return redirect(url_for('print_receipt', pedido_id=pedido.id))

@app.route('/print_receipt/<int:pedido_id>')
def print_receipt(pedido_id):
    """Generate printable receipt with detailed product information"""
    pedido = Pedido.query.get_or_404(pedido_id)
    mesa = Mesa.query.get(pedido.mesa_id)
    
    # Parse products and get detailed information
    import json
    productos_dict = json.loads(pedido.productos) if pedido.productos else {}
    
    # Build detailed products list with quantities and prices
    productos_detalle = []
    for producto_id_str, cantidad in productos_dict.items():
        producto = Producto.query.get(int(producto_id_str))
        if producto:
            productos_detalle.append({
                'nombre': producto.nombre,
                'precio': float(producto.precio),
                'cantidad': cantidad,
                'subtotal': float(producto.precio) * cantidad
            })
    
    return render_template('receipt_print.html', 
                         pedido=pedido, 
                         mesa=mesa,
                         productos_detalle=productos_detalle)

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

@app.route('/inventory')
def inventory():
    """Inventory management view"""
    productos = Producto.query.filter_by(activo=True).order_by(Producto.categoria, Producto.nombre).all()
    
    # Estadísticas de stock
    productos_agotados = [p for p in productos if p.stock_agotado]
    productos_bajo_stock = [p for p in productos if p.stock_bajo and not p.stock_agotado]
    
    return render_template('inventory.html', 
                         productos=productos,
                         productos_agotados=productos_agotados,
                         productos_bajo_stock=productos_bajo_stock)

@app.route('/update_stock', methods=['POST'])
def update_stock():
    """Update product stock"""
    producto_id = int(request.form.get('producto_id'))
    nuevo_stock = int(request.form.get('nuevo_stock'))
    motivo = request.form.get('motivo', 'ajuste_inventario')
    
    producto = Producto.query.get_or_404(producto_id)
    stock_anterior = producto.stock_actual
    
    # Crear movimiento de stock
    movimiento = MovimientoStock(
        producto_id=producto_id,
        tipo_movimiento='ajuste',
        cantidad=nuevo_stock - stock_anterior,
        motivo=motivo,
        stock_anterior=stock_anterior,
        stock_nuevo=nuevo_stock
    )
    
    # Actualizar stock
    producto.stock_actual = nuevo_stock
    producto.fecha_actualizacion = datetime.utcnow()
    
    db.session.add(movimiento)
    db.session.commit()
    
    flash(f'Stock de {producto.nombre} actualizado a {nuevo_stock}', 'success')
    return redirect(url_for('inventory'))

@app.route('/add_stock', methods=['POST'])
def add_stock():
    """Add stock to product"""
    producto_id = int(request.form.get('producto_id'))
    cantidad = int(request.form.get('cantidad'))
    motivo = request.form.get('motivo', 'compra')
    
    producto = Producto.query.get_or_404(producto_id)
    stock_anterior = producto.stock_actual
    nuevo_stock = stock_anterior + cantidad
    
    # Crear movimiento de entrada
    movimiento = MovimientoStock(
        producto_id=producto_id,
        tipo_movimiento='entrada',
        cantidad=cantidad,
        motivo=motivo,
        stock_anterior=stock_anterior,
        stock_nuevo=nuevo_stock
    )
    
    # Actualizar stock
    producto.stock_actual = nuevo_stock
    producto.fecha_actualizacion = datetime.utcnow()
    
    db.session.add(movimiento)
    db.session.commit()
    
    flash(f'Añadidas {cantidad} unidades a {producto.nombre}', 'success')
    return redirect(url_for('inventory'))

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
