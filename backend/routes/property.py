from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models import db, Property
from ..utils import role_required

bp = Blueprint('properties', __name__, url_prefix='/api/properties')

@bp.post('/')
@role_required('admin', 'manager')
def create_property():
    data = request.json
    prop = Property(
        address=data.get('address'),
        property_type=data.get('property_type'),
        num_units=data.get('num_units'),
        owner_id=data.get('owner_id')
    )
    db.session.add(prop)
    db.session.commit()
    return jsonify({'id': prop.property_id}), 201

@bp.get('/')
@jwt_required()
def list_properties():
    props = Property.query.all()
    return jsonify([
        {'id': p.property_id, 'address': p.address, 'type': p.property_type}
        for p in props
    ])
