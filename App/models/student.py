from App.database import db
from .user import User
from sqlalchemy.exc import IntegrityError
from .observer import Subject


class Student(User, Subject):

    __tablename__ = "student"
    student_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
    
    #relationship to LoggedHours and Request both One-to-Many
    loggedhours = db.relationship('LoggedHours', backref='student', lazy=True, cascade="all, delete-orphan")
    requests = db.relationship('Request', backref='student', lazy=True, cascade="all, delete-orphan")

    #Inheritance setup
    __mapper_args__ = {
        "polymorphic_identity": "student"
    }
    #calls parent constructor
    def __init__(self, username, email, password):
        Subject.__init__(self)
        super().__init__(username, email, password, role="student")

    def __repr__(self):
        return f"[Student ID= {str(self.student_id):<3}  Name= {self.username:<10} Email= {self.email}]"
    
    def get_json(self):
        return{
            'student_id': self.student_id,
            'username': self.username,
            'email': self.email
        }
    
    # Method to create a new student
    def create_student(username, email, password):
        #non-empty input validation
        if not username or not username.strip():
            return print("Username cannot be empty")
        if not email or not email.strip():
            return print("Email cannot be empty")
        if not password or not password.strip():
            return print("Password cannot be empty")
        #duplicate error handling
        try:
            newstudent = Student(username=username, email=email, password=password)
            db.session.add(newstudent)
            db.session.commit()
            return newstudent
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Duplicate student")

    # Method for student to request hours
    def request_hours_confirmation(self, hours):
        from App.models import Request
        #Invalid Input handling
        if hours is None or hours <= 0 :
            return print("Requested hours must be non-NULL and greater than 0")

        try: 
            hours = float(hours)
        except (TypeError,ValueError):
            return print("Requested hours must be a number")
        
        #Invalid ID handling
        if not self.student_id:
            return print(f"Invalid Student ID <{self.student_id}>")
        
        try:
            request = Request(student_id=self.student_id, hours=hours, status='pending')
            db.session.add(request)
            db.session.commit()
            return request
        except IntegrityError:
            db.session.rollback()
            return None


    # Method to calculate total approved hours and accolades
    def accolades(self):
        # Only count approved logged hours
        total_hours = sum(lh.hours for lh in self.loggedhours if lh.status == 'approved')
        accolades = []
        if total_hours >= 10:
            accolades.append('10 Hours Milestone')
        if total_hours >= 25:
            accolades.append('25 Hours Milestone')
        if total_hours >= 50:
            accolades.append('50 Hours Milestone')
        return accolades

    def check_milestones(self, recent_logged=None):
        """
        Business logic to check if the student achieved a milestone.
        If a recent_logged is provided, use it to determine whether a milestone
        was just crossed and notify observers.
        """
        total_hours = sum(lh.hours for lh in self.loggedhours if lh.status == 'approved')
        milestones = [10, 25, 50]
        if recent_logged is not None:
            previous_total = total_hours - recent_logged.hours
            for m in milestones:
                if total_hours >= m and previous_total < m:
                    # Notify observers that a milestone was achieved
                    self.notify('milestone_achieved', milestone=m, total_hours=total_hours, logged_hours_id=getattr(recent_logged, 'id', None))
        else:
            for m in milestones:
                if total_hours >= m:
                    self.notify('milestone_achieved', milestone=m, total_hours=total_hours)

