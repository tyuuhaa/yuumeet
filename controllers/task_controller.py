"""
task_controller.py
Logika bisnis untuk pengelolaan Action Items (Tugas hasil rapat).
"""

from models.action_item_model import ActionItem
from utils.validators import validate_task_form


class TaskController:

    @staticmethod
    def create_task(task_name, assignee, priority, deadline, status="To Do", meeting_id=None):
        validate_task_form(task_name, assignee, priority, deadline, status)
        return ActionItem.create(task_name, assignee, priority, deadline, status, meeting_id)

    @staticmethod
    def update_task(item_id, task_name, assignee, priority, deadline, status, meeting_id=None):
        validate_task_form(task_name, assignee, priority, deadline, status)
        ActionItem.update(item_id, task_name, assignee, priority, deadline, status, meeting_id)

    @staticmethod
    def update_status(item_id, status):
        ActionItem.update_status(item_id, status)

    @staticmethod
    def delete_task(item_id):
        ActionItem.delete(item_id)

    @staticmethod
    def get_task(item_id):
        return ActionItem.get_by_id(item_id)

    @staticmethod
    def get_all_tasks():
        return ActionItem.get_all()

    @staticmethod
    def get_tasks_by_meeting(meeting_id):
        return ActionItem.get_by_meeting(meeting_id)

    @staticmethod
    def search_tasks(keyword):
        if not keyword:
            return ActionItem.get_all()
        return ActionItem.search(keyword)

    @staticmethod
    def filter_tasks(status=None, assignee=None, priority=None, date_from=None, date_to=None):
        return ActionItem.filter(status, assignee, priority, date_from, date_to)

    @staticmethod
    def count_unfinished():
        return ActionItem.count_unfinished()

    @staticmethod
    def count_by_status():
        return ActionItem.count_by_status()

    @staticmethod
    def upcoming_deadlines(days=7):
        return ActionItem.upcoming_deadlines(days)

    @staticmethod
    def overdue_tasks():
        return ActionItem.overdue()

    @staticmethod
    def completion_percentage():
        return ActionItem.completion_percentage()
