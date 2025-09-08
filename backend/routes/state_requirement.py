from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import json
try:
    from ..models import db, StateRequirement
    from ..utils import role_required
except ImportError:
    from models import db, StateRequirement
    from utils import role_required

bp = Blueprint('state_requirements', __name__, url_prefix='/api/state-requirements')

@bp.get('/')
@jwt_required()
def list_state_requirements():
    """List all state requirements"""
    states = StateRequirement.query.all()
    return jsonify([
        {
            'id': state.requirement_id,
            'state_code': state.state_code,
            'state_name': state.state_name,
            'agency_name': state.agency_name,
            'processing_time': state.processing_time,
            'website_url': state.website_url
        }
        for state in states
    ])

@bp.get('/<state_code>')
@jwt_required()
def get_state_requirement(state_code):
    """Get state requirements by state code"""
    state = StateRequirement.query.filter_by(state_code=state_code.upper()).first_or_404()
    return jsonify({
        'id': state.requirement_id,
        'state_code': state.state_code,
        'state_name': state.state_name,
        'agency_name': state.agency_name,
        'required_documents': json.loads(state.required_documents) if state.required_documents else [],
        'fees': json.loads(state.fees) if state.fees else {},
        'processing_time': state.processing_time,
        'contact_info': json.loads(state.contact_info) if state.contact_info else {},
        'special_requirements': state.special_requirements,
        'website_url': state.website_url
    })

@bp.post('/')
@role_required('admin')
def create_state_requirement():
    """Create or update state requirements (admin only)"""
    data = request.json
    
    # Check if state already exists
    existing = StateRequirement.query.filter_by(state_code=data['state_code'].upper()).first()
    
    if existing:
        # Update existing
        existing.state_name = data.get('state_name', existing.state_name)
        existing.agency_name = data.get('agency_name', existing.agency_name)
        existing.required_documents = json.dumps(data.get('required_documents', []))
        existing.fees = json.dumps(data.get('fees', {}))
        existing.processing_time = data.get('processing_time', existing.processing_time)
        existing.contact_info = json.dumps(data.get('contact_info', {}))
        existing.special_requirements = data.get('special_requirements', existing.special_requirements)
        existing.website_url = data.get('website_url', existing.website_url)
        db.session.commit()
        return jsonify({'id': existing.requirement_id, 'message': 'State requirement updated'})
    else:
        # Create new
        state_req = StateRequirement(
            state_code=data['state_code'].upper(),
            state_name=data['state_name'],
            agency_name=data.get('agency_name'),
            required_documents=json.dumps(data.get('required_documents', [])),
            fees=json.dumps(data.get('fees', {})),
            processing_time=data.get('processing_time'),
            contact_info=json.dumps(data.get('contact_info', {})),
            special_requirements=data.get('special_requirements'),
            website_url=data.get('website_url')
        )
        db.session.add(state_req)
        db.session.commit()
        return jsonify({'id': state_req.requirement_id, 'message': 'State requirement created'}), 201