from app import db
from datetime import datetime

class Mesa(db.Model):
    """Table model"""
    __tablename__ = 'mesa'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    zona = db.Column(db.String(50), nullable=False)  # Terraza, Sala, Barra
    estado = db.Column(db.String(20), default='libre')  # libre, ocupada, pagada
    
    # Relationships
    pedidos = db.relationship('Pedido', backref='mesa', lazy=True)
    
    def __repr__(self):
        return f'<Mesa {self.zona} {self.numero}>'

class Producto(db.Model):
    """Product model with categories, photos and stock management"""
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    categoria = db.Column(db.String(50), nullable=False, default='General')
    foto_url = db.Column(db.String(255), nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    activo = db.Column(db.Boolean, default=True)
    orden = db.Column(db.Integer, default=0)  # Para ordenar productos en la interfaz
    
    # Stock management
    stock_actual = db.Column(db.Integer, default=0)  # Cantidad actual en stock
    stock_minimo = db.Column(db.Integer, default=5)  # Alerta cuando llegue a este nivel
    unidad_medida = db.Column(db.String(20), default='unidad')  # unidad, litro, kg, etc.
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Producto {self.nombre} - Stock: {self.stock_actual}>'
    
    @property
    def stock_bajo(self):
        """Retorna True si el stock está por debajo del mínimo"""
        return self.stock_actual <= self.stock_minimo
    
    @property
    def stock_agotado(self):
        """Retorna True si no hay stock"""
        return self.stock_actual <= 0

class Pedido(db.Model):
    """Order model"""
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    mesa_id = db.Column(db.Integer, db.ForeignKey('mesa.id'), nullable=False)
    productos = db.Column(db.Text)  # JSON string with products and quantities
    total = db.Column(db.Numeric(10, 2), default=0.00)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_pago = db.Column(db.DateTime)
    forma_pago = db.Column(db.String(20))  # efectivo, tarjeta
    estado = db.Column(db.String(20), default='abierto')  # abierto, cerrado, pagado
    
    # Relationships
    tickets = db.relationship('Ticket', backref='pedido', lazy=True)
    
    def __repr__(self):
        return f'<Pedido {self.id} Mesa {self.mesa_id}>'

class Ticket(db.Model):
    """Ticket/Receipt model"""
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Ticket {self.id}>'

class MovimientoStock(db.Model):
    """Stock movement tracking model"""
    __tablename__ = 'movimiento_stock'
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    tipo_movimiento = db.Column(db.String(20), nullable=False)  # 'entrada', 'salida', 'ajuste'
    cantidad = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(100), nullable=True)  # 'venta', 'compra', 'perdida', 'ajuste_inventario'
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    usuario = db.Column(db.String(50), default='sistema')
    stock_anterior = db.Column(db.Integer, nullable=False)
    stock_nuevo = db.Column(db.Integer, nullable=False)
    
    # Relationship
    producto = db.relationship('Producto', backref='movimientos_stock')
    
    def __repr__(self):
        return f'<MovimientoStock {self.tipo_movimiento} - {self.cantidad}>'
