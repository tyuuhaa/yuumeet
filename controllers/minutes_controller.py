"""
minutes_controller.py
Logika bisnis untuk pencatatan notulen rapat (auto-save).
"""

from models.minutes_model import MeetingMinutes


class MinutesController:

    @staticmethod
    def get_minutes(meeting_id):
        minutes = MeetingMinutes.get_by_meeting(meeting_id)
        if minutes is None:
            return {"discussion": "", "decisions": "", "additional_notes": ""}
        return {
            "discussion": minutes.discussion or "",
            "decisions": minutes.decisions or "",
            "additional_notes": minutes.additional_notes or "",
        }

    @staticmethod
    def auto_save(meeting_id, discussion, decisions, additional_notes):
        MeetingMinutes.save(meeting_id, discussion, decisions, additional_notes)
