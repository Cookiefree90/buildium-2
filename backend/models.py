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

class StateRequirement(db.Model):
    __tablename__ = 'state_requirements'
    requirement_id = db.Column(db.Integer, primary_key=True)
    state_code = db.Column(db.String(2), nullable=False)  # AL, AK, AZ, etc.
    state_name = db.Column(db.String(100), nullable=False)
    agency_name = db.Column(db.String(200))  # DMV, DOT, etc.
    required_documents = db.Column(db.Text)  # JSON array of required documents
    fees = db.Column(db.Text)  # JSON object with fee information
    processing_time = db.Column(db.String(100))
    contact_info = db.Column(db.Text)  # JSON object with contact details
    special_requirements = db.Column(db.Text)  # State-specific notes
    website_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MobileHome(db.Model):
    __tablename__ = 'mobile_homes'
    mobile_home_id = db.Column(db.Integer, primary_key=True)
    vin_number = db.Column(db.String(17), unique=True, nullable=False)
    serial_number = db.Column(db.String(50))
    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    year = db.Column(db.Integer)
    width = db.Column(db.Float)  # Width in feet
    length = db.Column(db.Float)  # Length in feet
    property_id = db.Column(db.Integer, db.ForeignKey('properties.property_id'))
    current_owner_name = db.Column(db.String(200))
    current_owner_address = db.Column(db.Text)
    current_owner_phone = db.Column(db.String(20))
    previous_owner_name = db.Column(db.String(200))
    previous_owner_address = db.Column(db.Text)
    title_status = db.Column(db.String(50))  # 'missing', 'lost', 'abandoned', 'clear'
    lien_holder = db.Column(db.String(200))
    lien_amount = db.Column(db.Float)
    acquisition_date = db.Column(db.Date)
    acquisition_method = db.Column(db.String(50))  # 'abandonment', 'purchase', 'inheritance'
    park_location_space = db.Column(db.String(50))
    manufactured_date = db.Column(db.Date)
    purchase_price = db.Column(db.Float)
    current_value = db.Column(db.Float)
    condition_notes = db.Column(db.Text)
    recovery_status = db.Column(db.String(50), default='pending')  # 'pending', 'in_progress', 'completed', 'failed'
    recovery_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RecoveryDocument(db.Model):
    __tablename__ = 'recovery_documents'
    document_id = db.Column(db.Integer, primary_key=True)
    mobile_home_id = db.Column(db.Integer, db.ForeignKey('mobile_homes.mobile_home_id'))
    document_type = db.Column(db.String(100))  # 'bill_of_sale', 'affidavit', 'lien_release', etc.
    document_name = db.Column(db.String(200))
    file_path = db.Column(db.String(500))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
