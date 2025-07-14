from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.education import (
    CourseCategory, Course, CourseModule, Lesson, Enrollment, 
    LessonProgress, Assessment, AssessmentQuestion, AssessmentSubmission,
    Scholarship, ScholarshipApplication
)
from datetime import datetime

education_bp = Blueprint('education', __name__)

# =============================================
# COURSE CATEGORY ROUTES
# =============================================

@education_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all course categories"""
    try:
        categories = CourseCategory.query.filter_by(is_active=True).all()
        return jsonify({
            'categories': [category.to_dict() for category in categories]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@education_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    """Create new course category (admin only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.has_permission('course_management'):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        data = request.get_json()
        
        category = CourseCategory(
            name=data['name'],
            description=data.get('description'),
            parent_id=data.get('parent_id'),
            sort_order=data.get('sort_order', 0)
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Category created successfully',
            'category': category.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# =============================================
# COURSE ROUTES
# =============================================

@education_bp.route('/courses', methods=['GET'])
def get_courses():
    """Get all published courses"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category_id = request.args.get('category_id', type=int)
        search = request.args.get('search', '')
        difficulty = request.args.get('difficulty', '')
        is_free = request.args.get('is_free', type=bool)
        
        query = Course.query.filter_by(is_published=True)
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if search:
            query = query.filter(Course.title.ilike(f'%{search}%'))
        
        if difficulty:
            query = query.filter_by(difficulty_level=difficulty)
        
        if is_free is not None:
            query = query.filter_by(is_free=is_free)
        
        courses = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'courses': [course.to_dict() for course in courses.items],
            'total': courses.total,
            'pages': courses.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@education_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """Get specific course details"""
    try:
        course = Course.query.get_or_404(course_id)
        
        if not course.is_published:
            return jsonify({'error': 'Course not found'}), 404
        
        return jsonify({
            'course': course.to_dict(include_modules=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@education_bp.route('/courses', methods=['POST'])
@jwt_required()
def create_course():
    """Create new course (educators only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not (current_user.has_role('educator') or current_user.has_permission('course_management')):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        data = request.get_json()
        
        course = Course(
            title=data['title'],
            description=data.get('description'),
            category_id=data.get('category_id'),
            instructor_id=current_user_id,
            difficulty_level=data.get('difficulty_level', 'beginner'),
            duration_hours=data.get('duration_hours'),
            language=data.get('language', 'bn'),
            prerequisites=data.get('prerequisites'),
            learning_objectives=data.get('learning_objectives', []),
            course_image_url=data.get('course_image_url'),
            price=data.get('price', 0),
            is_free=data.get('is_free', True),
            enrollment_limit=data.get('enrollment_limit'),
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data.get('start_date') else None,
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None
        )
        
        db.session.add(course)
        db.session.commit()
        
        return jsonify({
            'message': 'Course created successfully',
            'course': course.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@education_bp.route('/courses/<int:course_id>', methods=['PUT'])
@jwt_required()
def update_course(course_id):
    """Update course (instructor or admin only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        course = Course.query.get_or_404(course_id)
        
        if not (course.instructor_id == current_user_id or current_user.has_permission('course_management')):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = [
            'title', 'description', 'category_id', 'difficulty_level',
            'duration_hours', 'prerequisites', 'learning_objectives',
            'course_image_url', 'price', 'is_free', 'enrollment_limit',
            'start_date', 'end_date'
        ]
        
        for field in allowed_fields:
            if field in data:
                if field in ['start_date', 'end_date'] and data[field]:
                    setattr(course, field, datetime.strptime(data[field], '%Y-%m-%d').date())
                else:
                    setattr(course, field, data[field])
        
        course.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Course updated successfully',
            'course': course.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# =============================================
# ENROLLMENT ROUTES
# =============================================

@education_bp.route('/courses/<int:course_id>/enroll', methods=['POST'])
@jwt_required()
def enroll_course(course_id):
    """Enroll in a course"""
    try:
        current_user_id = get_jwt_identity()
        course = Course.query.get_or_404(course_id)
        
        if not course.is_enrollment_open:
            return jsonify({'error': 'Enrollment is not open for this course'}), 400
        
        # Check if already enrolled
        existing_enrollment = Enrollment.query.filter_by(
            course_id=course_id, student_id=current_user_id
        ).first()
        
        if existing_enrollment:
            return jsonify({'error': 'Already enrolled in this course'}), 400
        
        enrollment = Enrollment(
            course_id=course_id,
            student_id=current_user_id
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

@education_bp.route('/my-courses', methods=['GET'])
@jwt_required()
def get_my_courses():
    """Get current user's enrolled courses"""
    try:
        current_user_id = get_jwt_identity()
        
        enrollments = Enrollment.query.filter_by(student_id=current_user_id).all()
        
        return jsonify({
            'enrollments': [enrollment.to_dict() for enrollment in enrollments]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@education_bp.route('/enrollments/<int:enrollment_id>/progress', methods=['GET'])
@jwt_required()
def get_enrollment_progress(enrollment_id):
    """Get detailed progress for an enrollment"""
    try:
        current_user_id = get_jwt_identity()
        enrollment = Enrollment.query.get_or_404(enrollment_id)
        
        if enrollment.student_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        lesson_progress = LessonProgress.query.filter_by(enrollment_id=enrollment_id).all()
        
        return jsonify({
            'enrollment': enrollment.to_dict(),
            'lesson_progress': [progress.to_dict() for progress in lesson_progress]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@education_bp.route('/lessons/<int:lesson_id>/complete', methods=['POST'])
@jwt_required()
def complete_lesson(lesson_id):
    """Mark a lesson as completed"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        enrollment_id = data.get('enrollment_id')
        
        # Verify enrollment belongs to current user
        enrollment = Enrollment.query.get_or_404(enrollment_id)
        if enrollment.student_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Get or create lesson progress
        lesson_progress = LessonProgress.query.filter_by(
            enrollment_id=enrollment_id, lesson_id=lesson_id
        ).first()
        
        if not lesson_progress:
            lesson_progress = LessonProgress(
                enrollment_id=enrollment_id,
                lesson_id=lesson_id
            )
            db.session.add(lesson_progress)
        
        lesson_progress.completed_at = datetime.utcnow()
        lesson_progress.time_spent_minutes = data.get('time_spent_minutes', 0)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Lesson completed successfully',
            'lesson_progress': lesson_progress.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# =============================================
# ASSESSMENT ROUTES
# =============================================

@education_bp.route('/courses/<int:course_id>/assessments', methods=['GET'])
@jwt_required()
def get_course_assessments(course_id):
    """Get assessments for a course"""
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user is enrolled in the course
        enrollment = Enrollment.query.filter_by(
            course_id=course_id, student_id=current_user_id
        ).first()
        
        if not enrollment:
            return jsonify({'error': 'Not enrolled in this course'}), 403
        
        assessments = Assessment.query.filter_by(
            course_id=course_id, is_published=True
        ).all()
        
        return jsonify({
            'assessments': [assessment.to_dict() for assessment in assessments]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@education_bp.route('/assessments/<int:assessment_id>', methods=['GET'])
@jwt_required()
def get_assessment(assessment_id):
    """Get assessment details with questions"""
    try:
        current_user_id = get_jwt_identity()
        assessment = Assessment.query.get_or_404(assessment_id)
        
        # Check if user is enrolled in the course
        enrollment = Enrollment.query.filter_by(
            course_id=assessment.course_id, student_id=current_user_id
        ).first()
        
        if not enrollment:
            return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({
            'assessment': assessment.to_dict(include_questions=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@education_bp.route('/assessments/<int:assessment_id>/submit', methods=['POST'])
@jwt_required()
def submit_assessment(assessment_id):
    """Submit assessment answers"""
    try:
        current_user_id = get_jwt_identity()
        assessment = Assessment.query.get_or_404(assessment_id)
        
        # Check if user is enrolled in the course
        enrollment = Enrollment.query.filter_by(
            course_id=assessment.course_id, student_id=current_user_id
        ).first()
        
        if not enrollment:
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        answers = data.get('answers', {})
        
        # Check if already submitted (based on attempts allowed)
        existing_submissions = AssessmentSubmission.query.filter_by(
            assessment_id=assessment_id, student_id=current_user_id
        ).count()
        
        if existing_submissions >= assessment.attempts_allowed:
            return jsonify({'error': 'Maximum attempts exceeded'}), 400
        
        submission = AssessmentSubmission(
            assessment_id=assessment_id,
            student_id=current_user_id,
            answers=answers
        )
        
        db.session.add(submission)
        db.session.commit()
        
        return jsonify({
            'message': 'Assessment submitted successfully',
            'submission': submission.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# =============================================
# SCHOLARSHIP ROUTES
# =============================================

@education_bp.route('/scholarships', methods=['GET'])
def get_scholarships():
    """Get all active scholarships"""
    try:
        scholarships = Scholarship.query.filter_by(is_active=True).all()
        
        return jsonify({
            'scholarships': [scholarship.to_dict() for scholarship in scholarships]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@education_bp.route('/scholarships/<int:scholarship_id>', methods=['GET'])
def get_scholarship(scholarship_id):
    """Get specific scholarship details"""
    try:
        scholarship = Scholarship.query.get_or_404(scholarship_id)
        
        return jsonify({
            'scholarship': scholarship.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@education_bp.route('/scholarships/<int:scholarship_id>/apply', methods=['POST'])
@jwt_required()
def apply_scholarship(scholarship_id):
    """Apply for a scholarship"""
    try:
        current_user_id = get_jwt_identity()
        scholarship = Scholarship.query.get_or_404(scholarship_id)
        
        if not scholarship.is_application_open:
            return jsonify({'error': 'Application is not open for this scholarship'}), 400
        
        # Check if already applied
        existing_application = ScholarshipApplication.query.filter_by(
            scholarship_id=scholarship_id, applicant_id=current_user_id
        ).first()
        
        if existing_application:
            return jsonify({'error': 'Already applied for this scholarship'}), 400
        
        data = request.get_json()
        
        application = ScholarshipApplication(
            scholarship_id=scholarship_id,
            applicant_id=current_user_id,
            application_data=data.get('application_data', {}),
            documents=data.get('documents', [])
        )
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify({
            'message': 'Scholarship application submitted successfully',
            'application': application.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@education_bp.route('/my-scholarship-applications', methods=['GET'])
@jwt_required()
def get_my_scholarship_applications():
    """Get current user's scholarship applications"""
    try:
        current_user_id = get_jwt_identity()
        
        applications = ScholarshipApplication.query.filter_by(
            applicant_id=current_user_id
        ).all()
        
        return jsonify({
            'applications': [application.to_dict() for application in applications]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================
# INSTRUCTOR ROUTES
# =============================================

@education_bp.route('/my-courses-as-instructor', methods=['GET'])
@jwt_required()
def get_my_courses_as_instructor():
    """Get courses where current user is the instructor"""
    try:
        current_user_id = get_jwt_identity()
        
        courses = Course.query.filter_by(instructor_id=current_user_id).all()
        
        return jsonify({
            'courses': [course.to_dict() for course in courses]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@education_bp.route('/courses/<int:course_id>/students', methods=['GET'])
@jwt_required()
def get_course_students(course_id):
    """Get students enrolled in a course (instructor only)"""
    try:
        current_user_id = get_jwt_identity()
        course = Course.query.get_or_404(course_id)
        
        if course.instructor_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        enrollments = Enrollment.query.filter_by(course_id=course_id).all()
        
        return jsonify({
            'students': [enrollment.to_dict() for enrollment in enrollments]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

