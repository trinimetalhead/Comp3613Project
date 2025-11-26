from App.models.observer import Observer
from App.database import db


class ActivityHistoryManager(Observer):
    def update(self, subject, event_type, **kwargs):
        if event_type == 'request_created':
            self._handle_request_created(subject, **kwargs)
        elif event_type == 'request_denied':
            self._handle_request_denied(subject, **kwargs)
        elif event_type == 'hours_logged':
            self._handle_hours_logged(subject, **kwargs)
        elif event_type == 'milestone_achieved':
            self._handle_milestone_achieved(subject, **kwargs)

    def _handle_request_created(self, subject, **kwargs):
        # subject is a Request instance
        from App.models import ActivityHistory

        activity = ActivityHistory(
            student_id=subject.student_id,
            activity_type='request_created',
            description=f"Submitted hours request for {subject.hours} hours (pending approval)",
            hours_value=subject.hours,
            request_id=subject.id
        )
        db.session.add(activity)
        db.session.commit()

    def _handle_hours_logged(self, subject, **kwargs):
        # subject is a LoggedHours instance
        from App.models import Student, ActivityHistory

        student = db.session.get(Student, subject.student_id)
        if not student:
            return

        activities = []

        # 1. Activity for hours earned
        total_hours = sum(lh.hours for lh in student.loggedhours if lh.status == 'approved')
        activity = ActivityHistory(
            student_id=subject.student_id,
            activity_type='hours_earned',
            description=f"Earned {subject.hours} hours (approved by staff)",
            hours_value=subject.hours,
            total_hours=total_hours,
            logged_hours_id=subject.id
        )
        db.session.add(activity)
        activities.append(activity)

        # 2. Check for new milestones and accolades
        previous_total = total_hours - subject.hours
        milestones = [10, 25, 50]
        for milestone in milestones:
            if total_hours >= milestone and previous_total < milestone:
                milestone_activity = ActivityHistory(
                    student_id=subject.student_id,
                    activity_type='milestone',
                    description=f"Achieved {milestone} hours milestone!",
                    total_hours=total_hours,
                    logged_hours_id=subject.id
                )
                db.session.add(milestone_activity)
                activities.append(milestone_activity)

                accolade_activity = ActivityHistory(
                    student_id=subject.student_id,
                    activity_type='accolade',
                    description=f"{milestone} Hours Milestone",
                    total_hours=total_hours,
                    logged_hours_id=subject.id
                )
                db.session.add(accolade_activity)
                activities.append(accolade_activity)

        if activities:
            db.session.commit()

    def _handle_milestone_achieved(self, subject, **kwargs):
        # subject is a Student instance
        from App.models import ActivityHistory

        milestone = kwargs.get('milestone')
        total_hours = kwargs.get('total_hours')
        logged_hours_id = kwargs.get('logged_hours_id')

        if milestone is None:
            return

        milestone_activity = ActivityHistory(
            student_id=subject.student_id,
            activity_type='milestone',
            description=f"Achieved {milestone} hours milestone!",
            total_hours=total_hours,
            logged_hours_id=logged_hours_id
        )
        db.session.add(milestone_activity)

        accolade_activity = ActivityHistory(
            student_id=subject.student_id,
            activity_type='accolade',
            description=f"{milestone} Hours Milestone",
            total_hours=total_hours,
            logged_hours_id=logged_hours_id
        )
        db.session.add(accolade_activity)

        db.session.commit()

    def _handle_request_denied(self, subject, **kwargs):
        # subject is a Request instance
        from App.models import ActivityHistory

        activity = ActivityHistory(
            student_id=subject.student_id,
            activity_type='request_denied',
            description=f"Hours request for {subject.hours} hours was denied",
            hours_value=subject.hours,
            request_id=subject.id
        )
        db.session.add(activity)
        db.session.commit()
