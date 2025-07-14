import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.config import config
from src.models.user import db
from src.models.education import *
from src.models.healthcare import *
from src.models.agriculture import *
from src.models.business import *
from src.models.community import *

# Import all route blueprints
from src.routes.auth import auth_bp
from src.routes.user import user_bp
from src.routes.education import education_bp
from src.routes.healthcare import healthcare_bp
from src.routes.agriculture import agriculture_bp
from src.routes.business import business_bp
from src.routes.community import community_bp
from src.routes.projects import projects_bp
from src.routes.advanced import advanced_bp

def create_app(config_name='default'):
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Configure CORS
    CORS(app, origins=app.config.get('CORS_ORIGINS', ['*']))
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(education_bp, url_prefix='/api/education')
    app.register_blueprint(healthcare_bp, url_prefix='/api/healthcare')
    app.register_blueprint(agriculture_bp, url_prefix='/api/agriculture')
    app.register_blueprint(business_bp, url_prefix='/api/business')
    app.register_blueprint(community_bp, url_prefix='/api/community')
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    app.register_blueprint(advanced_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default roles and permissions if they don't exist
        create_default_data()
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Invalid token'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Authorization token is required'}), 401
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'ONGON BANGLADESH API is running',
            'version': '1.0.0'
        })
    
    # API info endpoint
    @app.route('/api')
    def api_info():
        return jsonify({
            'name': 'ONGON BANGLADESH API',
            'version': '1.0.0',
            'description': 'Comprehensive platform for social welfare, education, healthcare, and agriculture',
            'endpoints': {
                'auth': '/api/auth',
                'users': '/api/users',
                'education': '/api/education',
                'healthcare': '/api/healthcare',
                'agriculture': '/api/agriculture',
                'business': '/api/business',
                'community': '/api/community',
                'projects': '/api/projects'
            }
        })
    
    # Serve frontend static files
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
            return jsonify({'error': 'Static folder not configured'}), 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                # If no frontend is built, return API info
                return jsonify({
                    'message': 'ONGON BANGLADESH API Server',
                    'status': 'running',
                    'api_docs': '/api'
                })
    
    return app

