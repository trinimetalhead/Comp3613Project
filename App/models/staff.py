from App.database import db
from .user import User
from sqlalchemy.exc import IntegrityError

class Staff(User):

    __tablename__ = "staff"
    staff_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
    
    #relationaship to LoggedHours
    loggedhours = db.relationship('LoggedHours', backref='staff', lazy=True, cascade="all, delete-orphan")

   #Inheritance, Staff is a child of User
    __mapper_args__ = {
        "polymorphic_identity": "staff"
    }
    #calls parent constructor
    def __init__(self, username, email, password):
       super().__init__(username, email, password, role="staff")

    def __repr__(self):
        
        return f"[Staff ID= {str(self.staff_id):<3} Name= {self.username:<10} Email= {self.email}]"
    
    def get_json(self):
        return{
            'staff_id': self.staff_id,
            'username': self.username,
            'email': self.email
        }
    
    # Method to create a new staff member
    def create_staff(username, email, password):
        if not username or not username.strip():
            return print("Username cannot be empty")
        if not email or not email.strip():
            return print("Email cannot be empty")
        if not password or not password.strip():
            return print("Password cannot be empty")
        try:
            newstaff = Staff(username=username, email=email, password=password)
            db.session.add(newstaff)
            db.session.commit()
            return newstaff
        except IntegrityError:
            db.session.rollback()
            return None    

    # Method for staff to approve or deny requests
    def approve_request(self, request):
        from App.models import LoggedHours
        if request.status != 'pending':
            return None
        # Mark request as approved
        request.status = 'approved'
        # Create a LoggedHours entry
        logged = LoggedHours(student_id=request.student_id, staff_id=self.staff_id, hours=request.hours, status='approved')
        db.session.add(logged)
        db.session.commit()
        
        # Encapsulated notification for approved hours
        logged.notify_approved()

        return logged
    
    #Method to deny a request
    def deny_request(self, request):
        if request.status != 'pending':
            return False
        request.status = 'denied'
        db.session.commit()
        # Encapsulated notification for denied request
        request.notify_denied()
        return True
    
    
    