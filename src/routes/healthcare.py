from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.healthcare import *
from datetime import datetime

healthcare_bp = Blueprint('healthcare', __name__)

# =============================================
# HEALTHCARE PROVIDER ROUTES
# =============================================

@healthcare_bp.route('/providers', methods=['GET'])
def get_providers():
    """Get all verified healthcare providers"""
    try:
        providers = HealthcareProvider.query.filter_by(is_verified=True).all()
        return jsonify({
            'providers': [provider.to_dict() for provider in providers]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@healthcare_bp.route('/provider-profile', methods=['POST'])
@jwt_required()
def create_provider_profile():
    """Create healthcare provider profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        provider = HealthcareProvider(
            user_id=current_user_id,
            license_number=data.get('license_number'),
            specialization=data.get('specialization'),
            qualifications=data.get('qualifications', []),
            experience_years=data.get('experience_years'),
            consultation_fee=data.get('consultation_fee'),
            availability_schedule=data.get('availability_schedule', {})
        )
        
        db.session.add(provider)
        db.session.commit()
        
        return jsonify({
            'message': 'Provider profile created successfully',
            'provider': provider.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# =============================================
# CONSULTATION ROUTES
# =============================================

@healthcare_bp.route('/consultations', methods=['POST'])
@jwt_required()
def book_consultation():
    """Book a consultation"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Get or create patient profile
        patient = Patient.query.filter_by(user_id=current_user_id).first()
        if not patient:
            patient = Patient(user_id=current_user_id)
            db.session.add(patient)
            db.session.flush()
        
        consultation = Consultation(
            patient_id=patient.id,
            provider_id=data['provider_id'],
            consultation_type=data.get('consultation_type', 'online'),
            appointment_date=datetime.strptime(data['appointment_date'], '%Y-%m-%d %H:%M'),
            symptoms=data.get('symptoms')
        )
        
        db.session.add(consultation)
        db.session.commit()
        
        return jsonify({
            'message': 'Consultation booked successfully',
            'consultation': consultation.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@healthcare_bp.route('/my-consultations', methods=['GET'])
@jwt_required()
def get_my_consultations():
    """Get current user's consultations"""
    try:
        current_user_id = get_jwt_identity()
        patient = Patient.query.filter_by(user_id=current_user_id).first()
        
        if not patient:
            return jsonify({'consultations': []}), 200
        
        consultations = Consultation.query.filter_by(patient_id=patient.id).all()
        
        return jsonify({
            'consultations': [consultation.to_dict() for consultation in consultations]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================
# BLOOD DONATION ROUTES
# =============================================

@healthcare_bp.route('/blood-donors', methods=['GET'])
def get_blood_donors():
    """Get available blood donors"""
    try:
        blood_group = request.args.get('blood_group')
        
        query = BloodDonor.query.filter_by(is_available=True, health_status='eligible')
        
        if blood_group:
            query = query.filter_by(blood_group=blood_group)
        
        donors = query.all()
        
        return jsonify({
            'donors': [donor.to_dict() for donor in donors]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@healthcare_bp.route('/blood-requests', methods=['POST'])
@jwt_required()
def create_blood_request():
    """Create a blood request"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        blood_request = BloodRequest(
            requester_id=current_user_id,
            patient_name=data['patient_name'],
            blood_group=data['blood_group'],
            units_needed=data.get('units_needed', 1),
            urgency_level=data.get('urgency_level', 'medium'),
            hospital_name=data.get('hospital_name'),
            hospital_address=data.get('hospital_address'),
            contact_phone=data.get('contact_phone'),
            needed_by_date=datetime.strptime(data['needed_by_date'], '%Y-%m-%d').date() if data.get('needed_by_date') else None
        )
        
        db.session.add(blood_request)
        db.session.commit()
        
        return jsonify({
            'message': 'Blood request created successfully',
            'blood_request': blood_request.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@healthcare_bp.route('/blood-requests', methods=['GET'])
def get_blood_requests():
    """Get active blood requests"""
    try:
        requests = BloodRequest.query.filter_by(status='active').all()
        
        return jsonify({
            'blood_requests': [request.to_dict() for request in requests]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================
# MEDICAL CAMP ROUTES
# =============================================

@healthcare_bp.route('/medical-camps', methods=['GET'])
def get_medical_camps():
    """Get active medical camps"""
    try:
        camps = MedicalCamp.query.filter_by(is_active=True).all()
        
        return jsonify({
            'medical_camps': [camp.to_dict() for camp in camps]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@healthcare_bp.route('/medical-camps/<int:camp_id>/register', methods=['POST'])
@jwt_required()
def register_for_camp(camp_id):
    """Register for a medical camp"""
    try:
        current_user_id = get_jwt_identity()
        camp = MedicalCamp.query.get_or_404(camp_id)
        
        if not camp.is_registration_open:
            return jsonify({'error': 'Registration is closed for this camp'}), 400
        
        # Get or create patient profile
        patient = Patient.query.filter_by(user_id=current_user_id).first()
        if not patient:
            patient = Patient(user_id=current_user_id)
            db.session.add(patient)
            db.session.flush()
        
        # Check if already registered
        existing_registration = CampRegistration.query.filter_by(
            camp_id=camp_id, patient_id=patient.id
        ).first()
        
        if existing_registration:
            return jsonify({'error': 'Already registered for this camp'}), 400
        
        data = request.get_json()
        
        registration = CampRegistration(
            camp_id=camp_id,
            patient_id=patient.id,
            services_requested=data.get('services_requested', []),
            special_requirements=data.get('special_requirements')
        )
        
        db.session.add(registration)
        db.session.commit()
        
        return jsonify({
            'message': 'Registered for medical camp successfully',
            'registration': registration.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

