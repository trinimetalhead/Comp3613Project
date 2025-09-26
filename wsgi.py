import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.models import Student
from App.models import Staff
from App.models import Request
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


'''APP COMMANDS(TESTING PURPOSES)'''

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')



#Comamand to list all staff in the database
@app.cli.command ("listStaff", help="Lists all staff in the database")
def listStaff():
    print("\n")
    staff = Staff.query.all()
    for member in staff:
        print(member)
    print("\n")


#Comamand to list all students in the database
@app.cli.command ("listStudents", help="Lists all students in the database")
def listStudents():
    print("\n")
    students = Student.query.all()
    for student in students:
        print(student)
    print("\n")


#Comamand to list all requests in the database
@app.cli.command ("listRequests", help="Lists all requests in the database")
def listRequests():
    print("\nAll Requests:")
    requests = Request.query.all()
    for request in requests:
        print(request)
    print("\n")


#Comamand to list all approved requests in the database
@app.cli.command ("listApprovedRequests", help="Lists all approved requests in the database")
def listApprovedRequests():
    print("\nApproved Requests:")
    requests = Request.query.filter_by(status='approved').all()
    for request in requests:
        print(request)
    print("\n")


#Comamand to list all pending requests in the database
@app.cli.command ("listPendingRequests", help="Lists all pending requests in the database")
def listPendingRequests():
    print("\nPending Requests:")
    requests = Request.query.filter_by(status='pending').all()
    for request in requests:
        print(request)
    print("\n")


#Comamand to list all denied requests in the database
@app.cli.command ("listDeniedRequests", help="Lists all denied requests in the database")
def listDeniedRequests():
    print("\nDenied Requests:")
    requests = Request.query.filter_by(status='denied').all()
    for request in requests:
        print(request)
    print("\n")


#Comamand to list all logged hours in the database
@app.cli.command ("listloggedHours", help="Lists all logged hours in the database")
def listloggedHours():
    print("\n")
    from App.models import LoggedHours
    logs = LoggedHours.query.all()
    for log in logs:
        print(log)
    print("\n")



'''STUDENT COMMANDS'''

student_cli = AppGroup('student', help='Student object commands')

@student_cli.command("hours", help="View total approved hours for a student")

def hours ():
    print("\n")
    student_id = int(input("Enter your student ID: "))

    student = Student.query.get(student_id)
    if not student:
        print(f"Student with id {student_id} not found.")
        return
    total_hours = sum(lh.hours for lh in student.loggedhours if lh.status == 'approved')
    print(f"Total approved hours for {student.name}: {total_hours}")
    print("\n")

@student_cli.command("create", help="Create a new student")
def create_student():
    print("\n")
    name = input("Enter student name: ")
    email = input("Enter student email: ")
    student = Student.create_student(name, email)
    print(f"Created student: {student}")
    print("\n")




#Command for student to request hour confirmation (student_id, hours)
@student_cli.command("requestHours", help="Student requests hour confirmation (interactive)")
def requestHours():

    print("\n")
    student_id = int(input("Enter your student ID: "))
    hours = float(input("Enter the number of hours to request: "))
    
    
    student = Student.query.get(student_id)
    if not student:
        print(f"Student with id {student_id} not found.")
        return
    req = student.request_hours_confirmation(hours)
    print(f"Requested {hours} hours for confirmation. Request ID: {req.id}, Status: {req.status}")
    print("\n")


#command to list all requests made by a specific student(student_id)
@student_cli.command("viewmyRequests", help="List all requests for a student")
def viewmyRequests():
    print("\n")
    student_id = int(input("Enter your student ID: "))
    student = Student.query.get(student_id)
    if not student:
        print(f"Student with id {student_id} not found.")
        return
    if not student.requests:
        print(f"No requests found for student {student_id}.")
    for req in student.requests:
        print(req)
    print("\n")


#command to list all accolades for a specific student (student_id)
@student_cli.command("viewmyAccolades", help="List all accolades for a student")
def viewmyAccolades():
    print("\n")
    student_id = int(input("Enter your student ID: "))
    student = Student.query.get(student_id)
    if not student:
        print(f"Student with id {student_id} not found.")
        return
    accolades = student.accolades()
    if not accolades:
        print(f"No accolades found for student {student_id}.")
    else:
        print(f"Accolades for student {student_id}:")
        for accolade in accolades:
            print(f"- {accolade}")
    print("\n")


