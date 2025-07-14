from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.business import *
from datetime import datetime

business_bp = Blueprint('business', __name__)

# =============================================
# LOAN PRODUCT ROUTES
# =============================================

@business_bp.route('/loan-products', methods=['GET'])
def get_loan_products():
    """Get all active loan products"""
    try:
        loan_products = LoanProduct.query.filter_by(is_active=True).all()
        return jsonify({
            'loan_products': [product.to_dict() for product in loan_products]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@business_bp.route('/loan-products/<int:product_id>', methods=['GET'])
def get_loan_product(product_id):
    """Get specific loan product details"""
    try:
        product = LoanProduct.query.get_or_404(product_id)
        return jsonify({
            'loan_product': product.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================
# LOAN APPLICATION ROUTES
# =============================================

@business_bp.route('/loan-applications', methods=['POST'])
@jwt_required()
def apply_for_loan():
    """Apply for a loan"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        application = LoanApplication(
            applicant_id=current_user_id,
            loan_product_id=data['loan_product_id'],
            requested_amount=data['requested_amount'],
            purpose=data.get('purpose'),
            business_plan=data.get('business_plan'),
            monthly_income=data.get('monthly_income'),
            existing_loans=data.get('existing_loans', 0),
            collateral_details=data.get('collateral_details'),
            guarantor_info=data.get('guarantor_info', {}),
            documents=data.get('documents', [])
        )
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify({
            'message': 'Loan application submitted successfully',
            'application': application.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@business_bp.route('/my-loan-applications', methods=['GET'])
@jwt_required()
def get_my_loan_applications():
    """Get current user's loan applications"""
    try:
        current_user_id = get_jwt_identity()
        applications = LoanApplication.query.filter_by(applicant_id=current_user_id).all()
        
        return jsonify({
            'applications': [application.to_dict() for application in applications]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@business_bp.route('/my-loans', methods=['GET'])
@jwt_required()
def get_my_loans():
    """Get current user's active loans"""
    try:
        current_user_id = get_jwt_identity()
        loans = Loan.query.filter_by(borrower_id=current_user_id).all()
        
        return jsonify({
            'loans': [loan.to_dict() for loan in loans]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================
# TRAINING PROGRAM ROUTES
# =============================================

@business_bp.route('/training-programs', methods=['GET'])
def get_training_programs():
    """Get all active training programs"""
    try:
        programs = TrainingProgram.query.filter_by(is_active=True).all()
        return jsonify({
            'training_programs': [program.to_dict() for program in programs]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@business_bp.route('/training-programs/<int:program_id>', methods=['GET'])
def get_training_program(program_id):
    """Get specific training program details"""
    try:
        program = TrainingProgram.query.get_or_404(program_id)
        return jsonify({
            'training_program': program.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@business_bp.route('/training-programs/<int:program_id>/enroll', methods=['POST'])
@jwt_required()
def enroll_in_training(program_id):
    """Enroll in a training program"""
    try:
        current_user_id = get_jwt_identity()
        program = TrainingProgram.query.get_or_404(program_id)
        
        if not program.is_enrollment_open:
            return jsonify({'error': 'Enrollment is closed for this program'}), 400
        
        # Check if already enrolled
        existing_enrollment = TrainingEnrollment.query.filter_by(
            program_id=program_id, participant_id=current_user_id
        ).first()
        
        if existing_enrollment:
            return jsonify({'error': 'Already enrolled in this program'}), 400
        
        enrollment = TrainingEnrollment(
            program_id=program_id,
            participant_id=current_user_id
        )
        
        db.session.add(enrollment)
        db.session.commit()
        
        return jsonify({
            'message': 'Enrolled successfully',
            'enrollment': enrollment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@business_bp.route('/my-training-enrollments', methods=['GET'])
@jwt_required()
def get_my_training_enrollments():
    """Get current user's training enrollments"""
    try:
        current_user_id = get_jwt_identity()
        enrollments = TrainingEnrollment.query.filter_by(participant_id=current_user_id).all()
        
        return jsonify({
            'enrollments': [enrollment.to_dict() for enrollment in enrollments]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================
# JOB PORTAL ROUTES
# =============================================

@business_bp.route('/job-categories', methods=['GET'])
def get_job_categories():
    """Get all job categories"""
    try:
        categories = JobCategory.query.filter_by(is_active=True).all()
        return jsonify({
            'job_categories': [category.to_dict() for category in categories]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@business_bp.route('/jobs', methods=['GET'])
def get_jobs():
    """Get all active job postings"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category_id = request.args.get('category_id', type=int)
        location = request.args.get('location', '')
        employment_type = request.args.get('employment_type', '')
        search = request.args.get('search', '')
        
        query = JobPosting.query.filter_by(is_active=True)
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if location:
            query = query.filter(JobPosting.location_address.ilike(f'%{location}%'))
        
        if employment_type:
            query = query.filter_by(employment_type=employment_type)
        
        if search:
            query = query.filter(JobPosting.title.ilike(f'%{search}%'))
        
        jobs = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'jobs': [job.to_dict() for job in jobs.items],
            'total': jobs.total,
            'pages': jobs.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@business_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get specific job details"""
    try:
        job = JobPosting.query.get_or_404(job_id)
        return jsonify({
            'job': job.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@business_bp.route('/jobs', methods=['POST'])
@jwt_required()
def create_job_posting():
    """Create a new job posting"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        job = JobPosting(
            title=data['title'],
            description=data.get('description'),
            category_id=data.get('category_id'),
            employer_id=current_user_id,
            company_name=data.get('company_name'),
            location_address=data.get('location_address'),
            employment_type=data.get('employment_type', 'full_time'),
            experience_required=data.get('experience_required'),
            skills_required=data.get('skills_required', []),
            salary_min=data.get('salary_min'),
            salary_max=data.get('salary_max'),
            application_deadline=datetime.strptime(data['application_deadline'], '%Y-%m-%d').date() if data.get('application_deadline') else None
        )
        
        db.session.add(job)
        db.session.commit()
        
        return jsonify({
            'message': 'Job posted successfully',
            'job': job.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@business_bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
@jwt_required()
def apply_for_job(job_id):
    """Apply for a job"""
    try:
        current_user_id = get_jwt_identity()
        job = JobPosting.query.get_or_404(job_id)
        
        if not job.is_application_open:
            return jsonify({'error': 'Application deadline has passed'}), 400
        
        # Check if already applied
        existing_application = JobApplication.query.filter_by(
            job_id=job_id, applicant_id=current_user_id
        ).first()
        
        if existing_application:
            return jsonify({'error': 'Already applied for this job'}), 400
        
        data = request.get_json()
        
        application = JobApplication(
            job_id=job_id,
            applicant_id=current_user_id,
            cover_letter=data.get('cover_letter'),
            resume_url=data.get('resume_url')
        )
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify({
            'message': 'Application submitted successfully',
            'application': application.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@business_bp.route('/my-job-applications', methods=['GET'])
@jwt_required()
def get_my_job_applications():
    """Get current user's job applications"""
    try:
        current_user_id = get_jwt_identity()
        applications = JobApplication.query.filter_by(applicant_id=current_user_id).all()
        
        return jsonify({
            'applications': [application.to_dict() for application in applications]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@business_bp.route('/my-job-postings', methods=['GET'])
@jwt_required()
def get_my_job_postings():
    """Get current user's job postings"""
    try:
        current_user_id = get_jwt_identity()
        jobs = JobPosting.query.filter_by(employer_id=current_user_id).all()
        
        return jsonify({
            'jobs': [job.to_dict() for job in jobs]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

