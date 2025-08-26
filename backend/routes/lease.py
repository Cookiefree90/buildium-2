from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models import db, Lease
from ..utils import role_required

bp = Blueprint('leases', __name__, url_prefix='/api/leases')

@bp.post('/')
@role_required('admin', 'manager')
def create_lease():
    data = request.json
    lease = Lease(
        tenant_id=data.get('tenant_id'),
        property_id=data.get('property_id'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        rent_amount=data.get('rent_amount'),
        payment_frequency=data.get('payment_frequency'),
        deposit=data.get('deposit'),
        status=data.get('status')
    )
    db.session.add(lease)
    db.session.commit()
    return jsonify({'id': lease.lease_id}), 201

@bp.get('/')
@jwt_required()
def list_leases():
    leases = Lease.query.all()
    return jsonify([
        {'id': l.lease_id, 'tenant_id': l.tenant_id, 'rent': l.rent_amount}
        for l in leases
    ])
