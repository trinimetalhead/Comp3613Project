## General App Commands

| Command | Description |
|---------|-------------|
| `flask init` | Creates and initializes the database |
| `flask listStaff` | Lists all staff in the database |
| `flask listStudents` | Lists all students in the database |
| `flask listRequests` | Lists all requests in the database |
| `flask listApprovedRequests` | Lists all approved requests |
| `flask listPendingRequests` | Lists all pending requests |
| `flask listDeniedRequests` | Lists all denied requests |
| `flask listloggedHours` | Lists all logged hours |

---

## Student Commands

| Command | Description |
|---------|-------------|
| `flask student create` | Create a new student (interactive: enter name + email) |
| `flask student hours` | View total hours (enter student ID) |
| `flask student requestHours` | Request hour confirmation (enter student ID + hours) |
| `flask student viewmyRequests` | List all requests made by a student (enter student ID) |
| `flask student viewmyAccolades` | List all accolades earned by a student (enter student ID) |
| `flask student viewLeaderboard` | View leaderboard of students ranked by approved hours |


---

## Staff Commands

| Command | Description |
|---------|-------------|
| `flask staff create` | Create a new staff member (interactive: enter name + email) |
| `flask staff requests` | View all pending requests |
| `flask staff approveRequest` | Approve a student’s request (enter staff ID + request ID) → logs hours |
| `flask staff denyRequest` | Deny a student’s request (enter staff ID + request ID) |
| `flask staff viewLeaderboard` | View leaderboard of students ranked by approved hours |