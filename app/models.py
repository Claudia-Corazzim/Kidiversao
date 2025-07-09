from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

"""
Modelos de dados para Kidiversão - Marketplace de Festas Infantis
"""

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))  # Aumentando o tamanho do campo
    is_admin = db.Column(db.Boolean, default=False)

    bookings = db.relationship('Booking', backref='user', lazy=True)
    packages = db.relationship('Package', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    addresses = db.relationship('Address', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric)
    image_url = db.Column(db.String(200))

    # Modificando para usar cascade delete nas relações
    bookings = db.relationship('Booking', backref='service', lazy=True, 
                               cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='service', lazy=True)
    package_items = db.relationship('PackageItem', backref='service', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False, index=True)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=True, index=True)
    event_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='Pendente')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Campos para pagamento (mantidos para futura integração)
    payment_status = db.Column(db.String(50), default='Pendente', index=True)
    payment_date = db.Column(db.DateTime, nullable=True)
    payment_method = db.Column(db.String(50), nullable=True)
    payment_id = db.Column(db.String(100), nullable=True)
    total_amount = db.Column(db.Numeric(10, 2), nullable=True)

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    name = db.Column(db.String(100))
    total_price = db.Column(db.Numeric)
    items = db.relationship('PackageItem', backref='package', lazy=True)
    bookings = db.relationship('Booking', backref='package', lazy=True)
    descricao = db.Column(db.String(1000))

class PackageItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    city = db.Column(db.String(100))
    neighborhood = db.Column(db.String(100))
    street = db.Column(db.String(100))
    number = db.Column(db.String(20))
    postal_code = db.Column(db.String(20))
