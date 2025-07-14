from src.models.user import db
from datetime import datetime

# =============================================
# COMMUNITY FEATURES MODELS
# =============================================

class Forum(db.Model):
    __tablename__ = 'forums'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    moderator_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    is_public = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    moderator = db.relationship('User', backref='moderated_forums')
    posts = db.relationship('ForumPost', backref='forum', cascade='all, delete-orphan')
    
    @property
    def post_count(self):
        return len(self.posts)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'moderator_id': self.moderator_id,
            'moderator_name': self.moderator.full_name if self.moderator else None,
            'is_public': self.is_public,
            'is_active': self.is_active,
            'post_count': self.post_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ForumPost(db.Model):
    __tablename__ = 'forum_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    forum_id = db.Column(db.Integer, db.ForeignKey('forums.id'), nullable=False)
    author_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    is_pinned = db.Column(db.Boolean, default=False)
    is_locked = db.Column(db.Boolean, default=False)
    views_count = db.Column(db.Integer, default=0)
    likes_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    author = db.relationship('User', backref='forum_posts')
    replies = db.relationship('ForumReply', backref='post', cascade='all, delete-orphan')
    
    @property
    def reply_count(self):
        return len(self.replies)
    
    def to_dict(self):
        return {
            'id': self.id,
            'forum_id': self.forum_id,
            'forum_name': self.forum.name if self.forum else None,
            'author_id': self.author_id,
            'author_name': self.author.full_name if self.author else None,
            'title': self.title,
            'content': self.content,
            'is_pinned': self.is_pinned,
            'is_locked': self.is_locked,
            'views_count': self.views_count,
            'likes_count': self.likes_count,
            'reply_count': self.reply_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ForumReply(db.Model):
    __tablename__ = 'forum_replies'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id'), nullable=False)
    author_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)
    parent_reply_id = db.Column(db.Integer, db.ForeignKey('forum_replies.id'))
    likes_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    author = db.relationship('User', backref='forum_replies')
    parent_reply = db.relationship('ForumReply', remote_side=[id], backref='child_replies')
    
    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'author_id': self.author_id,
            'author_name': self.author.full_name if self.author else None,
            'content': self.content,
            'parent_reply_id': self.parent_reply_id,
            'likes_count': self.likes_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50))  # workshop, seminar, camp, fundraiser
    organizer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    start_datetime = db.Column(db.DateTime)
    end_datetime = db.Column(db.DateTime)
    location_address = db.Column(db.Text)
    location_coordinates = db.Column(db.String(100))  # "lat,lng" format
    is_online = db.Column(db.Boolean, default=False)
    meeting_link = db.Column(db.Text)
    capacity = db.Column(db.Integer)
    registration_fee = db.Column(db.Numeric(8, 2), default=0)
    registration_deadline = db.Column(db.DateTime)
    is_public = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    organizer = db.relationship('User', backref='organized_events')
    registrations = db.relationship('EventRegistration', backref='event', cascade='all, delete-orphan')
    
    @property
    def registration_count(self):
        return len(self.registrations)
    
    @property
    def is_registration_open(self):
        if self.capacity and self.registration_count >= self.capacity:
            return False
        if self.registration_deadline and self.registration_deadline < datetime.utcnow():
            return False
        return self.is_active
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'event_type': self.event_type,
            'organizer_id': self.organizer_id,
            'organizer_name': self.organizer.full_name if self.organizer else None,
            'start_datetime': self.start_datetime.isoformat() if self.start_datetime else None,
            'end_datetime': self.end_datetime.isoformat() if self.end_datetime else None,
            'location_address': self.location_address,
            'location_coordinates': self.location_coordinates,
            'is_online': self.is_online,
            'meeting_link': self.meeting_link,
            'capacity': self.capacity,
            'registration_count': self.registration_count,
            'registration_fee': float(self.registration_fee) if self.registration_fee else 0,
            'registration_deadline': self.registration_deadline.isoformat() if self.registration_deadline else None,
            'is_public': self.is_public,
            'is_active': self.is_active,
            'is_registration_open': self.is_registration_open,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class EventRegistration(db.Model):
    __tablename__ = 'event_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    participant_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    attendance_status = db.Column(db.String(20), default='registered')  # registered, attended, absent
    payment_status = db.Column(db.String(20), default='pending')
    special_requirements = db.Column(db.Text)
    
    # Relationships
    participant = db.relationship('User', backref='event_registrations')
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('event_id', 'participant_id', name='unique_event_participant'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'event_title': self.event.title if self.event else None,
            'participant_id': self.participant_id,
            'participant_name': self.participant.full_name if self.participant else None,
            'registration_date': self.registration_date.isoformat() if self.registration_date else None,
            'attendance_status': self.attendance_status,
            'payment_status': self.payment_status,
            'special_requirements': self.special_requirements
        }

