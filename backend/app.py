from datetime import timedelta
from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from flask_cors import CORS
from flask_socketio import SocketIO
import os
import openai

from .models import db, User
from .routes.property import bp as property_bp
from .routes.tenant import bp as tenant_bp
from .routes.lease import bp as lease_bp
from .routes.payment import bp as payment_bp
from .routes.maintenance import bp as maintenance_bp
from .utils import role_required


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///property.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'change-this-secret')
    openai.api_key = os.getenv('OPENAI_API_KEY')

    CORS(app)
    db.init_app(app)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    socketio = SocketIO(app, cors_allowed_origins="*")

    # -------------------- Routes -------------------- #
    @app.post('/api/signup')
    def signup():
        data = request.json
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'User already exists'}), 400
        hashed = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(email=data['email'], password_hash=hashed, role=data.get('role', 'tenant'))
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created'}), 201

    @app.post('/api/login')
    def login():
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password_hash, data['password']):
            token = create_access_token(identity={'id': user.user_id, 'role': user.role}, expires_delta=timedelta(hours=1))
            return jsonify({'token': token})
        return jsonify({'message': 'Invalid credentials'}), 401

    @app.get('/api/user')
    @jwt_required()
    def get_user():
        current = get_jwt_identity()
        user = User.query.get(current['id'])
        return jsonify({'email': user.email, 'role': user.role})

    @app.post('/api/gpt')
    @jwt_required()
    def gpt_endpoint():
        question = request.json.get('question', '')
        try:
            completion = openai.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[{'role': 'user', 'content': question}]
            )
            answer = completion.choices[0].message.content
            return jsonify({'answer': answer})
        except Exception as exc:
            return jsonify({'error': str(exc)}), 500

    # Register blueprints
    app.register_blueprint(property_bp)
    app.register_blueprint(tenant_bp)
    app.register_blueprint(lease_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(maintenance_bp)

    @app.before_first_request
    def create_tables():
        db.create_all()

    # example socket event for notifications
    @socketio.on('connect')
    def handle_connect():
        pass

    return app, socketio


if __name__ == '__main__':
    app, socketio = create_app()
    socketio.run(app, debug=True)
