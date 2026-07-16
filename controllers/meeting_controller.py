"""
meeting_controller.py
Menjembatani View dengan Model Meeting. Berisi logika bisnis terkait pengelolaan rapat.
"""

from models.meeting_model import Meeting
from models.minutes_model import MeetingMinutes
from models.action_item_model import ActionItem
from utils.validators import validate_meeting_form


class MeetingController:

    @staticmethod
    def create_meeting(title, date, time, location, chairperson, participants, agenda):
        validate_meeting_form(title, date, time, location, chairperson)
        return Meeting.create(title, date, time, location, chairperson, participants, agenda)

    @staticmethod
    def update_meeting(meeting_id, title, date, time, location, chairperson, participants, agenda):
        validate_meeting_form(title, date, time, location, chairperson)
        Meeting.update(meeting_id, title, date, time, location, chairperson, participants, agenda)

    @staticmethod
    def delete_meeting(meeting_id):
        # Menghapus notulen & tugas terkait agar data tetap konsisten
        MeetingMinutes.delete_by_meeting(meeting_id)
        for item in ActionItem.get_by_meeting(meeting_id):
            ActionItem.delete(item.id)
        Meeting.delete(meeting_id)

    @staticmethod
    def get_meeting(meeting_id):
        return Meeting.get_by_id(meeting_id)

    @staticmethod
    def get_all_meetings():
        return Meeting.get_all()

    @staticmethod
    def search_meetings(keyword):
        if not keyword:
            return Meeting.get_all()
        return Meeting.search(keyword)

    @staticmethod
    def get_meetings_by_month(year, month):
        return Meeting.filter_by_month(year, month)

    @staticmethod
    def get_meetings_by_date(date_str):
        return Meeting.filter_by_date(date_str)

    @staticmethod
    def get_upcoming_meetings(limit=5):
        return Meeting.upcoming(limit)

    @staticmethod
    def count_meetings():
        return Meeting.count_all()