class VolunteerOpportunity(db.Model):
    __tablename__ = 'volunteer_opportunities'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    organization_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(100))  # education, healthcare, environment, disaster_relief
    skills_required = db.Column(db.JSON)  # Array of skills
    time_commitment = db.Column(db.String(100))
    location_address = db.Column(db.Text)
    location_coordinates = db.Column(db.String(100))  # "lat,lng" format
    is_remote = db.Column(db.Boolean, default=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    volunteers_needed = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    organization = db.relationship('User', backref='volunteer_opportunities')
    applications = db.relationship('VolunteerApplication', backref='opportunity', cascade='all, delete-orphan')
    
    @property
    def application_count(self):
        return len(self.applications)
    
    @property
    def is_application_open(self):
        if self.volunteers_needed and self.application_count >= self.volunteers_needed:
            return False
        if self.end_date and self.end_date < datetime.utcnow().date():
            return False
        return self.is_active
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'organization_id': self.organization_id,
            'organization_name': self.organization.full_name if self.organization else None,
            'category': self.category,
            'skills_required': self.skills_required,
            'time_commitment': self.time_commitment,
            'location_address': self.location_address,
            'location_coordinates': self.location_coordinates,
            'is_remote': self.is_remote,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'volunteers_needed': self.volunteers_needed,
            'application_count': self.application_count,
            'is_active': self.is_active,
            'is_application_open': self.is_application_open,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class VolunteerApplication(db.Model):
    __tablename__ = 'volunteer_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('volunteer_opportunities.id'), nullable=False)
    volunteer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    motivation = db.Column(db.Text)
    availability = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    reviewed_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    
    # Relationships
    volunteer = db.relationship('User', foreign_keys=[volunteer_id], backref='volunteer_applications')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('opportunity_id', 'volunteer_id', name='unique_opportunity_volunteer'),)
    
    @property
    def is_reviewed(self):
        return self.reviewed_at is not None
    
    def to_dict(self):
        return {
            'id': self.id,
            'opportunity_id': self.opportunity_id,
            'opportunity_title': self.opportunity.title if self.opportunity else None,
            'volunteer_id': self.volunteer_id,
            'volunteer_name': self.volunteer.full_name if self.volunteer else None,
            'motivation': self.motivation,
            'availability': self.availability,
            'status': self.status,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'reviewed_by': self.reviewed_by,
            'reviewer_name': self.reviewer.full_name if self.reviewer else None,
            'is_reviewed': self.is_reviewed
        }

