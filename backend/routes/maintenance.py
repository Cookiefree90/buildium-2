from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
try:
    from ..models import db, MaintenanceRequest
    from ..utils import role_required
except ImportError:
    from models import db, MaintenanceRequest
    from utils import role_required

bp = Blueprint('maintenance', __name__, url_prefix='/api/maintenance')

@bp.post('/')
@jwt_required()
def create_request():
    data = request.json
    req = MaintenanceRequest(
        tenant_id=data.get('tenant_id'),
        property_id=data.get('property_id'),
        description=data.get('description'),
        status=data.get('status', 'open'),
        priority=data.get('priority'),
        assigned_to=data.get('assigned_to')
    )
    db.session.add(req)
    db.session.commit()
    socketio = current_app.extensions['socketio']
    socketio.emit('maintenance_update', {'id': req.request_id, 'status': req.status})
    return jsonify({'id': req.request_id}), 201

@bp.get('/')
@role_required('admin', 'manager')
def list_requests():
    requests = MaintenanceRequest.query.all()
    return jsonify([
        {'id': r.request_id, 'status': r.status, 'priority': r.priority}
        for r in requests
    ])
