"""
dashboard_controller.py
Mengagregasi data dari beberapa model untuk ditampilkan di Dashboard.
"""

from models.meeting_model import Meeting
from models.action_item_model import ActionItem


class DashboardController:

    @staticmethod
    def get_summary():
        return {
            "total_meetings": Meeting.count_all(),
            "unfinished_tasks": ActionItem.count_unfinished(),
            "upcoming_deadlines": len(ActionItem.upcoming_deadlines(7)),
            "completion_percentage": ActionItem.completion_percentage(),
        }

    @staticmethod
    def get_upcoming_meetings(limit=5):
        return Meeting.upcoming(limit)

    @staticmethod
    def get_upcoming_deadline_tasks(days=7):
        return ActionItem.upcoming_deadlines(days)

    @staticmethod
    def get_overdue_tasks():
        return ActionItem.overdue()

    @staticmethod
    def get_task_status_stats():
        return ActionItem.count_by_status()

    @staticmethod
    def get_meetings_per_month():
        return Meeting.count_per_month()

    @staticmethod
    def get_productivity_score():
        """
        Productivity Score sederhana berdasarkan:
        - persentase tugas selesai (bobot 70%)
        - rendahnya jumlah tugas overdue (bobot 30%)
        """
        completion = ActionItem.completion_percentage()
        overdue_count = len(ActionItem.overdue())
        total = len(ActionItem.get_all())
        overdue_penalty = 0 if total == 0 else min(30, (overdue_count / total) * 100 * 0.3)
        score = max(0, min(100, (completion * 0.7) + (30 - overdue_penalty)))
        return round(score, 1)
