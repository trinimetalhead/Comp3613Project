from App.database import db
from App.models import Student


def request_hours(student_id, hours):
    """Controller: Resolve ID to object and delegate to model"""
    student = db.session.get(Student, student_id)
    if not student:
        return None, "Student not found"
    return student.request_hours_confirmation(hours), None


def create_student(username, email, password):
    """Controller: Create a new student and return it"""
    # Basic uniqueness check
    existing = db.session.query(Student).filter_by(username=username).first()
    if existing:
        return None, "User already exists"

    student = Student.create_student(username, email, password)
    return student, None
from App.database import db
from App.models import User,Staff,Student,Request

def register_student(name,email,password):
    new_student=Student.create_student(name,email,password)
    return new_student

def get_approved_hours(student_id): #calculates and returns the total approved hours for a student
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    total_hours = sum(lh.hours for lh in student.loggedhours if lh.status == 'approved')
    return (student.username,total_hours)

def create_hours_request(student_id,hours): #creates a new hours request for a student
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    req = student.request_hours_confirmation(hours)
    return req

def fetch_requests(student_id): #fetch requests for a student
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    return student.requests

def fetch_accolades(student_id): #fetch accolades for a student
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    accolades = student.accolades()
    return accolades

def generate_leaderboard():
    students = Student.query.all()
    leaderboard = []
    for student in students:
        total_hours=sum(lh.hours for lh in student.loggedhours if lh.status == 'approved')

        leaderboard.append({
            'name': student.username,
            'hours': total_hours
        })

    leaderboard.sort(key=lambda item: item['hours'], reverse=True)

    return leaderboard

def get_all_students_json():
    students = Student.query.all()
    return [student.get_json() for student in students]

