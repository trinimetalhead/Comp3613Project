from App.database import db
from App.models import Staff, Request


def approve_request(staff_id, request_id):
    staff = db.session.get(Staff, staff_id)
    request = db.session.get(Request, request_id)

    if not staff:
        return None, "Staff not found"
    if not request:
        return None, "Request not found"

    logged = staff.approve_request(request)
    return logged, None
