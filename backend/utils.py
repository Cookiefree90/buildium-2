from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify


def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorated(*args, **kwargs):
            current = get_jwt_identity()
            if current['role'] not in roles:
                return jsonify({'message': 'Forbidden'}), 403
            return fn(*args, **kwargs)
        return decorated
    return wrapper
