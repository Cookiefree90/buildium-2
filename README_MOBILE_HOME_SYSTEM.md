# Mobile Home Park VIN/Title Recovery System

## Overview

This system provides comprehensive Excel sheet generation for mobile home park VIN/title recovery processes across all 50 United States. It's designed to be sold to park owners and MHP (Mobile Home Park) investors as a professional tool for managing title recovery documentation.

## Features

### ✅ Complete State Coverage
- **26+ States Implemented** with detailed requirements
- State-specific agency information and contact details
- Required documents and fee structures
- Processing times and special requirements
- Official website references

### ✅ Professional Excel Generation
- **State-specific Excel sheets** with professional formatting
- Comprehensive mobile home data tracking
- Required documents checklist by state
- Fee breakdown and contact information
- Multi-state workbook generation capability

### ✅ Comprehensive Mobile Home Management
- VIN number tracking and validation
- Owner information management (current and previous)
- Title status tracking (missing, lost, abandoned, clear)
- Recovery status monitoring (pending, in_progress, completed, failed)
- Lien information and amounts
- Property association and space tracking

### ✅ Business-Ready API
- RESTful API design with proper authentication
- Role-based access control (admin, manager, tenant)
- CRUD operations for all entities
- Excel export endpoints for different use cases

## API Endpoints

### Mobile Home Management
- `GET /api/mobile-homes` - List all mobile homes
- `POST /api/mobile-homes` - Create new mobile home record
- `GET /api/mobile-homes/{id}` - Get specific mobile home details
- `PUT /api/mobile-homes/{id}` - Update mobile home record
- `DELETE /api/mobile-homes/{id}` - Delete mobile home record

### State Requirements
- `GET /api/state-requirements` - List all state requirements
- `GET /api/state-requirements/{state_code}` - Get specific state requirements
- `POST /api/state-requirements` - Create/update state requirements (admin only)

### Excel Export
- `GET /api/excel/states/{state_code}` - Generate state-specific Excel sheet
- `GET /api/excel/all-states` - Generate comprehensive multi-state workbook
- `GET /api/excel/property/{property_id}` - Generate property-specific Excel sheet

## Frontend Interface

### Mobile Home VIN Recovery Dashboard
- **Mobile Home Listing**: View all mobile homes with status indicators
- **Add/Edit Forms**: Comprehensive forms for mobile home data entry
- **State Selection**: Choose from available states for Excel generation
- **Excel Download**: One-click download of formatted Excel sheets
- **Status Tracking**: Visual indicators for title and recovery status

## Database Schema

### StateRequirement
- State code, name, and agency information
- Required documents (JSON array)
- Fees breakdown (JSON object)
- Processing times and contact information
- Special state-specific requirements

### MobileHome
- VIN number (unique identifier)
- Make, model, year, dimensions
- Current and previous owner information
- Title status and lien information
- Acquisition details and recovery status
- Property association and location

### RecoveryDocument
- Document type and file management
- Associated mobile home tracking
- Upload dates and notes

## Business Model

### Target Market
- **Mobile Home Park Owners**: Manage title recovery for abandoned units
- **MHP Investors**: Due diligence and asset recovery tools
- **Property Management Companies**: Streamline recovery processes
- **Legal Professionals**: Standardized documentation for title recovery

### Revenue Streams
- **Per-State License**: Individual state Excel templates
- **Complete Package**: All 50 states bundle
- **Property-Specific Reports**: Custom property analysis
- **Subscription Model**: Ongoing updates and support

## Installation & Setup

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python populate_states.py  # Load state requirements
python create_sample_data.py  # Create sample data
python app.py  # Start server
```

### Frontend Setup
```bash
cd frontend
npm install
npm start  # Development server
npm run build  # Production build
```

### Default Admin User
- **Email**: admin@example.com
- **Password**: admin123
- **Role**: admin

## Excel Output Features

### Professional Formatting
- Branded headers with state information
- Color-coded status indicators
- Proper column sizing and borders
- Money formatting for financial fields
- Date formatting for date fields

### State-Specific Content
- Agency contact information
- Required documents checklist
- Fee breakdown by type
- Processing time estimates
- Special requirements and notes

### Multi-Export Options
- **Single State**: Focus on specific state requirements
- **All States**: Comprehensive workbook with all states
- **Property Specific**: Filter by property for targeted reports

## Sample States Included

✅ **Alabama** - Alabama Department of Revenue - Motor Vehicle Division  
✅ **Alaska** - Alaska Division of Motor Vehicles  
✅ **Arizona** - Arizona Department of Transportation - Motor Vehicle Division  
✅ **Arkansas** - Arkansas Office of Motor Vehicle  
✅ **California** - California Department of Housing and Community Development  
✅ **Colorado** - Colorado Department of Revenue - Motor Vehicle  
✅ **Connecticut** - Connecticut Department of Motor Vehicles  
✅ **Delaware** - Delaware Division of Motor Vehicles  
✅ **Florida** - Florida Department of Highway Safety and Motor Vehicles  
✅ **Georgia** - Georgia Department of Revenue - Motor Vehicle Division  
*...and 16+ more states with detailed requirements*

## Sample Mobile Home Data

The system includes realistic sample data:
- **4 Sample Mobile Homes** across different properties
- Various title statuses (missing, lost, abandoned, clear)
- Different recovery stages (pending, in_progress, completed)
- Realistic VIN numbers, owner information, and financial data

## Professional Use Cases

### Scenario 1: Park Owner with Abandoned Unit
1. Enter mobile home details and owner information
2. Select appropriate state (e.g., California)
3. Generate Excel sheet with CA-specific requirements
4. Follow state agency guidelines for title recovery
5. Track progress through recovery status updates

### Scenario 2: MHP Investor Due Diligence
1. Load property information and mobile home inventory
2. Generate comprehensive Excel report for target state
3. Review required documentation and fees
4. Assess recovery costs and timeline
5. Make informed investment decisions

### Scenario 3: Multi-State Portfolio Management
1. Manage mobile homes across multiple states
2. Generate state-specific reports as needed
3. Track recovery status across entire portfolio
4. Maintain organized documentation for legal compliance

## Technology Stack

- **Backend**: Flask, SQLAlchemy, JWT Authentication, OpenPyXL
- **Frontend**: React, Axios, React Router
- **Database**: SQLite (development), easily upgradeable to PostgreSQL
- **Excel Generation**: OpenPyXL with professional styling
- **Authentication**: JWT with role-based access control

## Next Steps for Production

1. **Complete All 50 States**: Add remaining 24 states with full requirements
2. **Enhanced Excel Features**: Add charts, conditional formatting, macros
3. **Document Upload**: Support for uploading recovery documents
4. **Email Integration**: Automated notifications and reminders
5. **Payment Integration**: Stripe/PayPal for selling Excel templates
6. **Multi-tenant Support**: Separate data for different customers
7. **Advanced Reporting**: Analytics and dashboard features

This system provides a solid foundation for a profitable SaaS business targeting the mobile home park industry with professional tools for title recovery and asset management.