from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.agriculture import *
from datetime import datetime

agriculture_bp = Blueprint('agriculture', __name__)

# =============================================
# FARMER PROFILE ROUTES
# =============================================

@agriculture_bp.route('/farmer-profile', methods=['POST'])
@jwt_required()
def create_farmer_profile():
    """Create farmer profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        farmer = Farmer(
            user_id=current_user_id,
            farm_size_acres=data.get('farm_size_acres'),
            farming_experience_years=data.get('farming_experience_years'),
            primary_crops=data.get('primary_crops', []),
            farming_methods=data.get('farming_methods', []),
            land_ownership=data.get('land_ownership'),
            irrigation_access=data.get('irrigation_access', False),
            equipment_owned=data.get('equipment_owned', []),
            annual_income=data.get('annual_income')
        )
        
        db.session.add(farmer)
        db.session.commit()
        
        return jsonify({
            'message': 'Farmer profile created successfully',
            'farmer': farmer.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@agriculture_bp.route('/farmer-profile', methods=['GET'])
@jwt_required()
def get_farmer_profile():
    """Get current user's farmer profile"""
    try:
        current_user_id = get_jwt_identity()
        farmer = Farmer.query.filter_by(user_id=current_user_id).first()
        
        if not farmer:
            return jsonify({'error': 'Farmer profile not found'}), 404
        
        return jsonify({
            'farmer': farmer.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================
# CROP ROUTES
# =============================================

@agriculture_bp.route('/crops', methods=['GET'])
def get_crops():
    """Get all available crops"""
    try:
        crops = Crop.query.all()
        return jsonify({
            'crops': [crop.to_dict() for crop in crops]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@agriculture_bp.route('/crops/<int:crop_id>', methods=['GET'])
def get_crop(crop_id):
    """Get specific crop details"""
    try:
        crop = Crop.query.get_or_404(crop_id)
        return jsonify({
            'crop': crop.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================
# FARM MANAGEMENT ROUTES
# =============================================

@agriculture_bp.route('/farms', methods=['POST'])
@jwt_required()
def create_farm():
    """Create a new farm"""
    try:
        current_user_id = get_jwt_identity()
        farmer = Farmer.query.filter_by(user_id=current_user_id).first()
        
        if not farmer:
            return jsonify({'error': 'Farmer profile required'}), 400
        
        data = request.get_json()
        
        farm = Farm(
            farmer_id=farmer.id,
            name=data.get('name'),
            location_address=data.get('location_address'),
            location_coordinates=data.get('location_coordinates'),
            total_area_acres=data.get('total_area_acres'),
            soil_type=data.get('soil_type'),
            water_source=data.get('water_source'),
            infrastructure=data.get('infrastructure', [])
        )
        
        db.session.add(farm)
        db.session.commit()
        
        return jsonify({
            'message': 'Farm created successfully',
            'farm': farm.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@agriculture_bp.route('/my-farms', methods=['GET'])
@jwt_required()
def get_my_farms():
    """Get current user's farms"""
    try:
        current_user_id = get_jwt_identity()
        farmer = Farmer.query.filter_by(user_id=current_user_id).first()
        
        if not farmer:
            return jsonify({'farms': []}), 200
        
        farms = Farm.query.filter_by(farmer_id=farmer.id).all()
        
        return jsonify({
            'farms': [farm.to_dict() for farm in farms]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================
# CROP CYCLE ROUTES
# =============================================

@agriculture_bp.route('/crop-cycles', methods=['POST'])
@jwt_required()
def create_crop_cycle():
    """Create a new crop cycle"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Verify farm ownership
        farm = Farm.query.get_or_404(data['farm_id'])
        farmer = Farmer.query.filter_by(user_id=current_user_id).first()
        
        if not farmer or farm.farmer_id != farmer.id:
            return jsonify({'error': 'Access denied'}), 403
        
        crop_cycle = CropCycle(
            farm_id=data['farm_id'],
            crop_id=data.get('crop_id'),
            area_planted_acres=data.get('area_planted_acres'),
            planting_date=datetime.strptime(data['planting_date'], '%Y-%m-%d').date() if data.get('planting_date') else None,
            expected_harvest_date=datetime.strptime(data['expected_harvest_date'], '%Y-%m-%d').date() if data.get('expected_harvest_date') else None,
            notes=data.get('notes')
        )
        
        db.session.add(crop_cycle)
        db.session.commit()
        
        return jsonify({
            'message': 'Crop cycle created successfully',
            'crop_cycle': crop_cycle.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# =============================================
# AGRICULTURAL MARKETPLACE ROUTES
# =============================================

@agriculture_bp.route('/products', methods=['GET'])
def get_agricultural_products():
    """Get available agricultural products"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        crop_id = request.args.get('crop_id', type=int)
        location = request.args.get('location', '')
        is_organic = request.args.get('is_organic', type=bool)
        
        query = AgriculturalProduct.query.filter_by(is_available=True)
        
        if crop_id:
            query = query.filter_by(crop_id=crop_id)
        
        if location:
            query = query.filter(AgriculturalProduct.location_address.ilike(f'%{location}%'))
        
        if is_organic is not None:
            query = query.filter_by(is_organic=is_organic)
        
        products = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'products': [product.to_dict() for product in products.items],
            'total': products.total,
            'pages': products.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@agriculture_bp.route('/products', methods=['POST'])
@jwt_required()
def create_agricultural_product():
    """Create a new agricultural product listing"""
    try:
        current_user_id = get_jwt_identity()
        farmer = Farmer.query.filter_by(user_id=current_user_id).first()
        
        if not farmer:
            return jsonify({'error': 'Farmer profile required'}), 400
        
        data = request.get_json()
        
        product = AgriculturalProduct(
            farmer_id=farmer.id,
            crop_id=data.get('crop_id'),
            title=data['title'],
            description=data.get('description'),
            quantity_available=data.get('quantity_available'),
            unit=data.get('unit'),
            price_per_unit=data.get('price_per_unit'),
            quality_grade=data.get('quality_grade'),
            harvest_date=datetime.strptime(data['harvest_date'], '%Y-%m-%d').date() if data.get('harvest_date') else None,
            location_address=data.get('location_address'),
            location_coordinates=data.get('location_coordinates'),
            images=data.get('images', []),
            is_organic=data.get('is_organic', False)
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'message': 'Product listed successfully',
            'product': product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@agriculture_bp.route('/products/<int:product_id>/inquire', methods=['POST'])
@jwt_required()
def create_product_inquiry():
    """Create an inquiry for a product"""
    try:
        current_user_id = get_jwt_identity()
        product = AgriculturalProduct.query.get_or_404(product_id)
        
        data = request.get_json()
        
        inquiry = ProductInquiry(
            product_id=product_id,
            buyer_id=current_user_id,
            quantity_requested=data.get('quantity_requested'),
            offered_price=data.get('offered_price'),
            message=data.get('message')
        )
        
        db.session.add(inquiry)
        db.session.commit()
        
        return jsonify({
            'message': 'Inquiry submitted successfully',
            'inquiry': inquiry.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# =============================================
# AGRICULTURAL ADVISORY ROUTES
# =============================================

@agriculture_bp.route('/advisories', methods=['GET'])
def get_agricultural_advisories():
    """Get active agricultural advisories"""
    try:
        advisories = AgriculturalAdvisory.query.filter(
            AgriculturalAdvisory.valid_until >= datetime.utcnow().date()
        ).all()
        
        return jsonify({
            'advisories': [advisory.to_dict() for advisory in advisories if advisory.is_active]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@agriculture_bp.route('/weather', methods=['GET'])
def get_weather_data():
    """Get weather data for a location"""
    try:
        location = request.args.get('location')
        days = request.args.get('days', 7, type=int)
        
        if not location:
            return jsonify({'error': 'Location parameter required'}), 400
        
        weather_data = WeatherData.query.filter(
            WeatherData.location_coordinates == location
        ).order_by(WeatherData.date.desc()).limit(days).all()
        
        return jsonify({
            'weather_data': [data.to_dict() for data in weather_data]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

