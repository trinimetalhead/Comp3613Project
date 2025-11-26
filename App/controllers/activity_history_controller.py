from App.database import db
from App.models import Student, ActivityHistory

def get_student_activity_history(student_id):
    """
    Retrieves the complete activity history for a student.
    
    Args:
        student_id: The ID of the student
        
    Returns:
        list: List of ActivityHistory objects sorted by timestamp (newest first)
        
    Raises:
        ValueError: If student not found
    """
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    activities = db.session.scalars(
        db.select(ActivityHistory)
        .filter_by(student_id=student_id)
        .order_by(ActivityHistory.timestamp.desc())
    ).all()
    
    return activities

def get_activity_history_json(student_id):
    """
    Retrieves activity history in JSON format.
    
    Args:
        student_id: The ID of the student
        
    Returns:
        list: List of activity history dictionaries
    """
    activities = get_student_activity_history(student_id)
    return [activity.get_json() for activity in activities]

def get_activity_by_type(student_id, activity_type):
    """
    Retrieves activity history filtered by activity type.
    
    Args:
        student_id: The ID of the student
        activity_type: The type of activity ('hours_earned', 'milestone', 'accolade', 'request_created')
        
    Returns:
        list: List of ActivityHistory objects of the specified type
    """
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    activities = db.session.scalars(
        db.select(ActivityHistory)
        .filter_by(student_id=student_id, activity_type=activity_type)
        .order_by(ActivityHistory.timestamp.desc())
    ).all()
    
    return activities

def get_earned_hours_history(student_id):
    """
    Retrieves all hours earned activities for a student.
    
    Args:
        student_id: The ID of the student
        
    Returns:
        list: List of hours_earned ActivityHistory objects
    """
    return get_activity_by_type(student_id, 'hours_earned')

def get_milestones_achieved(student_id):
    """
    Retrieves all milestones achieved by a student.
    
    Args:
        student_id: The ID of the student
        
    Returns:
        list: List of milestone ActivityHistory objects
    """
    return get_activity_by_type(student_id, 'milestone')

def get_accolades_earned(student_id):
    """
    Retrieves all accolades earned by a student.
    
    Args:
        student_id: The ID of the student
        
    Returns:
        list: List of accolade ActivityHistory objects
    """
    return get_activity_by_type(student_id, 'accolade')

def get_requests_submitted(student_id):
    """
    Retrieves all request submissions by a student.
    
    Args:
        student_id: The ID of the student
        
    Returns:
        list: List of request_created ActivityHistory objects
    """
    return get_activity_by_type(student_id, 'request_created')

def get_activity_summary(student_id):
    """
    Retrieves a comprehensive summary of a student's activity.
    
    Args:
        student_id: The ID of the student
        
    Returns:
        dict: Summary containing activity counts, milestones, accolades, and recent activity
    """
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    all_activities = get_student_activity_history(student_id)
    
    # Count activities by type
    hours_earned = get_earned_hours_history(student_id)
    milestones = get_milestones_achieved(student_id)
    accolades = get_accolades_earned(student_id)
    requests = get_requests_submitted(student_id)
    
    # Calculate total hours
    total_hours = sum(lh.hours for lh in student.loggedhours if lh.status == 'approved')
    
    return {
        'student_id': student_id,
        'student_name': student.username,
        'total_approved_hours': total_hours,
        'activity_counts': {
            'hours_earned': len(hours_earned),
            'milestones_achieved': len(milestones),
            'accolades_earned': len(accolades),
            'requests_submitted': len(requests)
        },
        'current_accolades': student.accolades(),
        'recent_activities': [activity.get_json() for activity in all_activities[:10]],  # Last 10 activities
        'milestones': [m.get_json() for m in milestones],
        'accolades': [a.get_json() for a in accolades]
    }
