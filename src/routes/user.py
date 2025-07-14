from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, db, DonorProfile, VolunteerProfile, BeneficiaryProfile
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users (admin only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.has_permission('user_management'):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        role_filter = request.args.get('role', '')
        
        query = User.query
        
        if search:
            query = query.filter(
                (User.first_name.ilike(f'%{search}%')) |
                (User.last_name.ilike(f'%{search}%')) |
                (User.email.ilike(f'%{search}%'))
            )
        
        if role_filter:
            query = query.join(User.roles).filter_by(name=role_filter)
        
        users = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get specific user details"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Users can view their own profile or admins can view any profile
        if current_user_id != user_id and not current_user.has_permission('user_management'):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict(include_sensitive=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user details"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Users can update their own profile or admins can update any profile
        if current_user_id != user_id and not current_user.has_permission('user_management'):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = [
            'first_name', 'last_name', 'phone', 'date_of_birth',
            'gender', 'address', 'city', 'state', 'country', 'postal_code'
        ]
        
        # Admin can update additional fields
        if current_user.has_permission('user_management'):
            allowed_fields.extend(['is_active', 'is_verified'])
        
        for field in allowed_fields:
            if field in data:
                if field == 'date_of_birth' and data[field]:
                    setattr(user, field, datetime.strptime(data[field], '%Y-%m-%d').date())
                else:
                    setattr(user, field, data[field])
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Delete user (admin only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.has_permission('user_management'):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Don't allow deleting self
        if current_user_id == user_id:
            return jsonify({'error': 'Cannot delete your own account'}), 400
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# =============================================
# DONOR PROFILE ROUTES
# =============================================

@user_bp.route('/donor-profile', methods=['GET'])
@jwt_required()
def get_donor_profile():
    """Get current user's donor profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if not user.donor_profile:
            return jsonify({'error': 'Donor profile not found'}), 404
        
        return jsonify({
            'donor_profile': user.donor_profile.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/donor-profile', methods=['POST'])
@jwt_required()
def create_donor_profile():
    """Create donor profile for current user"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.donor_profile:
            return jsonify({'error': 'Donor profile already exists'}), 400
        
        data = request.get_json()
        
        donor_profile = DonorProfile(
            user_id=current_user_id,
            donor_type=data.get('donor_type', 'individual'),
            organization_name=data.get('organization_name'),
            tax_id=data.get('tax_id'),
            preferred_causes=data.get('preferred_causes', []),
            donation_frequency=data.get('donation_frequency', 'one-time'),
            is_anonymous=data.get('is_anonymous', False)
        )
        
        db.session.add(donor_profile)
        
        # Add donor role if not already present
        if not user.has_role('donor'):
            from src.models.user import Role
            donor_role = Role.query.filter_by(name='donor').first()
            if donor_role:
                user.roles.append(donor_role)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Donor profile created successfully',
            'donor_profile': donor_profile.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/donor-profile', methods=['PUT'])
@jwt_required()
def update_donor_profile():
    """Update current user's donor profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.donor_profile:
            return jsonify({'error': 'Donor profile not found'}), 404
        
        data = request.get_json()
        donor_profile = user.donor_profile
        
        # Update allowed fields
        allowed_fields = [
            'donor_type', 'organization_name', 'tax_id', 'preferred_causes',
            'donation_frequency', 'is_anonymous'
        ]
        
        for field in allowed_fields:
            if field in data:
                setattr(donor_profile, field, data[field])
        
        donor_profile.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Donor profile updated successfully',
            'donor_profile': donor_profile.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# =============================================
# VOLUNTEER PROFILE ROUTES
# =============================================

@user_bp.route('/volunteer-profile', methods=['GET'])
@jwt_required()
def get_volunteer_profile():
    """Get current user's volunteer profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if not user.volunteer_profile:
            return jsonify({'error': 'Volunteer profile not found'}), 404
        
        return jsonify({
            'volunteer_profile': user.volunteer_profile.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/volunteer-profile', methods=['POST'])
@jwt_required()
def create_volunteer_profile():
    """Create volunteer profile for current user"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.volunteer_profile:
            return jsonify({'error': 'Volunteer profile already exists'}), 400
        
        data = request.get_json()
        
        volunteer_profile = VolunteerProfile(
            user_id=current_user_id,
            skills=data.get('skills', []),
            availability_days=data.get('availability_days', []),
            availability_hours=data.get('availability_hours'),
            experience_years=data.get('experience_years'),
            languages_spoken=data.get('languages_spoken', []),
            emergency_contact_name=data.get('emergency_contact_name'),
            emergency_contact_phone=data.get('emergency_contact_phone')
        )
        
        db.session.add(volunteer_profile)
        
        # Add volunteer role if not already present
        if not user.has_role('volunteer'):
            from src.models.user import Role
            volunteer_role = Role.query.filter_by(name='volunteer').first()
            if volunteer_role:
                user.roles.append(volunteer_role)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Volunteer profile created successfully',
            'volunteer_profile': volunteer_profile.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/volunteer-profile', methods=['PUT'])
@jwt_required()
def update_volunteer_profile():
    """Update current user's volunteer profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.volunteer_profile:
            return jsonify({'error': 'Volunteer profile not found'}), 404
        
        data = request.get_json()
        volunteer_profile = user.volunteer_profile
        
        # Update allowed fields
        allowed_fields = [
            'skills', 'availability_days', 'availability_hours', 'experience_years',
            'languages_spoken', 'emergency_contact_name', 'emergency_contact_phone'
        ]
        
        for field in allowed_fields:
            if field in data:
                setattr(volunteer_profile, field, data[field])
        
        volunteer_profile.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Volunteer profile updated successfully',
            'volunteer_profile': volunteer_profile.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# =============================================
# BENEFICIARY PROFILE ROUTES
# =============================================

@user_bp.route('/beneficiary-profile', methods=['GET'])
@jwt_required()
def get_beneficiary_profile():
    """Get current user's beneficiary profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if not user.beneficiary_profile:
            return jsonify({'error': 'Beneficiary profile not found'}), 404
        
        return jsonify({
            'beneficiary_profile': user.beneficiary_profile.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/beneficiary-profile', methods=['POST'])
@jwt_required()
def create_beneficiary_profile():
    """Create beneficiary profile for current user"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.beneficiary_profile:
            return jsonify({'error': 'Beneficiary profile already exists'}), 400
        
        data = request.get_json()
        
        beneficiary_profile = BeneficiaryProfile(
            user_id=current_user_id,
            household_size=data.get('household_size'),
            monthly_income=data.get('monthly_income'),
            employment_status=data.get('employment_status'),
            education_level=data.get('education_level'),
            health_conditions=data.get('health_conditions', []),
            assistance_needed=data.get('assistance_needed', [])
        )
        
        db.session.add(beneficiary_profile)
        
        # Add beneficiary role if not already present
        if not user.has_role('beneficiary'):
            from src.models.user import Role
            beneficiary_role = Role.query.filter_by(name='beneficiary').first()
            if beneficiary_role:
                user.roles.append(beneficiary_role)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Beneficiary profile created successfully',
            'beneficiary_profile': beneficiary_profile.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/beneficiary-profile', methods=['PUT'])
@jwt_required()
def update_beneficiary_profile():
    """Update current user's beneficiary profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.beneficiary_profile:
            return jsonify({'error': 'Beneficiary profile not found'}), 404
        
        data = request.get_json()
        beneficiary_profile = user.beneficiary_profile
        
        # Update allowed fields
        allowed_fields = [
            'household_size', 'monthly_income', 'employment_status',
            'education_level', 'health_conditions', 'assistance_needed'
        ]
        
        for field in allowed_fields:
            if field in data:
                setattr(beneficiary_profile, field, data[field])
        
        beneficiary_profile.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Beneficiary profile updated successfully',
            'beneficiary_profile': beneficiary_profile.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