def create_default_data():
    """Create default roles, permissions, and other initial data"""
    from src.models.user import Role, Permission, role_permissions
    
    # Default roles
    default_roles = [
        {'name': 'admin', 'description': 'System Administrator'},
        {'name': 'donor', 'description': 'Donation Provider'},
        {'name': 'volunteer', 'description': 'Volunteer Worker'},
        {'name': 'beneficiary', 'description': 'Service Beneficiary'},
        {'name': 'healthcare_provider', 'description': 'Healthcare Professional'},
        {'name': 'educator', 'description': 'Education Provider'},
        {'name': 'farmer', 'description': 'Agricultural Producer'},
        {'name': 'business_owner', 'description': 'Business Entity'},
        {'name': 'organization', 'description': 'Non-profit Organization'}
    ]
    
    # Default permissions
    default_permissions = [
        {'name': 'user_management', 'description': 'Manage users and roles', 'module': 'admin'},
        {'name': 'course_management', 'description': 'Manage courses and content', 'module': 'education'},
        {'name': 'patient_management', 'description': 'Manage patient records', 'module': 'healthcare'},
        {'name': 'farm_management', 'description': 'Manage farm operations', 'module': 'agriculture'},
        {'name': 'loan_management', 'description': 'Manage microfinance operations', 'module': 'finance'},
        {'name': 'project_management', 'description': 'Manage projects and campaigns', 'module': 'projects'},
        {'name': 'event_management', 'description': 'Manage events and activities', 'module': 'events'},
        {'name': 'report_access', 'description': 'Access reports and analytics', 'module': 'reports'}
    ]
    
    # Create roles
    for role_data in default_roles:
        if not Role.query.filter_by(name=role_data['name']).first():
            role = Role(**role_data)
            db.session.add(role)
    
    # Create permissions
    for perm_data in default_permissions:
        if not Permission.query.filter_by(name=perm_data['name']).first():
            permission = Permission(**perm_data)
            db.session.add(permission)
    
    db.session.commit()
    
    # Assign permissions to admin role
    admin_role = Role.query.filter_by(name='admin').first()
    if admin_role:
        all_permissions = Permission.query.all()
        for permission in all_permissions:
            if permission not in admin_role.permissions:
                admin_role.permissions.append(permission)
    
    # Default course categories
    from src.models.education import CourseCategory
    default_categories = [
        {'name': 'Technology', 'description': 'Computer and technology courses'},
        {'name': 'Business', 'description': 'Business and entrepreneurship'},
        {'name': 'Agriculture', 'description': 'Farming and agricultural techniques'},
        {'name': 'Healthcare', 'description': 'Health and medical education'},
        {'name': 'Life Skills', 'description': 'Personal development and life skills'}
    ]
    
    for cat_data in default_categories:
        if not CourseCategory.query.filter_by(name=cat_data['name']).first():
            category = CourseCategory(**cat_data)
            db.session.add(category)
    
    # Default job categories
    from src.models.business import JobCategory
    default_job_categories = [
        {'name': 'Technology', 'description': 'IT and software jobs'},
        {'name': 'Agriculture', 'description': 'Farming and agricultural jobs'},
        {'name': 'Healthcare', 'description': 'Medical and healthcare jobs'},
        {'name': 'Education', 'description': 'Teaching and training jobs'},
        {'name': 'Business', 'description': 'Business and finance jobs'}
    ]
    
    for cat_data in default_job_categories:
        if not JobCategory.query.filter_by(name=cat_data['name']).first():
            category = JobCategory(**cat_data)
            db.session.add(category)
    
    # Default loan products
    from src.models.business import LoanProduct
    default_loan_products = [
        {
            'name': 'Micro Business Loan',
            'description': 'Small business startup loan',
            'min_amount': 5000,
            'max_amount': 50000,
            'interest_rate': 12.0,
            'tenure_months': 12
        },
        {
            'name': 'Agriculture Loan',
            'description': 'Farming and crop financing',
            'min_amount': 10000,
            'max_amount': 100000,
            'interest_rate': 10.0,
            'tenure_months': 24
        },
        {
            'name': 'Education Loan',
            'description': 'Educational expenses financing',
            'min_amount': 15000,
            'max_amount': 200000,
            'interest_rate': 8.0,
            'tenure_months': 36
        },
        {
            'name': 'Women Entrepreneur Loan',
            'description': 'Special loan for women entrepreneurs',
            'min_amount': 5000,
            'max_amount': 75000,
            'interest_rate': 10.0,
            'tenure_months': 18
        }
    ]
    
    for loan_data in default_loan_products:
        if not LoanProduct.query.filter_by(name=loan_data['name']).first():
            product = LoanProduct(**loan_data)
            db.session.add(product)
    
    # Default crops
    from src.models.agriculture import Crop
    default_crops = [
        {
            'name': 'Rice',
            'scientific_name': 'Oryza sativa',
            'category': 'cereal',
            'growing_season': 'kharif',
            'maturity_days': 120,
            'water_requirements': 'high'
        },
        {
            'name': 'Wheat',
            'scientific_name': 'Triticum aestivum',
            'category': 'cereal',
            'growing_season': 'rabi',
            'maturity_days': 110,
            'water_requirements': 'medium'
        },
        {
            'name': 'Potato',
            'scientific_name': 'Solanum tuberosum',
            'category': 'vegetable',
            'growing_season': 'rabi',
            'maturity_days': 90,
            'water_requirements': 'medium'
        },
        {
            'name': 'Tomato',
            'scientific_name': 'Solanum lycopersicum',
            'category': 'vegetable',
            'growing_season': 'rabi',
            'maturity_days': 75,
            'water_requirements': 'medium'
        }
    ]
    
    for crop_data in default_crops:
        if not Crop.query.filter_by(name=crop_data['name']).first():
            crop = Crop(**crop_data)
            db.session.add(crop)
    
    db.session.commit()

# Create the Flask app
app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

