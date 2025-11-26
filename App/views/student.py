from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.models import Student
from.index import index_views
from App.controllers.student_controller import get_all_students_json,fetch_accolades,create_hours_request
from App.controllers.activity_history_controller import (
    get_activity_history_json,
    get_activity_summary,
    get_earned_hours_history,
    get_milestones_achieved,
    get_accolades_earned,
    get_requests_submitted
)

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/api/accolades', methods=['GET'])
@jwt_required()
def accolades_report_action():
    user = jwt_current_user
    if user.role != 'student':
        return jsonify(message='Access forbidden: Not a student'), 403
    report = fetch_accolades(user.student_id)
    if not report:
        return jsonify(message='No accolades for this student'), 404
    return jsonify(report)

@student_views.route('/api/make_request', methods=['POST'])
@jwt_required()
def make_request_action():
    user = jwt_current_user
    if user.role != 'student':
        return jsonify(message='Access forbidden: Not a student'), 403
    data = request.json
    if not data or 'hours' not in data:
        return jsonify(message='Invalid request data'), 400
    request_2 = create_hours_request(user.student_id, data['hours'])
    return jsonify(request_2.get_json()), 201

@student_views.route('/api/activity_history', methods=['GET'])
@jwt_required()
def get_activity_history():
    """
    Retrieves the complete activity history for the current student.
    
    Returns:
        200: List of all activities sorted by timestamp (newest first)
        403: If user is not a student
    """
    user = jwt_current_user
    if user.role != 'student':
        return jsonify(message='Access forbidden: Not a student'), 403
    
    try:
        history = get_activity_history_json(user.student_id)
        return jsonify(history), 200
    except ValueError as e:
        return jsonify(message=str(e)), 404

@student_views.route('/api/activity_summary', methods=['GET'])
@jwt_required()
def get_activity_summary_action():
    """
    Retrieves a comprehensive summary of the student's activity.
    
    Includes:
    - Total approved hours
    - Activity counts by type
    - Current accolades
    - Milestones achieved
    - Recent activities
    
    Returns:
        200: Activity summary dictionary
        403: If user is not a student
    """
    user = jwt_current_user
    if user.role != 'student':
        return jsonify(message='Access forbidden: Not a student'), 403
    
    try:
        summary = get_activity_summary(user.student_id)
        return jsonify(summary), 200
    except ValueError as e:
        return jsonify(message=str(e)), 404

@student_views.route('/api/milestones', methods=['GET'])
@jwt_required()
def get_milestones_action():
    """
    Retrieves all milestones achieved by the student.
    
    Returns:
        200: List of milestone activities
        403: If user is not a student
    """
    user = jwt_current_user
    if user.role != 'student':
        return jsonify(message='Access forbidden: Not a student'), 403
    
    try:
        milestones = get_milestones_achieved(user.student_id)
        return jsonify([m.get_json() for m in milestones]), 200
    except ValueError as e:
        return jsonify(message=str(e)), 404

@student_views.route('/api/accolades_history', methods=['GET'])
@jwt_required()
def get_accolades_history_action():
    """
    Retrieves all accolades earned by the student.
    
    Returns:
        200: List of accolade activities
        403: If user is not a student
    """
    user = jwt_current_user
    if user.role != 'student':
        return jsonify(message='Access forbidden: Not a student'), 403
    
    try:
        accolades = get_accolades_earned(user.student_id)
        return jsonify([a.get_json() for a in accolades]), 200
    except ValueError as e:
        return jsonify(message=str(e)), 404

@student_views.route('/api/hours_earned', methods=['GET'])
@jwt_required()
def get_hours_earned_action():
    """
    Retrieves all hours earned activities by the student.
    
    Returns:
        200: List of hours_earned activities
        403: If user is not a student
    """
    user = jwt_current_user
    if user.role != 'student':
        return jsonify(message='Access forbidden: Not a student'), 403
    
    try:
        hours = get_earned_hours_history(user.student_id)
        return jsonify([h.get_json() for h in hours]), 200
    except ValueError as e:
        return jsonify(message=str(e)), 404

@student_views.route('/api/requests_history', methods=['GET'])
@jwt_required()
def get_requests_history_action():
    """
    Retrieves all hour requests submitted by the student.
    
    Returns:
        200: List of request_created activities
        403: If user is not a student
    """
    user = jwt_current_user
    if user.role != 'student':
        return jsonify(message='Access forbidden: Not a student'), 403
    
    try:
        requests = get_requests_submitted(user.student_id)
        return jsonify([r.get_json() for r in requests]), 200
    except ValueError as e:
        return jsonify(message=str(e)), 404