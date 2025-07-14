from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.community import Project, Donation, ProjectExpense, PaymentTransaction
from datetime import datetime

projects_bp = Blueprint('projects', __name__)

# =============================================
# PROJECT ROUTES
# =============================================

@projects_bp.route('/', methods=['GET'])
def get_projects():
    """Get all active projects"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category = request.args.get('category', '')
        status = request.args.get('status', 'active')
        featured_only = request.args.get('featured_only', False, type=bool)
        
        query = Project.query.filter_by(status=status)
        
        if category:
            query = query.filter_by(category=category)
        
        if featured_only:
            query = query.filter_by(is_featured=True)
        
        projects = query.order_by(Project.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'projects': [project.to_dict() for project in projects.items],
            'total': projects.total,
            'pages': projects.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Get specific project details"""
    try:
        project = Project.query.get_or_404(project_id)
        return jsonify({
            'project': project.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/', methods=['POST'])
@jwt_required()
def create_project():
    """Create a new project"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        project = Project(
            title=data['title'],
            description=data.get('description'),
            category=data.get('category'),
            manager_id=current_user_id,
            target_amount=data.get('target_amount'),
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data.get('start_date') else None,
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None,
            location_address=data.get('location_address'),
            location_coordinates=data.get('location_coordinates'),
            images=data.get('images', []),
            documents=data.get('documents', [])
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            'message': 'Project created successfully',
            'project': project.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    """Update project (manager only)"""
    try:
        current_user_id = get_jwt_identity()
        project = Project.query.get_or_404(project_id)
        
        if project.manager_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = [
            'title', 'description', 'category', 'target_amount',
            'start_date', 'end_date', 'location_address', 'location_coordinates',
            'images', 'documents', 'status'
        ]
        
        for field in allowed_fields:
            if field in data:
                if field in ['start_date', 'end_date'] and data[field]:
                    setattr(project, field, datetime.strptime(data[field], '%Y-%m-%d').date())
                else:
                    setattr(project, field, data[field])
        
        project.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Project updated successfully',
            'project': project.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/my-projects', methods=['GET'])
@jwt_required()
def get_my_projects():
    """Get current user's managed projects"""
    try:
        current_user_id = get_jwt_identity()
        projects = Project.query.filter_by(manager_id=current_user_id).all()
        
        return jsonify({
            'projects': [project.to_dict() for project in projects]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================
# DONATION ROUTES
# =============================================

@projects_bp.route('/<int:project_id>/donate', methods=['POST'])
@jwt_required()
def donate_to_project(project_id):
    """Make a donation to a project"""
    try:
        current_user_id = get_jwt_identity()
        project = Project.query.get_or_404(project_id)
        
        if project.status != 'active':
            return jsonify({'error': 'Project is not accepting donations'}), 400
        
        data = request.get_json()
        
        donation = Donation(
            donor_id=current_user_id,
            project_id=project_id,
            amount=data['amount'],
            currency=data.get('currency', 'BDT'),
            donation_type=data.get('donation_type', 'one_time'),
            frequency=data.get('frequency'),
            is_anonymous=data.get('is_anonymous', False),
            message=data.get('message'),
            payment_method=data.get('payment_method')
        )
        
        db.session.add(donation)
        db.session.flush()  # Get the donation ID
        
        # Create payment transaction
        transaction = PaymentTransaction(
            donation_id=donation.id,
            transaction_type='donation',
            amount=donation.amount,
            currency=donation.currency,
            payment_gateway=data.get('payment_gateway', 'manual'),
            status='pending'
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'message': 'Donation initiated successfully',
            'donation': donation.to_dict(),
            'transaction': transaction.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/donations/<int:donation_id>/confirm', methods=['POST'])
@jwt_required()
def confirm_donation(donation_id):
    """Confirm a donation payment (simplified)"""
    try:
        current_user_id = get_jwt_identity()
        donation = Donation.query.get_or_404(donation_id)
        
        if donation.donor_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # In a real implementation, you would verify payment with the gateway
        # For now, we'll just mark as completed
        donation.payment_status = 'completed'
        donation.processed_at = datetime.utcnow()
        
        # Update project raised amount
        project = donation.project
        if project:
            project.raised_amount = (project.raised_amount or 0) + donation.amount
        
        # Update transaction status
        for transaction in donation.transactions:
            transaction.status = 'success'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Donation confirmed successfully',
            'donation': donation.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/<int:project_id>/donations', methods=['GET'])
def get_project_donations(project_id):
    """Get donations for a project"""
    try:
        project = Project.query.get_or_404(project_id)
        
        # Only show non-anonymous donations or basic stats
        donations = Donation.query.filter_by(
            project_id=project_id, 
            payment_status='completed',
            is_anonymous=False
        ).order_by(Donation.donated_at.desc()).limit(50).all()
        
        total_donations = Donation.query.filter_by(
            project_id=project_id, 
            payment_status='completed'
        ).count()
        
        return jsonify({
            'donations': [donation.to_dict() for donation in donations],
            'total_donations': total_donations,
            'total_amount': float(project.raised_amount) if project.raised_amount else 0
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/my-donations', methods=['GET'])
@jwt_required()
def get_my_donations():
    """Get current user's donations"""
    try:
        current_user_id = get_jwt_identity()
        donations = Donation.query.filter_by(donor_id=current_user_id).order_by(
            Donation.donated_at.desc()
        ).all()
        
        return jsonify({
            'donations': [donation.to_dict() for donation in donations]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================
# PROJECT EXPENSE ROUTES
# =============================================

@projects_bp.route('/<int:project_id>/expenses', methods=['GET'])
@jwt_required()
def get_project_expenses(project_id):
    """Get expenses for a project (manager only)"""
    try:
        current_user_id = get_jwt_identity()
        project = Project.query.get_or_404(project_id)
        
        if project.manager_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        expenses = ProjectExpense.query.filter_by(project_id=project_id).order_by(
            ProjectExpense.expense_date.desc()
        ).all()
        
        return jsonify({
            'expenses': [expense.to_dict() for expense in expenses]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/<int:project_id>/expenses', methods=['POST'])
@jwt_required()
def create_project_expense(project_id):
    """Create a project expense (manager only)"""
    try:
        current_user_id = get_jwt_identity()
        project = Project.query.get_or_404(project_id)
        
        if project.manager_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        
        expense = ProjectExpense(
            project_id=project_id,
            category=data.get('category'),
            description=data.get('description'),
            amount=data['amount'],
            expense_date=datetime.strptime(data['expense_date'], '%Y-%m-%d').date() if data.get('expense_date') else datetime.utcnow().date(),
            receipt_url=data.get('receipt_url'),
            created_by=current_user_id
        )
        
        db.session.add(expense)
        db.session.commit()
        
        return jsonify({
            'message': 'Expense recorded successfully',
            'expense': expense.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/expenses/<int:expense_id>/approve', methods=['POST'])
@jwt_required()
def approve_expense(expense_id):
    """Approve a project expense (admin only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.has_permission('project_management'):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        expense = ProjectExpense.query.get_or_404(expense_id)
        
        expense.approved_by = current_user_id
        expense.approved_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Expense approved successfully',
            'expense': expense.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# =============================================
# PROJECT STATISTICS ROUTES
# =============================================

@projects_bp.route('/statistics', methods=['GET'])
def get_project_statistics():
    """Get overall project statistics"""
    try:
        total_projects = Project.query.count()
        active_projects = Project.query.filter_by(status='active').count()
        completed_projects = Project.query.filter_by(status='completed').count()
        
        total_donations = db.session.query(db.func.sum(Donation.amount)).filter_by(
            payment_status='completed'
        ).scalar() or 0
        
        total_donors = db.session.query(db.func.count(db.func.distinct(Donation.donor_id))).filter_by(
            payment_status='completed'
        ).scalar() or 0
        
        return jsonify({
            'total_projects': total_projects,
            'active_projects': active_projects,
            'completed_projects': completed_projects,
            'total_donations': float(total_donations),
            'total_donors': total_donors
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

