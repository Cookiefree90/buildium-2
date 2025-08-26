from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models import db, Payment
from ..utils import role_required

bp = Blueprint('payments', __name__, url_prefix='/api/payments')

@bp.post('/')
@role_required('admin', 'manager')
def create_payment():
    data = request.json
    payment = Payment(
        tenant_id=data.get('tenant_id'),
        lease_id=data.get('lease_id'),
        payment_date=data.get('payment_date'),
        amount=data.get('amount'),
        payment_status=data.get('payment_status'),
        payment_method=data.get('payment_method')
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify({'id': payment.payment_id}), 201

@bp.get('/')
@jwt_required()
def list_payments():
    payments = Payment.query.all()
    return jsonify([
        {'id': p.payment_id, 'amount': p.amount, 'status': p.payment_status}
        for p in payments
    ])
