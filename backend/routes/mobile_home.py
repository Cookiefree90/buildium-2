from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import json
try:
    from ..models import db, MobileHome, StateRequirement, RecoveryDocument
    from ..utils import role_required
except ImportError:
    from models import db, MobileHome, StateRequirement, RecoveryDocument
    from utils import role_required

bp = Blueprint('mobile_homes', __name__, url_prefix='/api/mobile-homes')

@bp.post('/')
@role_required('admin', 'manager')
def create_mobile_home():
    """Create a new mobile home record"""
    data = request.json
    mobile_home = MobileHome(
        vin_number=data.get('vin_number'),
        serial_number=data.get('serial_number'),
        make=data.get('make'),
        model=data.get('model'),
        year=data.get('year'),
        width=data.get('width'),
        length=data.get('length'),
        property_id=data.get('property_id'),
        current_owner_name=data.get('current_owner_name'),
        current_owner_address=data.get('current_owner_address'),
        current_owner_phone=data.get('current_owner_phone'),
        previous_owner_name=data.get('previous_owner_name'),
        previous_owner_address=data.get('previous_owner_address'),
        title_status=data.get('title_status', 'missing'),
        lien_holder=data.get('lien_holder'),
        lien_amount=data.get('lien_amount'),
        acquisition_date=datetime.strptime(data.get('acquisition_date'), '%Y-%m-%d').date() if data.get('acquisition_date') else None,
        acquisition_method=data.get('acquisition_method'),
        park_location_space=data.get('park_location_space'),
        manufactured_date=datetime.strptime(data.get('manufactured_date'), '%Y-%m-%d').date() if data.get('manufactured_date') else None,
        purchase_price=data.get('purchase_price'),
        current_value=data.get('current_value'),
        condition_notes=data.get('condition_notes'),
        recovery_status=data.get('recovery_status', 'pending'),
        recovery_notes=data.get('recovery_notes')
    )
    db.session.add(mobile_home)
    db.session.commit()
    return jsonify({'id': mobile_home.mobile_home_id}), 201

@bp.get('/')
@jwt_required()
def list_mobile_homes():
    """List all mobile homes"""
    mobile_homes = MobileHome.query.all()
    return jsonify([
        {
            'id': mh.mobile_home_id,
            'vin_number': mh.vin_number,
            'make': mh.make,
            'model': mh.model,
            'year': mh.year,
            'title_status': mh.title_status,
            'recovery_status': mh.recovery_status,
            'property_id': mh.property_id
        }
        for mh in mobile_homes
    ])

@bp.get('/<int:mobile_home_id>')
@jwt_required()
def get_mobile_home(mobile_home_id):
    """Get a specific mobile home by ID"""
    mobile_home = MobileHome.query.get_or_404(mobile_home_id)
    return jsonify({
        'id': mobile_home.mobile_home_id,
        'vin_number': mobile_home.vin_number,
        'serial_number': mobile_home.serial_number,
        'make': mobile_home.make,
        'model': mobile_home.model,
        'year': mobile_home.year,
        'width': mobile_home.width,
        'length': mobile_home.length,
        'property_id': mobile_home.property_id,
        'current_owner_name': mobile_home.current_owner_name,
        'current_owner_address': mobile_home.current_owner_address,
        'current_owner_phone': mobile_home.current_owner_phone,
        'previous_owner_name': mobile_home.previous_owner_name,
        'previous_owner_address': mobile_home.previous_owner_address,
        'title_status': mobile_home.title_status,
        'lien_holder': mobile_home.lien_holder,
        'lien_amount': mobile_home.lien_amount,
        'acquisition_date': mobile_home.acquisition_date.isoformat() if mobile_home.acquisition_date else None,
        'acquisition_method': mobile_home.acquisition_method,
        'park_location_space': mobile_home.park_location_space,
        'manufactured_date': mobile_home.manufactured_date.isoformat() if mobile_home.manufactured_date else None,
        'purchase_price': mobile_home.purchase_price,
        'current_value': mobile_home.current_value,
        'condition_notes': mobile_home.condition_notes,
        'recovery_status': mobile_home.recovery_status,
        'recovery_notes': mobile_home.recovery_notes,
        'created_at': mobile_home.created_at.isoformat(),
        'updated_at': mobile_home.updated_at.isoformat()
    })

@bp.put('/<int:mobile_home_id>')
@role_required('admin', 'manager')
def update_mobile_home(mobile_home_id):
    """Update a mobile home record"""
    mobile_home = MobileHome.query.get_or_404(mobile_home_id)
    data = request.json
    
    # Update fields if provided
    for field in ['vin_number', 'serial_number', 'make', 'model', 'year', 'width', 'length',
                  'current_owner_name', 'current_owner_address', 'current_owner_phone',
                  'previous_owner_name', 'previous_owner_address', 'title_status',
                  'lien_holder', 'lien_amount', 'acquisition_method', 'park_location_space',
                  'purchase_price', 'current_value', 'condition_notes', 'recovery_status',
                  'recovery_notes']:
        if field in data:
            setattr(mobile_home, field, data[field])
    
    # Handle date fields
    if 'acquisition_date' in data and data['acquisition_date']:
        mobile_home.acquisition_date = datetime.strptime(data['acquisition_date'], '%Y-%m-%d').date()
    if 'manufactured_date' in data and data['manufactured_date']:
        mobile_home.manufactured_date = datetime.strptime(data['manufactured_date'], '%Y-%m-%d').date()
    
    mobile_home.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Mobile home updated successfully'})

@bp.delete('/<int:mobile_home_id>')
@role_required('admin', 'manager')
def delete_mobile_home(mobile_home_id):
    """Delete a mobile home record"""
    mobile_home = MobileHome.query.get_or_404(mobile_home_id)
    db.session.delete(mobile_home)
    db.session.commit()
    return jsonify({'message': 'Mobile home deleted successfully'})