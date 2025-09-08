#!/usr/bin/env python3
"""
Script to create sample mobile home data for testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, MobileHome, Property, User
from datetime import datetime, date

def create_sample_data():
    """Create sample mobile homes and properties for testing"""
    app, socketio = create_app()
    
    with app.app_context():
        print("Creating sample data...")
        
        # Create a sample user if none exists
        if not User.query.first():
            from flask_bcrypt import Bcrypt
            bcrypt = Bcrypt()
            admin_user = User(
                email='admin@example.com',
                password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8'),
                role='admin',
                first_name='Admin',
                last_name='User'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Created admin user: admin@example.com / admin123")
        
        # Create sample properties if none exist
        if not Property.query.first():
            sample_properties = [
                Property(
                    address='123 Mobile Home Park Dr, Sacramento, CA 95818',
                    property_type='Mobile Home Park',
                    num_units=50,
                    owner_id=1
                ),
                Property(
                    address='456 Sunrise MHP Blvd, Phoenix, AZ 85001',
                    property_type='Mobile Home Park',
                    num_units=75,
                    owner_id=1
                ),
                Property(
                    address='789 Desert View MHP, Las Vegas, NV 89101',
                    property_type='Mobile Home Park',
                    num_units=100,
                    owner_id=1
                )
            ]
            
            for prop in sample_properties:
                db.session.add(prop)
            db.session.commit()
            print(f"Created {len(sample_properties)} sample properties")
        
        # Create sample mobile homes
        sample_homes = [
            {
                'vin_number': '1ABCD1234567890123',
                'make': 'Clayton',
                'model': 'Double Wide',
                'year': 2018,
                'serial_number': 'CLY123456',
                'width': 28.0,
                'length': 56.0,
                'property_id': 1,
                'current_owner_name': 'John Smith',
                'current_owner_address': '123 Mobile Home Park Dr, Space 15, Sacramento, CA 95818',
                'current_owner_phone': '(916) 555-0123',
                'title_status': 'missing',
                'acquisition_date': date(2023, 6, 15),
                'acquisition_method': 'abandonment',
                'park_location_space': 'Space 15',
                'purchase_price': 45000.00,
                'current_value': 42000.00,
                'recovery_status': 'pending'
            },
            {
                'vin_number': '2EFGH2345678901234',
                'make': 'Fleetwood',
                'model': 'Single Wide',
                'year': 2020,
                'serial_number': 'FLT789012',
                'width': 16.0,
                'length': 80.0,
                'property_id': 1,
                'current_owner_name': 'Jane Doe',
                'current_owner_address': '123 Mobile Home Park Dr, Space 23, Sacramento, CA 95818',
                'current_owner_phone': '(916) 555-0456',
                'previous_owner_name': 'Bob Johnson',
                'title_status': 'lost',
                'lien_holder': 'ABC Finance',
                'lien_amount': 15000.00,
                'acquisition_date': date(2023, 8, 1),
                'acquisition_method': 'purchase',
                'park_location_space': 'Space 23',
                'purchase_price': 35000.00,
                'current_value': 38000.00,
                'recovery_status': 'in_progress'
            },
            {
                'vin_number': '3IJKL3456789012345',
                'make': 'Champion',
                'model': 'Triple Wide',
                'year': 2019,
                'serial_number': 'CHP345678',
                'width': 42.0,
                'length': 60.0,
                'property_id': 2,
                'current_owner_name': 'Mike Wilson',
                'current_owner_address': '456 Sunrise MHP Blvd, Space 8, Phoenix, AZ 85001',
                'current_owner_phone': '(602) 555-0789',
                'title_status': 'abandoned',
                'acquisition_date': date(2023, 4, 20),
                'acquisition_method': 'abandonment',
                'park_location_space': 'Space 8',
                'purchase_price': 65000.00,
                'current_value': 58000.00,
                'condition_notes': 'Needs roof repair and interior cleaning',
                'recovery_status': 'pending'
            },
            {
                'vin_number': '4MNOP4567890123456',
                'make': 'Skyline',
                'model': 'Double Wide Deluxe',
                'year': 2021,
                'serial_number': 'SKY901234',
                'width': 32.0,
                'length': 64.0,
                'property_id': 3,
                'current_owner_name': 'Sarah Davis',
                'current_owner_address': '789 Desert View MHP, Space 42, Las Vegas, NV 89101',
                'current_owner_phone': '(702) 555-0321',
                'title_status': 'clear',
                'acquisition_date': date(2023, 9, 10),
                'acquisition_method': 'purchase',
                'park_location_space': 'Space 42',
                'purchase_price': 55000.00,
                'current_value': 60000.00,
                'recovery_status': 'completed'
            }
        ]
        
        for home_data in sample_homes:
            # Check if mobile home already exists
            existing = MobileHome.query.filter_by(vin_number=home_data['vin_number']).first()
            if not existing:
                mobile_home = MobileHome(**home_data)
                db.session.add(mobile_home)
        
        db.session.commit()
        
        total_homes = MobileHome.query.count()
        print(f"Sample data created successfully! Total mobile homes: {total_homes}")

if __name__ == '__main__':
    create_sample_data()