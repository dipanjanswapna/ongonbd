from src.models.user import db
from datetime import datetime

class LoanProduct(db.Model):
    __tablename__ = 'loan_products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    min_amount = db.Column(db.Numeric(12, 2))
    max_amount = db.Column(db.Numeric(12, 2))
    interest_rate = db.Column(db.Numeric(5, 2))
    tenure_months = db.Column(db.Integer)
    eligibility_criteria = db.Column(db.Text)
    required_documents = db.Column(db.JSON)  # Array of required documents
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    applications = db.relationship('LoanApplication', backref='loan_product')
    loans = db.relationship('Loan', backref='loan_product')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'min_amount': float(self.min_amount) if self.min_amount else None,
            'max_amount': float(self.max_amount) if self.max_amount else None,
            'interest_rate': float(self.interest_rate) if self.interest_rate else None,
            'tenure_months': self.tenure_months,
            'eligibility_criteria': self.eligibility_criteria,
            'required_documents': self.required_documents,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class LoanApplication(db.Model):
    __tablename__ = 'loan_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    loan_product_id = db.Column(db.Integer, db.ForeignKey('loan_products.id'))
    requested_amount = db.Column(db.Numeric(12, 2))
    purpose = db.Column(db.Text)
    business_plan = db.Column(db.Text)
    monthly_income = db.Column(db.Numeric(10, 2))
    existing_loans = db.Column(db.Numeric(12, 2))
    collateral_details = db.Column(db.Text)
    guarantor_info = db.Column(db.JSON)
    documents = db.Column(db.JSON)  # Array of document URLs
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, disbursed
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    reviewed_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    review_notes = db.Column(db.Text)
    
    # Relationships
    applicant = db.relationship('User', foreign_keys=[applicant_id], backref='loan_applications')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])
    loan = db.relationship('Loan', backref='application', uselist=False)
    
    @property
    def is_reviewed(self):
        return self.reviewed_at is not None
    
    def to_dict(self):
        return {
            'id': self.id,
            'applicant_id': self.applicant_id,
            'applicant_name': self.applicant.full_name if self.applicant else None,
            'loan_product_id': self.loan_product_id,
            'loan_product_name': self.loan_product.name if self.loan_product else None,
            'requested_amount': float(self.requested_amount) if self.requested_amount else None,
            'purpose': self.purpose,
            'business_plan': self.business_plan,
            'monthly_income': float(self.monthly_income) if self.monthly_income else None,
            'existing_loans': float(self.existing_loans) if self.existing_loans else None,
            'collateral_details': self.collateral_details,
            'guarantor_info': self.guarantor_info,
            'documents': self.documents,
            'status': self.status,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'reviewed_by': self.reviewed_by,
            'reviewer_name': self.reviewer.full_name if self.reviewer else None,
            'review_notes': self.review_notes,
            'is_reviewed': self.is_reviewed
        }

