from datetime import datetime
from EcoApp import db,login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Company(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(40), nullable=False, unique=True)
    company_ceo = db.Column(db.String(40), nullable=False)
    orders = db.relationship('Order', backref='company', lazy=True)

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
    orders = db.relationship('Order', backref='user', lazy=True)


class Services(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    orders = db.relationship('Order', backref='service', lazy=True)

class Order(db.Model):  # Changed from 'orders' to 'Order' to follow naming conventions
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False)
