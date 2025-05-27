from app import db
from datetime import datetime

class Mesa(db.Model):
    """Table model"""
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    zona = db.Column(db.String(50), nullable=False)  # Terraza, Sala, Barra
    estado = db.Column(db.String(20), default='libre')  # libre, ocupada, pagada
    
    # Relationships
    pedidos = db.relationship('Pedido', backref='mesa', lazy=True)
    
    def __repr__(self):
        return f'<Mesa {self.zona} {self.numero}>'

class Producto(db.Model):
    """Product model"""
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Producto {self.nombre}>'

class Pedido(db.Model):
    """Order model"""
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
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Ticket {self.id}>'
