from src.models.user import db
from datetime import datetime

class CourseCategory(db.Model):
    __tablename__ = 'course_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('course_categories.id'))
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Self-referential relationship for subcategories
    parent = db.relationship('CourseCategory', remote_side=[id], backref='subcategories')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id,
            'sort_order': self.sort_order,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'subcategories': [sub.to_dict() for sub in self.subcategories] if self.subcategories else []
        }

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('course_categories.id'))
    instructor_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    difficulty_level = db.Column(db.String(20))  # beginner, intermediate, advanced
    duration_hours = db.Column(db.Integer)
    language = db.Column(db.String(10), default='bn')
    prerequisites = db.Column(db.Text)
    learning_objectives = db.Column(db.JSON)  # Array of objectives
    course_image_url = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), default=0)
    is_free = db.Column(db.Boolean, default=True)
    is_published = db.Column(db.Boolean, default=False)
    enrollment_limit = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = db.relationship('CourseCategory', backref='courses')
    instructor = db.relationship('User', backref='taught_courses')
    modules = db.relationship('CourseModule', backref='course', cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', backref='course', cascade='all, delete-orphan')
    assessments = db.relationship('Assessment', backref='course', cascade='all, delete-orphan')
    
    @property
    def enrollment_count(self):
        return len(self.enrollments)
    
    @property
    def is_enrollment_open(self):
        if self.enrollment_limit and self.enrollment_count >= self.enrollment_limit:
            return False
        if self.end_date and self.end_date < datetime.utcnow().date():
            return False
        return self.is_published
    
    def to_dict(self, include_modules=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'instructor_id': self.instructor_id,
            'instructor_name': self.instructor.full_name if self.instructor else None,
            'difficulty_level': self.difficulty_level,
            'duration_hours': self.duration_hours,
            'language': self.language,
            'prerequisites': self.prerequisites,
            'learning_objectives': self.learning_objectives,
            'course_image_url': self.course_image_url,
            'price': float(self.price) if self.price else 0,
            'is_free': self.is_free,
            'is_published': self.is_published,
            'enrollment_limit': self.enrollment_limit,
            'enrollment_count': self.enrollment_count,
            'is_enrollment_open': self.is_enrollment_open,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_modules:
            data['modules'] = [module.to_dict(include_lessons=True) for module in self.modules]
        
        return data

class CourseModule(db.Model):
    __tablename__ = 'course_modules'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    lessons = db.relationship('Lesson', backref='module', cascade='all, delete-orphan')
    
    def to_dict(self, include_lessons=False):
        data = {
            'id': self.id,
            'course_id': self.course_id,
            'title': self.title,
            'description': self.description,
            'sort_order': self.sort_order,
            'is_published': self.is_published,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'lesson_count': len(self.lessons)
        }
        
        if include_lessons:
            data['lessons'] = [lesson.to_dict() for lesson in self.lessons]
        
        return data

class Lesson(db.Model):
    __tablename__ = 'lessons'
    
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('course_modules.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    content_type = db.Column(db.String(20))  # text, video, audio, document
    content_url = db.Column(db.Text)
    duration_minutes = db.Column(db.Integer)
    sort_order = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'title': self.title,
            'content': self.content,
            'content_type': self.content_type,
            'content_url': self.content_url,
            'duration_minutes': self.duration_minutes,
            'sort_order': self.sort_order,
            'is_published': self.is_published,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    student_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime)
    progress_percentage = db.Column(db.Integer, default=0)
    final_grade = db.Column(db.Numeric(5, 2))
    certificate_issued = db.Column(db.Boolean, default=False)
    certificate_url = db.Column(db.Text)
    
    # Relationships
    student = db.relationship('User', backref='enrollments')
    lesson_progress = db.relationship('LessonProgress', backref='enrollment', cascade='all, delete-orphan')
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('course_id', 'student_id', name='unique_course_student'),)
    
    @property
    def is_completed(self):
        return self.completion_date is not None
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'course_title': self.course.title if self.course else None,
            'student_id': self.student_id,
            'student_name': self.student.full_name if self.student else None,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'progress_percentage': self.progress_percentage,
            'final_grade': float(self.final_grade) if self.final_grade else None,
            'certificate_issued': self.certificate_issued,
            'certificate_url': self.certificate_url,
            'is_completed': self.is_completed
        }

class LessonProgress(db.Model):
    __tablename__ = 'lesson_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    time_spent_minutes = db.Column(db.Integer, default=0)
    
    # Relationships
    lesson = db.relationship('Lesson', backref='progress_records')
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('enrollment_id', 'lesson_id', name='unique_enrollment_lesson'),)
    
    @property
    def is_completed(self):
        return self.completed_at is not None
    
    def to_dict(self):
        return {
            'id': self.id,
            'enrollment_id': self.enrollment_id,
            'lesson_id': self.lesson_id,
            'lesson_title': self.lesson.title if self.lesson else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'time_spent_minutes': self.time_spent_minutes,
            'is_completed': self.is_completed
        }

