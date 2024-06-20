from datetime import datetime
from EcoApp import db, login_manager
from flask_login import UserMixin
from EcoApp import app,db

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    district = db.Column(db.String(20), nullable=False)
    sector = db.Column(db.String(20), nullable=False)
    village = db.Column(db.String(20), nullable=False)
    street = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(200), nullable=False)  # Increased length for hashed password
    cell = db.Column(db.String(20), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        return f"{self.id}, {self.email}, {self.first_name}, {self.last_name}"

class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    order_services = db.relationship('OrderServices', backref='service', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    scheduled_date = db.Column(db.Date, nullable=False)  # New column for scheduled date
    status = db.Column(db.String(20), nullable=False, default='Pending')  # Default status to 'Pending'
    order_services = db.relationship('OrderServices', backref='order', lazy=True)

class OrderServices(db.Model):  # New table for many-to-many relationship
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)


