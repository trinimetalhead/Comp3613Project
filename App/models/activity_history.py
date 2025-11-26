from App.database import db
from datetime import datetime

class ActivityHistory(db.Model):
    """
    Tracks student activity history including:
    - Hours earned
    - Milestones achieved
    - Accolades rewarded
    
    Uses Observer pattern to automatically create records when events occur.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # 'hours_earned', 'milestone', 'accolade', 'request_created'
    description = db.Column(db.String(255), nullable=False)
    hours_value = db.Column(db.Float, nullable=True)  # For hours_earned activity
    total_hours = db.Column(db.Float, nullable=True)  # Cumulative hours at time of activity
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Optional: Link to related records
    logged_hours_id = db.Column(db.Integer, db.ForeignKey('logged_hours.id'), nullable=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=True)

    def __init__(self, student_id, activity_type, description, hours_value=None, total_hours=None, logged_hours_id=None, request_id=None):
        self.student_id = student_id
        self.activity_type = activity_type
        self.description = description
        self.hours_value = hours_value
        self.total_hours = total_hours
        self.logged_hours_id = logged_hours_id
        self.request_id = request_id

    def __repr__(self):
        return f"[ActivityID={self.id} StudentID={self.student_id} Type={self.activity_type} Description={self.description}]"

    def get_json(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'activity_type': self.activity_type,
            'description': self.description,
            'hours_value': self.hours_value,
            'total_hours': self.total_hours,
            'timestamp': self.timestamp.isoformat()
        }