class VolunteerHours(db.Model):
    __tablename__ = 'volunteer_hours'
    
    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('volunteer_opportunities.id'))
    date = db.Column(db.Date)
    hours_worked = db.Column(db.Numeric(4, 2))
    activity_description = db.Column(db.Text)
    verified_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    verified_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    volunteer = db.relationship('User', foreign_keys=[volunteer_id], backref='volunteer_hours')
    opportunity = db.relationship('VolunteerOpportunity', backref='volunteer_hours')
    verifier = db.relationship('User', foreign_keys=[verified_by])
    
    @property
    def is_verified(self):
        return self.verified_at is not None
    
    def to_dict(self):
        return {
            'id': self.id,
            'volunteer_id': self.volunteer_id,
            'volunteer_name': self.volunteer.full_name if self.volunteer else None,
            'opportunity_id': self.opportunity_id,
            'opportunity_title': self.opportunity.title if self.opportunity else None,
            'date': self.date.isoformat() if self.date else None,
            'hours_worked': float(self.hours_worked) if self.hours_worked else None,
            'activity_description': self.activity_description,
            'verified_by': self.verified_by,
            'verifier_name': self.verifier.full_name if self.verifier else None,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# =============================================
# PROJECTS AND DONATIONS MODELS
# =============================================

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))  # education, healthcare, agriculture, disaster_relief
    manager_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    target_amount = db.Column(db.Numeric(15, 2))
    raised_amount = db.Column(db.Numeric(15, 2), default=0)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    location_address = db.Column(db.Text)
    location_coordinates = db.Column(db.String(100))  # "lat,lng" format
    images = db.Column(db.JSON)  # Array of image URLs
    documents = db.Column(db.JSON)  # Array of document URLs
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled, on_hold
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    manager = db.relationship('User', backref='managed_projects')
    donations = db.relationship('Donation', backref='project', cascade='all, delete-orphan')
    expenses = db.relationship('ProjectExpense', backref='project', cascade='all, delete-orphan')
    
    @property
    def donation_count(self):
        return len(self.donations)
    
    @property
    def progress_percentage(self):
        if self.target_amount and self.raised_amount:
            return min((self.raised_amount / self.target_amount) * 100, 100)
        return 0
    
    @property
    def total_expenses(self):
        return sum(expense.amount for expense in self.expenses if expense.approved_at)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'manager_id': self.manager_id,
            'manager_name': self.manager.full_name if self.manager else None,
            'target_amount': float(self.target_amount) if self.target_amount else None,
            'raised_amount': float(self.raised_amount) if self.raised_amount else 0,
            'progress_percentage': self.progress_percentage,
            'donation_count': self.donation_count,
            'total_expenses': float(self.total_expenses) if self.total_expenses else 0,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'location_address': self.location_address,
            'location_coordinates': self.location_coordinates,
            'images': self.images,
            'documents': self.documents,
            'status': self.status,
            'is_featured': self.is_featured,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Donation(db.Model):
    __tablename__ = 'donations'
    
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    currency = db.Column(db.String(3), default='BDT')
    donation_type = db.Column(db.String(20))  # one_time, recurring
    frequency = db.Column(db.String(20))  # monthly, quarterly, yearly (for recurring)
    is_anonymous = db.Column(db.Boolean, default=False)
    message = db.Column(db.Text)
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    payment_status = db.Column(db.String(20), default='pending')  # pending, completed, failed, refunded
    tax_deductible = db.Column(db.Boolean, default=True)
    receipt_url = db.Column(db.Text)
    donated_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    
    # Relationships
    donor = db.relationship('User', backref='donations')
    transactions = db.relationship('PaymentTransaction', backref='donation', cascade='all, delete-orphan')
    
    @property
    def is_processed(self):
        return self.payment_status == 'completed' and self.processed_at is not None
    
    def to_dict(self):
        return {
            'id': self.id,
            'donor_id': self.donor_id,
            'donor_name': self.donor.full_name if self.donor and not self.is_anonymous else 'Anonymous',
            'project_id': self.project_id,
            'project_title': self.project.title if self.project else None,
            'amount': float(self.amount) if self.amount else None,
            'currency': self.currency,
            'donation_type': self.donation_type,
            'frequency': self.frequency,
            'is_anonymous': self.is_anonymous,
            'message': self.message,
            'payment_method': self.payment_method,
            'transaction_id': self.transaction_id,
            'payment_status': self.payment_status,
            'tax_deductible': self.tax_deductible,
            'receipt_url': self.receipt_url,
            'donated_at': self.donated_at.isoformat() if self.donated_at else None,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None,
            'is_processed': self.is_processed
        }

class PaymentTransaction(db.Model):
    __tablename__ = 'payment_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    donation_id = db.Column(db.Integer, db.ForeignKey('donations.id'))
    transaction_type = db.Column(db.String(20))  # donation, refund, fee
    amount = db.Column(db.Numeric(12, 2))
    currency = db.Column(db.String(3), default='BDT')
    payment_gateway = db.Column(db.String(50))
    gateway_transaction_id = db.Column(db.String(100))
    gateway_response = db.Column(db.JSON)
    status = db.Column(db.String(20))  # pending, success, failed, cancelled
    processed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'donation_id': self.donation_id,
            'transaction_type': self.transaction_type,
            'amount': float(self.amount) if self.amount else None,
            'currency': self.currency,
            'payment_gateway': self.payment_gateway,
            'gateway_transaction_id': self.gateway_transaction_id,
            'gateway_response': self.gateway_response,
            'status': self.status,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None
        }

class ProjectExpense(db.Model):
    __tablename__ = 'project_expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    amount = db.Column(db.Numeric(12, 2))
    expense_date = db.Column(db.Date)
    receipt_url = db.Column(db.Text)
    approved_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    approved_at = db.Column(db.DateTime)
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    approver = db.relationship('User', foreign_keys=[approved_by])
    creator = db.relationship('User', foreign_keys=[created_by])
    
    @property
    def is_approved(self):
        return self.approved_at is not None
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'project_title': self.project.title if self.project else None,
            'category': self.category,
            'description': self.description,
            'amount': float(self.amount) if self.amount else None,
            'expense_date': self.expense_date.isoformat() if self.expense_date else None,
            'receipt_url': self.receipt_url,
            'approved_by': self.approved_by,
            'approver_name': self.approver.full_name if self.approver else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'created_by': self.created_by,
            'creator_name': self.creator.full_name if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_approved': self.is_approved
        }

