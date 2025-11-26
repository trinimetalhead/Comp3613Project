from App.database import db
from App.models import Staff, Request


def approve_request(staff_id, request_id):
    """Controller: Resolve IDs to objects and delegate to model"""
    staff = db.session.get(Staff, staff_id)
    request = db.session.get(Request, request_id)
    if not staff or not request:
        return None, "Staff or Request not found"
    return staff.approve_request(request), None


def deny_request(staff_id, request_id):
    staff = db.session.get(Staff, staff_id)
    request = db.session.get(Request, request_id)
    if not staff or not request:
        return None, "Staff or Request not found"
    return staff.deny_request(request), None
from App.database import db
from App.models import User,Staff,Student,Request

def register_staff(name,email,password): #registers a new staff member
    new_staff = Staff.create_staff(name, email, password)
    return new_staff

def fetch_all_requests(): #fetches all pending requests for staff to review
    pending_requests = Request.query.filter_by(status='pending').all()
    if not pending_requests:
        return []
    
    requests_data=[]
    for req in pending_requests:
        student = Student.query.get(req.student_id)
        student_name = student.username if student else "Unknown"
        
        requests_data.append({
            'id': req.id,
            'student_name': student_name,
            'hours': req.hours,
            'status':req.status
        })
    
    return requests_data

def process_request_approval(staff_id, request_id): #staff approves a student's hours request
    staff = Staff.query.get(staff_id)
    if not staff:
        raise ValueError(f"Staff with id {staff_id} not found.")
    
    request = Request.query.get(request_id)
    if not request:
        raise ValueError(f"Request with id {request_id} not found.")
    
    student = Student.query.get(request.student_id)
    name = student.username if student else "Unknown" # should always find student if data integrity is maintained
    logged = staff.approve_request(request)

    return {
        'request': request,
        'student_name': name,
        'staff_name': staff.username,
        'logged_hours': logged
    }

def process_request_denial(staff_id, request_id): #staff denies a student's hours request
    staff = Staff.query.get(staff_id)
    if not staff:
        raise ValueError(f"Staff with id {staff_id} not found.")
    
    request = Request.query.get(request_id)
    if not request:
        raise ValueError(f"Request with id {request_id} not found.")
    
    student = Student.query.get(request.student_id)
    name = student.username if student else "Unknown"
    denied = staff.deny_request(request)
    
    return {
        'request': request,
        'student_name': name,
        'staff_name': staff.username,
        'denial_successful': denied
    }
    
def get_all_staff_json(): #returns all staff members in JSON format
    staff_members = Staff.query.all()
    return [staff.get_json() for staff in staff_members]