#Student command to view leaderboard of students by approved hours
@student_cli.command("viewLeaderboard", help="View leaderboard of students by approved hours")
def viewLeaderboard():
    print("\n")
    students = Student.query.all()
    leaderboard = sorted(students, key=lambda s: sum(lh.hours for lh in s.loggedhours if lh.status == 'approved'), reverse=True)
    print("Leaderboard (by approved hours):")
    for rank, student in enumerate(leaderboard, 1):
        total_hours = sum(lh.hours for lh in student.loggedhours if lh.status == 'approved')
        print(f"{rank:<6}. {student.name:<10} ------ \t{total_hours} hours")
    print("\n")

app.cli.add_command(student_cli) # add the group to the cli




'''STAFF COMMANDS'''



staff_cli = AppGroup('staff', help='Staff object commands')

@staff_cli.command("create", help="Create a new staff member")
def create_staff():
    print("\n")
    name = input("Enter staff name: ")
    email = input("Enter staff email: ")
    staff = Staff.create_staff(name, email)
    print(f"Created staff member: {staff}")
    print("\n")


#Command for staff to view all pending requests
@staff_cli.command("requests", help="View all pending hour requests")
def requests():
    from App.models import Request, Student
    pending_requests = Request.query.filter_by(status='pending').all()
    if not pending_requests:
        print("No pending requests found.")
        return
    print("\n\nPending Requests:")
    for req in pending_requests:
        student = Student.query.get(req.student_id)
        student_name = student.name if student else "Unknown"
        print(f"Request ID: {req.id:<4} Student: {student_name:<10} Hours: {req.hours:<7}  Status: {req.status}")
    
    print("\n")


#Command for staff to approve a student's request (staff_id, request_id)
#Once approved it is added to logged hours database
@staff_cli.command("approveRequest", help="Staff approves a student's request")
def approveRequest():

    print("\n")
    staff_id = int(input("Enter your staff ID: "))
    request_id = int(input("Enter the request ID to approve: "))

    staff = Staff.query.get(staff_id)
    if not staff:
        print(f"Staff with id {staff_id} not found.")
        return
    request = Request.query.get(request_id)
    if not request:
        print(f"Request with id {request_id} not found.")
        return
    student = Student.query.get(request.student_id)
    student_name = student.name 
    logged = staff.approve_request(request)
    if logged:
        print(f"Request {request_id} for {request.hours} hours made by {student_name} approved by Staff {staff.name} (ID: {staff_id}). Logged Hours ID: {logged.id}")
    else:
        print(f"Request {request_id} for {request.hours} hours made by {student_name} could not be approved (Already Processed).")
    print("\n")



# Command for staff to deny a student's request (staff_id, request_id)
#change request status to denied, no logged hours created
@staff_cli.command("denyRequest", help="Staff denies a student's request") 
def denyRequest():
    print("\n")
    staff_id = int(input("Enter your staff ID: "))
    request_id = int(input("Enter the request ID to deny: "))

    staff = Staff.query.get(staff_id)
    if not staff:
        print(f"Staff with id {staff_id} not found.")
        return
    request = Request.query.get(request_id)
    if not request:
        print(f"Request with id {request_id} not found.")
        return
    student = Student.query.get(request.student_id)
    student_name = student.name
    success = staff.deny_request(request)
    if success:
        print(f"Request {request_id} for {request.hours} hours made by {student_name} denied by Staff {staff.name} (ID: {staff_id}).")
    else:
        print(f"Request {request_id} for {request.hours} hours made by {student_name} could not be denied (Already Processed).")
    print("\n")


#staff command to view leaderboard of students by approved hours
@staff_cli.command("viewLeaderboard", help="View leaderboard of students by approved hours")
def viewLeaderboard():
    students = Student.query.all()
    leaderboard = sorted(students, key=lambda s: sum(lh.hours for lh in s.loggedhours if lh.status == 'approved'), reverse=True)
    print("\n")
    print("Leaderboard (by approved hours):")
    for rank, student in enumerate(leaderboard, 1):
        total_hours = sum(lh.hours for lh in student.loggedhours if lh.status == 'approved')
        print(f"{rank:<6}. {student.name:<10} ------ \t{total_hours} hours")
    print("\n")

app.cli.add_command(staff_cli) # add the group to the cli