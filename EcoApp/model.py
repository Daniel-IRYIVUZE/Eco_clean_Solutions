from datetime import datetime
from EcoApp import db


class Company(db.Model):
    comId = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(20), nullable=False, unique=True)
    company_ceo = db.Column(db.String(20), nullable=False)
    orders = db.relationship('Order', backref='company', lazy=True)

class Users(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    district = db.Column(db.String(20), nullable=False)
    sector = db.Column(db.String(20), nullable=False)
    village = db.Column(db.String(20), nullable=False)
    street = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(20), nullable=False)
    cell = db.Column(db.String(20), nullable=False)  # Changed to string to accommodate phone numbers
    orders = db.relationship('Order', backref='user', lazy=True)

class Services(db.Model):
    sevId = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(40), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    orders = db.relationship('Order', backref='service', lazy=True)

class Order(db.Model):  # Changed from 'orders' to 'Order' to follow naming conventions
    ordId = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.comId'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.sevId'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False)
