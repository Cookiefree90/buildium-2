from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models import db, Tenant
from ..utils import role_required

bp = Blueprint('tenants', __name__, url_prefix='/api/tenants')

@bp.post('/')
@role_required('admin', 'manager')
def create_tenant():
    data = request.json
    tenant = Tenant(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        phone_number=data.get('phone_number'),
        property_id=data.get('property_id')
    )
    db.session.add(tenant)
    db.session.commit()
    return jsonify({'id': tenant.tenant_id}), 201

@bp.get('/')
@jwt_required()
def list_tenants():
    tenants = Tenant.query.all()
    return jsonify([
        {'id': t.tenant_id, 'name': f"{t.first_name} {t.last_name}"}
        for t in tenants
    ])
