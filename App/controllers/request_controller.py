from App.database import db
from App.models import Student


def create_request(student_id, hours):
    """
    Resolve IDs to objects and delegate request creation to the Student model.
    """
    student = db.session.get(Student, student_id)
    if not student:
        return None, "Student not found"

    request = student.request_hours_confirmation(hours)
    return request, None
