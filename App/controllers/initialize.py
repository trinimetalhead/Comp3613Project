from App.models import Student, Staff, Request
from App.database import db


def initialize():


    db.drop_all()
    db.create_all()
    #create_user('bob', 'bobpass')

    # Add sample students

    students = [
        Student(name='Alice', email='alice.smith@gmail.com'),
        Student(name='Bob', email='bob.jones@hotmail.com'),
        Student(name='Charlie', email='charlie.brown@gmail.com'),
        Student(name='Diana', email='diana.lee@hotmail.com'),
        Student(name='Eve', email='eve.patel@gmail.com'),
        Student(name='Frank', email='frank.miller@gmail.com'),
        Student(name='Grace', email='grace.wilson@hotmail.com'),
    ]
    db.session.add_all(students)
    db.session.commit()


    staff_members = [
        Staff(name='Mr. Smith', email='mr.smith@gmail.com'),
        Staff(name='Ms. Johnson', email='ms.johnson@hotmail.com'),
        Staff(name='Mr. Lee', email='mr.lee@gmail.com'),
        
    ]
    for staff_member in staff_members:
        db.session.add(staff_member)
    db.session.commit()

    # Add sample requests for students
    all_students = Student.query.order_by(Student.id).all()
    requests = []
    import random
    for i, student in enumerate(all_students):
        hours = random.randint(10, 60)
        req = Request(student_id=student.id, hours=hours, status='pending')
        requests.append(req)
    db.session.add_all(requests)
    db.session.commit()

    # Add sample logged hours (approve first 2 requests by first 3 staff)
    from App.models import LoggedHours
    all_staff = Staff.query.order_by(Staff.id).all()
    for i, req in enumerate(requests[:3]):
        staff_member = all_staff[i % len(all_staff)]
        if i < 2:
            req.status = 'approved'
            log = LoggedHours(student_id=req.student_id, staff_id=staff_member.id, hours=req.hours, status='approved')
            db.session.add(log)
        else:
            req.status = 'denied'
    db.session.commit()

    
    