class Loan(db.Model):
    __tablename__ = 'loans'
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('loan_applications.id'), unique=True)
    borrower_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    loan_product_id = db.Column(db.Integer, db.ForeignKey('loan_products.id'))
    principal_amount = db.Column(db.Numeric(12, 2))
    interest_rate = db.Column(db.Numeric(5, 2))
    tenure_months = db.Column(db.Integer)
    monthly_emi = db.Column(db.Numeric(10, 2))
    disbursement_date = db.Column(db.Date)
    maturity_date = db.Column(db.Date)
    outstanding_balance = db.Column(db.Numeric(12, 2))
    status = db.Column(db.String(20), default='active')  # active, closed, defaulted
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    borrower = db.relationship('User', backref='loans')
    payments = db.relationship('LoanPayment', backref='loan', cascade='all, delete-orphan')
    
    @property
    def total_paid(self):
        return sum(payment.amount_paid for payment in self.payments)
    
    @property
    def payment_count(self):
        return len(self.payments)
    
    def to_dict(self):
        return {
            'id': self.id,
            'application_id': self.application_id,
            'borrower_id': self.borrower_id,
            'borrower_name': self.borrower.full_name if self.borrower else None,
            'loan_product_id': self.loan_product_id,
            'loan_product_name': self.loan_product.name if self.loan_product else None,
            'principal_amount': float(self.principal_amount) if self.principal_amount else None,
            'interest_rate': float(self.interest_rate) if self.interest_rate else None,
            'tenure_months': self.tenure_months,
            'monthly_emi': float(self.monthly_emi) if self.monthly_emi else None,
            'disbursement_date': self.disbursement_date.isoformat() if self.disbursement_date else None,
            'maturity_date': self.maturity_date.isoformat() if self.maturity_date else None,
            'outstanding_balance': float(self.outstanding_balance) if self.outstanding_balance else None,
            'total_paid': float(self.total_paid) if self.total_paid else 0,
            'payment_count': self.payment_count,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class LoanPayment(db.Model):
    __tablename__ = 'loan_payments'
    
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.id'), nullable=False)
    payment_date = db.Column(db.Date)
    amount_paid = db.Column(db.Numeric(10, 2))
    principal_component = db.Column(db.Numeric(10, 2))
    interest_component = db.Column(db.Numeric(10, 2))
    payment_method = db.Column(db.String(20))
    transaction_reference = db.Column(db.String(100))
    late_fee = db.Column(db.Numeric(8, 2), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'loan_id': self.loan_id,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'amount_paid': float(self.amount_paid) if self.amount_paid else None,
            'principal_component': float(self.principal_component) if self.principal_component else None,
            'interest_component': float(self.interest_component) if self.interest_component else None,
            'payment_method': self.payment_method,
            'transaction_reference': self.transaction_reference,
            'late_fee': float(self.late_fee) if self.late_fee else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class TrainingProgram(db.Model):
    __tablename__ = 'training_programs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))  # technical, business, soft_skills
    duration_hours = db.Column(db.Integer)
    trainer_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    max_participants = db.Column(db.Integer)
    fee = db.Column(db.Numeric(8, 2), default=0)
    prerequisites = db.Column(db.Text)
    certification_provided = db.Column(db.Boolean, default=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    location_address = db.Column(db.Text)
    is_online = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    trainer = db.relationship('User', backref='training_programs')
    enrollments = db.relationship('TrainingEnrollment', backref='program', cascade='all, delete-orphan')
    
    @property
    def enrollment_count(self):
        return len(self.enrollments)
    
    @property
    def is_enrollment_open(self):
        if self.max_participants and self.enrollment_count >= self.max_participants:
            return False
        if self.end_date and self.end_date < datetime.utcnow().date():
            return False
        return self.is_active
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'duration_hours': self.duration_hours,
            'trainer_id': self.trainer_id,
            'trainer_name': self.trainer.full_name if self.trainer else None,
            'max_participants': self.max_participants,
            'enrollment_count': self.enrollment_count,
            'fee': float(self.fee) if self.fee else 0,
            'prerequisites': self.prerequisites,
            'certification_provided': self.certification_provided,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'location_address': self.location_address,
            'is_online': self.is_online,
            'is_active': self.is_active,
            'is_enrollment_open': self.is_enrollment_open,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class TrainingEnrollment(db.Model):
    __tablename__ = 'training_enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('training_programs.id'), nullable=False)
    participant_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime)
    attendance_percentage = db.Column(db.Numeric(5, 2))
    final_score = db.Column(db.Numeric(5, 2))
    certificate_issued = db.Column(db.Boolean, default=False)
    certificate_url = db.Column(db.Text)
    
    # Relationships
    participant = db.relationship('User', backref='training_enrollments')
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('program_id', 'participant_id', name='unique_program_participant'),)
    
    @property
    def is_completed(self):
        return self.completion_date is not None
    
    def to_dict(self):
        return {
            'id': self.id,
            'program_id': self.program_id,
            'program_name': self.program.name if self.program else None,
            'participant_id': self.participant_id,
            'participant_name': self.participant.full_name if self.participant else None,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'attendance_percentage': float(self.attendance_percentage) if self.attendance_percentage else None,
            'final_score': float(self.final_score) if self.final_score else None,
            'certificate_issued': self.certificate_issued,
            'certificate_url': self.certificate_url,
            'is_completed': self.is_completed
        }

class JobCategory(db.Model):
    __tablename__ = 'job_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('job_categories.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Self-referential relationship for subcategories
    parent = db.relationship('JobCategory', remote_side=[id], backref='subcategories')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'subcategories': [sub.to_dict() for sub in self.subcategories] if self.subcategories else []
        }

class JobPosting(db.Model):
    __tablename__ = 'job_postings'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('job_categories.id'))
    employer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    company_name = db.Column(db.String(255))
    location_address = db.Column(db.Text)
    employment_type = db.Column(db.String(20))  # full_time, part_time, contract, freelance
    experience_required = db.Column(db.String(50))
    skills_required = db.Column(db.JSON)  # Array of skills
    salary_min = db.Column(db.Numeric(10, 2))
    salary_max = db.Column(db.Numeric(10, 2))
    application_deadline = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = db.relationship('JobCategory', backref='job_postings')
    employer = db.relationship('User', backref='job_postings')
    applications = db.relationship('JobApplication', backref='job', cascade='all, delete-orphan')
    
    @property
    def application_count(self):
        return len(self.applications)
    
    @property
    def is_application_open(self):
        if self.application_deadline and self.application_deadline < datetime.utcnow().date():
            return False
        return self.is_active
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'employer_id': self.employer_id,
            'employer_name': self.employer.full_name if self.employer else None,
            'company_name': self.company_name,
            'location_address': self.location_address,
            'employment_type': self.employment_type,
            'experience_required': self.experience_required,
            'skills_required': self.skills_required,
            'salary_min': float(self.salary_min) if self.salary_min else None,
            'salary_max': float(self.salary_max) if self.salary_max else None,
            'application_deadline': self.application_deadline.isoformat() if self.application_deadline else None,
            'application_count': self.application_count,
            'is_active': self.is_active,
            'is_application_open': self.is_application_open,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class JobApplication(db.Model):
    __tablename__ = 'job_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job_postings.id'), nullable=False)
    applicant_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    cover_letter = db.Column(db.Text)
    resume_url = db.Column(db.Text)
    status = db.Column(db.String(20), default='applied')  # applied, shortlisted, interviewed, selected, rejected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applicant = db.relationship('User', backref='job_applications')
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('job_id', 'applicant_id', name='unique_job_applicant'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'job_title': self.job.title if self.job else None,
            'applicant_id': self.applicant_id,
            'applicant_name': self.applicant.full_name if self.applicant else None,
            'cover_letter': self.cover_letter,
            'resume_url': self.resume_url,
            'status': self.status,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

