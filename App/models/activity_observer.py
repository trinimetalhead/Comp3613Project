from App.database import db
from App.models import ActivityLog


class ActivityObserver:
    """
    Simple Observer that writes ActivityLog rows and checks milestones.
    Usage: observer.update(student, 'hours_approved', {'hours': 3, 'staff_id': 5})
    """

    def update(self, subject, event_type, payload):
        # subject is a Student instance
        if event_type == "hours_approved":
            hours = payload.get("hours")
            staff_id = payload.get("staff_id")
            detail = f"Approved {hours} hours by staff {staff_id}"
            db.session.add(ActivityLog(student_id=subject.student_id,
                                       category="hours",
                                       detail=detail))
            db.session.commit()
            self._check_and_log_milestones(subject)

        elif event_type == "accolade_awarded":
            name = payload.get("name")
            detail = f"Awarded accolade '{name}'"
            db.session.add(ActivityLog(student_id=subject.student_id,
                                       category="accolade",
                                       detail=detail))
            db.session.commit()

    def _check_and_log_milestones(self, student):
        # compute total approved hours from student's loggedhours relationship
        total_hours = sum(lh.hours for lh in student.loggedhours if lh.status == "approved")
        milestones = [(50, "50 Hours Milestone"), (25, "25 Hours Milestone"), (10, "10 Hours Milestone")]

        # Avoid duplicate milestone logs by checking existing activity logs
        existing = {l.detail for l in getattr(student, 'activity_logs', [])}
        for threshold, name in milestones:
            if total_hours >= threshold and name not in existing:
                db.session.add(ActivityLog(student_id=student.student_id,
                                           category="milestone",
                                           detail=name))
        db.session.commit()