class Assessment(db.Model):
    __tablename__ = 'assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    assessment_type = db.Column(db.String(20))  # quiz, assignment, exam
    total_marks = db.Column(db.Integer)
    passing_marks = db.Column(db.Integer)
    time_limit_minutes = db.Column(db.Integer)
    attempts_allowed = db.Column(db.Integer, default=1)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    questions = db.relationship('AssessmentQuestion', backref='assessment', cascade='all, delete-orphan')
    submissions = db.relationship('AssessmentSubmission', backref='assessment', cascade='all, delete-orphan')
    
    def to_dict(self, include_questions=False):
        data = {
            'id': self.id,
            'course_id': self.course_id,
            'course_title': self.course.title if self.course else None,
            'title': self.title,
            'description': self.description,
            'assessment_type': self.assessment_type,
            'total_marks': self.total_marks,
            'passing_marks': self.passing_marks,
            'time_limit_minutes': self.time_limit_minutes,
            'attempts_allowed': self.attempts_allowed,
            'is_published': self.is_published,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'question_count': len(self.questions)
        }
        
        if include_questions:
            data['questions'] = [q.to_dict() for q in self.questions]
        
        return data

class AssessmentQuestion(db.Model):
    __tablename__ = 'assessment_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20))  # multiple_choice, true_false, essay, fill_blank
    options = db.Column(db.JSON)  # For multiple choice questions
    correct_answer = db.Column(db.Text)
    marks = db.Column(db.Integer, default=1)
    sort_order = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'options': self.options,
            'marks': self.marks,
            'sort_order': self.sort_order
            # Note: correct_answer is not included for security
        }

class AssessmentSubmission(db.Model):
    __tablename__ = 'assessment_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    student_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    answers = db.Column(db.JSON)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    graded_at = db.Column(db.DateTime)
    graded_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    total_marks = db.Column(db.Integer)
    obtained_marks = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    
    # Relationships
    student = db.relationship('User', foreign_keys=[student_id], backref='assessment_submissions')
    grader = db.relationship('User', foreign_keys=[graded_by])
    
    @property
    def is_graded(self):
        return self.graded_at is not None
    
    @property
    def percentage_score(self):
        if self.total_marks and self.obtained_marks is not None:
            return (self.obtained_marks / self.total_marks) * 100
        return None
    
    @property
    def is_passed(self):
        if self.assessment and self.assessment.passing_marks and self.obtained_marks is not None:
            return self.obtained_marks >= self.assessment.passing_marks
        return None
    
    def to_dict(self):
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'assessment_title': self.assessment.title if self.assessment else None,
            'student_id': self.student_id,
            'student_name': self.student.full_name if self.student else None,
            'answers': self.answers,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'graded_at': self.graded_at.isoformat() if self.graded_at else None,
            'graded_by': self.graded_by,
            'total_marks': self.total_marks,
            'obtained_marks': self.obtained_marks,
            'percentage_score': self.percentage_score,
            'is_passed': self.is_passed,
            'feedback': self.feedback,
            'is_graded': self.is_graded
        }

class Scholarship(db.Model):
    __tablename__ = 'scholarships'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    amount = db.Column(db.Numeric(10, 2))
    eligibility_criteria = db.Column(db.Text)
    application_deadline = db.Column(db.Date)
    selection_criteria = db.Column(db.Text)
    total_slots = db.Column(db.Integer)
    available_slots = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', backref='created_scholarships')
    applications = db.relationship('ScholarshipApplication', backref='scholarship', cascade='all, delete-orphan')
    
    @property
    def application_count(self):
        return len(self.applications)
    
    @property
    def is_application_open(self):
        if self.application_deadline and self.application_deadline < datetime.utcnow().date():
            return False
        if self.available_slots is not None and self.available_slots <= 0:
            return False
        return self.is_active
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'amount': float(self.amount) if self.amount else None,
            'eligibility_criteria': self.eligibility_criteria,
            'application_deadline': self.application_deadline.isoformat() if self.application_deadline else None,
            'selection_criteria': self.selection_criteria,
            'total_slots': self.total_slots,
            'available_slots': self.available_slots,
            'application_count': self.application_count,
            'is_active': self.is_active,
            'is_application_open': self.is_application_open,
            'created_by': self.created_by,
            'creator_name': self.creator.full_name if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ScholarshipApplication(db.Model):
    __tablename__ = 'scholarship_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    scholarship_id = db.Column(db.Integer, db.ForeignKey('scholarships.id'), nullable=False)
    applicant_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    application_data = db.Column(db.JSON)
    documents = db.Column(db.JSON)  # Array of document URLs
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    reviewed_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    review_notes = db.Column(db.Text)
    
    # Relationships
    applicant = db.relationship('User', foreign_keys=[applicant_id], backref='scholarship_applications')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('scholarship_id', 'applicant_id', name='unique_scholarship_applicant'),)
    
    @property
    def is_reviewed(self):
        return self.reviewed_at is not None
    
    def to_dict(self):
        return {
            'id': self.id,
            'scholarship_id': self.scholarship_id,
            'scholarship_name': self.scholarship.name if self.scholarship else None,
            'applicant_id': self.applicant_id,
            'applicant_name': self.applicant.full_name if self.applicant else None,
            'application_data': self.application_data,
            'documents': self.documents,
            'status': self.status,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'reviewed_by': self.reviewed_by,
            'reviewer_name': self.reviewer.full_name if self.reviewer else None,
            'review_notes': self.review_notes,
            'is_reviewed': self.is_reviewed
        }

