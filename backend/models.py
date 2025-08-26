from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), default='tenant')
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Property(db.Model):
    __tablename__ = 'properties'
    property_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200))
    property_type = db.Column(db.String(50))
    num_units = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Tenant(db.Model):
    __tablename__ = 'tenants'
    tenant_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120))
    phone_number = db.Column(db.String(20))
    move_in_date = db.Column(db.Date)
    move_out_date = db.Column(db.Date)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.property_id'))
    lease_id = db.Column(db.Integer, db.ForeignKey('leases.lease_id'))

class Lease(db.Model):
    __tablename__ = 'leases'
    lease_id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.tenant_id'))
    property_id = db.Column(db.Integer, db.ForeignKey('properties.property_id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    rent_amount = db.Column(db.Float)
    payment_frequency = db.Column(db.String(20))
    deposit = db.Column(db.Float)
    status = db.Column(db.String(20))

class Payment(db.Model):
    __tablename__ = 'payments'
    payment_id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.tenant_id'))
    lease_id = db.Column(db.Integer, db.ForeignKey('leases.lease_id'))
    payment_date = db.Column(db.Date)
    amount = db.Column(db.Float)
    payment_status = db.Column(db.String(20))
    payment_method = db.Column(db.String(50))

class MaintenanceRequest(db.Model):
    __tablename__ = 'maintenance_requests'
    request_id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.tenant_id'))
    property_id = db.Column(db.Integer, db.ForeignKey('properties.property_id'))
    description = db.Column(db.String(200))
    status = db.Column(db.String(20))
    priority = db.Column(db.String(20))
    assigned_to = db.Column(db.String(100))
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    completed_date = db.Column(db.DateTime)

class CommunicationLog(db.Model):
    __tablename__ = 'communication_logs'
    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.tenant_id'))
    message = db.Column(db.Text)
    message_type = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
