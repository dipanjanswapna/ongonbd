from src.models.user import db
from datetime import datetime

class HealthcareProvider(db.Model):
    __tablename__ = 'healthcare_providers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), unique=True, nullable=False)
    license_number = db.Column(db.String(100), unique=True)
    specialization = db.Column(db.String(100))
    qualifications = db.Column(db.JSON)  # Array of qualifications
    experience_years = db.Column(db.Integer)
    consultation_fee = db.Column(db.Numeric(8, 2))
    availability_schedule = db.Column(db.JSON)  # Schedule data
    is_verified = db.Column(db.Boolean, default=False)
    verified_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    verified_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='healthcare_provider')
    verifier = db.relationship('User', foreign_keys=[verified_by])
    consultations = db.relationship('Consultation', backref='provider', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else None,
            'license_number': self.license_number,
            'specialization': self.specialization,
            'qualifications': self.qualifications,
            'experience_years': self.experience_years,
            'consultation_fee': float(self.consultation_fee) if self.consultation_fee else None,
            'availability_schedule': self.availability_schedule,
            'is_verified': self.is_verified,
            'verified_by': self.verified_by,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), unique=True, nullable=False)
    blood_group = db.Column(db.String(5))
    height_cm = db.Column(db.Integer)
    weight_kg = db.Column(db.Numeric(5, 2))
    allergies = db.Column(db.JSON)  # Array of allergies
    chronic_conditions = db.Column(db.JSON)  # Array of conditions
    emergency_contact_name = db.Column(db.String(255))
    emergency_contact_phone = db.Column(db.String(20))
    insurance_info = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='patient_profile')
    consultations = db.relationship('Consultation', backref='patient', cascade='all, delete-orphan')
    medical_records = db.relationship('MedicalRecord', backref='patient', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else None,
            'blood_group': self.blood_group,
            'height_cm': self.height_cm,
            'weight_kg': float(self.weight_kg) if self.weight_kg else None,
            'allergies': self.allergies,
            'chronic_conditions': self.chronic_conditions,
            'emergency_contact_name': self.emergency_contact_name,
            'emergency_contact_phone': self.emergency_contact_phone,
            'insurance_info': self.insurance_info,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Consultation(db.Model):
    __tablename__ = 'consultations'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('healthcare_providers.id'), nullable=False)
    consultation_type = db.Column(db.String(20))  # online, offline, emergency
    appointment_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    symptoms = db.Column(db.Text)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    follow_up_date = db.Column(db.Date)
    consultation_fee = db.Column(db.Numeric(8, 2))
    payment_status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.user.full_name if self.patient and self.patient.user else None,
            'provider_id': self.provider_id,
            'provider_name': self.provider.user.full_name if self.provider and self.provider.user else None,
            'consultation_type': self.consultation_type,
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'status': self.status,
            'symptoms': self.symptoms,
            'diagnosis': self.diagnosis,
            'prescription': self.prescription,
            'follow_up_date': self.follow_up_date.isoformat() if self.follow_up_date else None,
            'consultation_fee': float(self.consultation_fee) if self.consultation_fee else None,
            'payment_status': self.payment_status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    consultation_id = db.Column(db.Integer, db.ForeignKey('consultations.id'))
    record_type = db.Column(db.String(50))  # diagnosis, prescription, lab_result, imaging
    record_data = db.Column(db.JSON)
    attachments = db.Column(db.JSON)  # Array of URLs to medical documents
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    consultation = db.relationship('Consultation', backref='medical_records')
    creator = db.relationship('User', backref='created_medical_records')
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.user.full_name if self.patient and self.patient.user else None,
            'consultation_id': self.consultation_id,
            'record_type': self.record_type,
            'record_data': self.record_data,
            'attachments': self.attachments,
            'created_by': self.created_by,
            'creator_name': self.creator.full_name if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class MedicalCamp(db.Model):
    __tablename__ = 'medical_camps'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    location_address = db.Column(db.Text)
    location_coordinates = db.Column(db.String(100))  # "lat,lng" format
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    services_offered = db.Column(db.JSON)  # Array of services
    organizer_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    capacity = db.Column(db.Integer)
    registration_fee = db.Column(db.Numeric(8, 2), default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    organizer = db.relationship('User', backref='organized_medical_camps')
    registrations = db.relationship('CampRegistration', backref='camp', cascade='all, delete-orphan')
    
    @property
    def registration_count(self):
        return len(self.registrations)
    
    @property
    def is_registration_open(self):
        if self.capacity and self.registration_count >= self.capacity:
            return False
        if self.end_date and self.end_date < datetime.utcnow().date():
            return False
        return self.is_active
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'location_address': self.location_address,
            'location_coordinates': self.location_coordinates,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'services_offered': self.services_offered,
            'organizer_id': self.organizer_id,
            'organizer_name': self.organizer.full_name if self.organizer else None,
            'capacity': self.capacity,
            'registration_count': self.registration_count,
            'registration_fee': float(self.registration_fee) if self.registration_fee else 0,
            'is_active': self.is_active,
            'is_registration_open': self.is_registration_open,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class CampRegistration(db.Model):
    __tablename__ = 'camp_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    camp_id = db.Column(db.Integer, db.ForeignKey('medical_camps.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    services_requested = db.Column(db.JSON)  # Array of requested services
    special_requirements = db.Column(db.Text)
    attendance_status = db.Column(db.String(20), default='registered')  # registered, attended, absent
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('camp_id', 'patient_id', name='unique_camp_patient'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'camp_id': self.camp_id,
            'camp_name': self.camp.name if self.camp else None,
            'patient_id': self.patient_id,
            'patient_name': self.patient.user.full_name if self.patient and self.patient.user else None,
            'registration_date': self.registration_date.isoformat() if self.registration_date else None,
            'services_requested': self.services_requested,
            'special_requirements': self.special_requirements,
            'attendance_status': self.attendance_status
        }

class BloodDonor(db.Model):
    __tablename__ = 'blood_donors'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), unique=True, nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    last_donation_date = db.Column(db.Date)
    health_status = db.Column(db.String(20), default='eligible')  # eligible, ineligible, temporary_defer
    medical_conditions = db.Column(db.JSON)  # Array of conditions
    is_available = db.Column(db.Boolean, default=True)
    total_donations = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='blood_donor_profile')
    
    @property
    def can_donate(self):
        if not self.is_available or self.health_status != 'eligible':
            return False
        if self.last_donation_date:
            # Check if 3 months have passed since last donation
            from datetime import timedelta
            return (datetime.utcnow().date() - self.last_donation_date) >= timedelta(days=90)
        return True
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else None,
            'blood_group': self.blood_group,
            'last_donation_date': self.last_donation_date.isoformat() if self.last_donation_date else None,
            'health_status': self.health_status,
            'medical_conditions': self.medical_conditions,
            'is_available': self.is_available,
            'can_donate': self.can_donate,
            'total_donations': self.total_donations,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class BloodInventory(db.Model):
    __tablename__ = 'blood_inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    blood_group = db.Column(db.String(5), nullable=False)
    units_available = db.Column(db.Integer, default=0)
    expiry_date = db.Column(db.Date)
    blood_bank_location = db.Column(db.String(255))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def is_expired(self):
        if self.expiry_date:
            return self.expiry_date < datetime.utcnow().date()
        return False
    
    def to_dict(self):
        return {
            'id': self.id,
            'blood_group': self.blood_group,
            'units_available': self.units_available,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'blood_bank_location': self.blood_bank_location,
            'is_expired': self.is_expired,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

class BloodRequest(db.Model):
    __tablename__ = 'blood_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    patient_name = db.Column(db.String(255))
    blood_group = db.Column(db.String(5), nullable=False)
    units_needed = db.Column(db.Integer)
    urgency_level = db.Column(db.String(20))  # low, medium, high, critical
    hospital_name = db.Column(db.String(255))
    hospital_address = db.Column(db.Text)
    contact_phone = db.Column(db.String(20))
    needed_by_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')  # active, fulfilled, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    requester = db.relationship('User', backref='blood_requests')
    
    @property
    def is_urgent(self):
        return self.urgency_level in ['high', 'critical']
    
    def to_dict(self):
        return {
            'id': self.id,
            'requester_id': self.requester_id,
            'requester_name': self.requester.full_name if self.requester else None,
            'patient_name': self.patient_name,
            'blood_group': self.blood_group,
            'units_needed': self.units_needed,
            'urgency_level': self.urgency_level,
            'is_urgent': self.is_urgent,
            'hospital_name': self.hospital_name,
            'hospital_address': self.hospital_address,
            'contact_phone': self.contact_phone,
            'needed_by_date': self.needed_by_date.isoformat() if self.needed_by_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

