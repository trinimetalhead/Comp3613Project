from .user import *
from .student import Student
from .staff import Staff
from .request import Request
from .loggedhours import LoggedHours
from .activity_history import ActivityHistory

# Initialize and register global observers
from .activity_history_manager import ActivityHistoryManager
from .observer import Subject

# singleton manager
activity_history_manager = ActivityHistoryManager()
Subject.attach_global(activity_history_manager)