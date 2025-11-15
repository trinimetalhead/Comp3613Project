from App.database import db
from .user import User

class Student(User):

    __tablename__ = "student"
    student_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
    
    # relationship to LoggedHours and Request both One-to-Many
    loggedhours = db.relationship('LoggedHours', backref='student', lazy=True, cascade="all, delete-orphan")
    requests = db.relationship('Request', backref='student', lazy=True, cascade="all, delete-orphan")

    # Activity logs relationship (persistent history)
    activity_logs = db.relationship('ActivityLog', backref='student', lazy=True)

    # Inheritance setup
    __mapper_args__ = {
        "polymorphic_identity": "student"
    }

    # calls parent constructor
    def __init__(self, username, email, password):
       super().__init__(username, email, password, role="student")
       # runtime-only observers list (not persisted)
       self._observers = []

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
        newstudent = Student(username=username, email=email, password=password)
        db.session.add(newstudent)
        db.session.commit()
        return newstudent
    
    # Method for student to request hours
    def request_hours_confirmation(self, hours):
        from App.models import Request
        request = Request(student_id=self.student_id, hours=hours, status='pending')
        db.session.add(request)
        db.session.commit()
        return request
    
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

    # Observer API (Subject)
    def register_observer(self, observer):
        if not hasattr(self, '_observers'):
            self._observers = []
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer):
        if hasattr(self, '_observers') and observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, event_type, payload=None):
        payload = payload or {}
        for obs in list(getattr(self, '_observers', [])):
            try:
                obs.update(self, event_type, payload)
            except Exception:
                # keep notifications best-effort; real app should log the exception
                pass

    # Convenience: return activity history as dicts (most recent first)
    def get_activity_history(self):
        return [a.to_dict() for a in sorted(self.activity_logs, key=lambda x: x.created_at, reverse=True)]

