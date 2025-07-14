from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.community import *
from datetime import datetime

community_bp = Blueprint('community', __name__)

# =============================================
# FORUM ROUTES
# =============================================

@community_bp.route('/forums', methods=['GET'])
def get_forums():
    """Get all active forums"""
    try:
        forums = Forum.query.filter_by(is_active=True, is_public=True).all()
        return jsonify({
            'forums': [forum.to_dict() for forum in forums]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@community_bp.route('/forums/<int:forum_id>/posts', methods=['GET'])
def get_forum_posts(forum_id):
    """Get posts in a forum"""
    try:
        forum = Forum.query.get_or_404(forum_id)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        posts = ForumPost.query.filter_by(forum_id=forum_id).order_by(
            ForumPost.is_pinned.desc(), ForumPost.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'posts': [post.to_dict() for post in posts.items],
            'total': posts.total,
            'pages': posts.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@community_bp.route('/forums/<int:forum_id>/posts', methods=['POST'])
@jwt_required()
def create_forum_post(forum_id):
    """Create a new forum post"""
    try:
        current_user_id = get_jwt_identity()
        forum = Forum.query.get_or_404(forum_id)
        
        data = request.get_json()
        
        post = ForumPost(
            forum_id=forum_id,
            author_id=current_user_id,
            title=data['title'],
            content=data.get('content')
        )
        
        db.session.add(post)
        db.session.commit()
        
        return jsonify({
            'message': 'Post created successfully',
            'post': post.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@community_bp.route('/posts/<int:post_id>/replies', methods=['GET'])
def get_post_replies(post_id):
    """Get replies to a forum post"""
    try:
        post = ForumPost.query.get_or_404(post_id)
        replies = ForumReply.query.filter_by(post_id=post_id).order_by(ForumReply.created_at.asc()).all()
        
        return jsonify({
            'replies': [reply.to_dict() for reply in replies]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@community_bp.route('/posts/<int:post_id>/replies', methods=['POST'])
@jwt_required()
def create_post_reply(post_id):
    """Reply to a forum post"""
    try:
        current_user_id = get_jwt_identity()
        post = ForumPost.query.get_or_404(post_id)
        
        if post.is_locked:
            return jsonify({'error': 'This post is locked'}), 400
        
        data = request.get_json()
        
        reply = ForumReply(
            post_id=post_id,
            author_id=current_user_id,
            content=data['content'],
            parent_reply_id=data.get('parent_reply_id')
        )
        
        db.session.add(reply)
        db.session.commit()
        
        return jsonify({
            'message': 'Reply posted successfully',
            'reply': reply.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# =============================================
# EVENT ROUTES
# =============================================

@community_bp.route('/events', methods=['GET'])
def get_events():
    """Get all public events"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        event_type = request.args.get('event_type', '')
        location = request.args.get('location', '')
        upcoming_only = request.args.get('upcoming_only', True, type=bool)
        
        query = Event.query.filter_by(is_active=True, is_public=True)
        
        if event_type:
            query = query.filter_by(event_type=event_type)
        
        if location:
            query = query.filter(Event.location_address.ilike(f'%{location}%'))
        
        if upcoming_only:
            query = query.filter(Event.start_datetime >= datetime.utcnow())
        
        events = query.order_by(Event.start_datetime.asc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'events': [event.to_dict() for event in events.items],
            'total': events.total,
            'pages': events.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@community_bp.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Get specific event details"""
    try:
        event = Event.query.get_or_404(event_id)
        return jsonify({
            'event': event.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@community_bp.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    """Create a new event"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        event = Event(
            title=data['title'],
            description=data.get('description'),
            event_type=data.get('event_type'),
            organizer_id=current_user_id,
            start_datetime=datetime.strptime(data['start_datetime'], '%Y-%m-%d %H:%M'),
            end_datetime=datetime.strptime(data['end_datetime'], '%Y-%m-%d %H:%M') if data.get('end_datetime') else None,
            location_address=data.get('location_address'),
            location_coordinates=data.get('location_coordinates'),
            is_online=data.get('is_online', False),
            meeting_link=data.get('meeting_link'),
            capacity=data.get('capacity'),
            registration_fee=data.get('registration_fee', 0),
            registration_deadline=datetime.strptime(data['registration_deadline'], '%Y-%m-%d %H:%M') if data.get('registration_deadline') else None,
            is_public=data.get('is_public', True)
        )
        
        db.session.add(event)
        db.session.commit()
        
        return jsonify({
            'message': 'Event created successfully',
            'event': event.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@community_bp.route('/events/<int:event_id>/register', methods=['POST'])
@jwt_required()
def register_for_event(event_id):
    """Register for an event"""
    try:
        current_user_id = get_jwt_identity()
        event = Event.query.get_or_404(event_id)
        
        if not event.is_registration_open:
            return jsonify({'error': 'Registration is closed for this event'}), 400
        
        # Check if already registered
        existing_registration = EventRegistration.query.filter_by(
            event_id=event_id, participant_id=current_user_id
        ).first()
        
        if existing_registration:
            return jsonify({'error': 'Already registered for this event'}), 400
        
        data = request.get_json()
        
        registration = EventRegistration(
            event_id=event_id,
            participant_id=current_user_id,
            special_requirements=data.get('special_requirements')
        )
        
        db.session.add(registration)
        db.session.commit()
        
        return jsonify({
            'message': 'Registered for event successfully',
            'registration': registration.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@community_bp.route('/my-event-registrations', methods=['GET'])
@jwt_required()
def get_my_event_registrations():
    """Get current user's event registrations"""
    try:
        current_user_id = get_jwt_identity()
        registrations = EventRegistration.query.filter_by(participant_id=current_user_id).all()
        
        return jsonify({
            'registrations': [registration.to_dict() for registration in registrations]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================
# VOLUNTEER OPPORTUNITY ROUTES
# =============================================

@community_bp.route('/volunteer-opportunities', methods=['GET'])
def get_volunteer_opportunities():
    """Get all active volunteer opportunities"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category = request.args.get('category', '')
        location = request.args.get('location', '')
        is_remote = request.args.get('is_remote', type=bool)
        
        query = VolunteerOpportunity.query.filter_by(is_active=True)
        
        if category:
            query = query.filter_by(category=category)
        
        if location:
            query = query.filter(VolunteerOpportunity.location_address.ilike(f'%{location}%'))
        
        if is_remote is not None:
            query = query.filter_by(is_remote=is_remote)
        
        opportunities = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'opportunities': [opp.to_dict() for opp in opportunities.items],
            'total': opportunities.total,
            'pages': opportunities.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@community_bp.route('/volunteer-opportunities/<int:opportunity_id>', methods=['GET'])
def get_volunteer_opportunity(opportunity_id):
    """Get specific volunteer opportunity details"""
    try:
        opportunity = VolunteerOpportunity.query.get_or_404(opportunity_id)
        return jsonify({
            'opportunity': opportunity.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@community_bp.route('/volunteer-opportunities/<int:opportunity_id>/apply', methods=['POST'])
@jwt_required()
def apply_for_volunteer_opportunity(opportunity_id):
    """Apply for a volunteer opportunity"""
    try:
        current_user_id = get_jwt_identity()
        opportunity = VolunteerOpportunity.query.get_or_404(opportunity_id)
        
        if not opportunity.is_application_open:
            return jsonify({'error': 'Application is closed for this opportunity'}), 400
        
        # Check if already applied
        existing_application = VolunteerApplication.query.filter_by(
            opportunity_id=opportunity_id, volunteer_id=current_user_id
        ).first()
        
        if existing_application:
            return jsonify({'error': 'Already applied for this opportunity'}), 400
        
        data = request.get_json()
        
        application = VolunteerApplication(
            opportunity_id=opportunity_id,
            volunteer_id=current_user_id,
            motivation=data.get('motivation'),
            availability=data.get('availability')
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

@community_bp.route('/my-volunteer-applications', methods=['GET'])
@jwt_required()
def get_my_volunteer_applications():
    """Get current user's volunteer applications"""
    try:
        current_user_id = get_jwt_identity()
        applications = VolunteerApplication.query.filter_by(volunteer_id=current_user_id).all()
        
        return jsonify({
            'applications': [application.to_dict() for application in applications]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@community_bp.route('/volunteer-hours', methods=['POST'])
@jwt_required()
def log_volunteer_hours():
    """Log volunteer hours"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        volunteer_hours = VolunteerHours(
            volunteer_id=current_user_id,
            opportunity_id=data.get('opportunity_id'),
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            hours_worked=data['hours_worked'],
            activity_description=data.get('activity_description')
        )
        
        db.session.add(volunteer_hours)
        db.session.commit()
        
        return jsonify({
            'message': 'Volunteer hours logged successfully',
            'volunteer_hours': volunteer_hours.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@community_bp.route('/my-volunteer-hours', methods=['GET'])
@jwt_required()
def get_my_volunteer_hours():
    """Get current user's volunteer hours"""
    try:
        current_user_id = get_jwt_identity()
        volunteer_hours = VolunteerHours.query.filter_by(volunteer_id=current_user_id).all()
        
        total_hours = sum(vh.hours_worked for vh in volunteer_hours if vh.hours_worked)
        
        return jsonify({
            'volunteer_hours': [vh.to_dict() for vh in volunteer_hours],
            'total_hours': float(total_hours) if total_hours else 0
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

