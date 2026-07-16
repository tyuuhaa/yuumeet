"""
minutes_model.py
Model untuk entitas Meeting Minutes (Notulen Rapat).
"""

from database.db_manager import DBManager


class MeetingMinutes:
    def __init__(self, id=None, meeting_id=None, discussion="", decisions="",
                 additional_notes="", created_at=None, updated_at=None):
        self.id = id
        self.meeting_id = meeting_id
        self.discussion = discussion
        self.decisions = decisions
        self.additional_notes = additional_notes
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def _row_to_obj(row):
        if row is None:
            return None
        return MeetingMinutes(
            id=row["id"], meeting_id=row["meeting_id"], discussion=row["discussion"],
            decisions=row["decisions"], additional_notes=row["additional_notes"],
            created_at=row["created_at"], updated_at=row["updated_at"]
        )

    @classmethod
    def get_by_meeting(cls, meeting_id):
        db = DBManager()
        row = db.fetch_one("SELECT * FROM minutes WHERE meeting_id=?", (meeting_id,))
        return cls._row_to_obj(row)

    @classmethod
    def save(cls, meeting_id, discussion, decisions, additional_notes):
        """Auto-save: insert jika belum ada, update jika sudah ada (upsert)."""
        db = DBManager()
        existing = cls.get_by_meeting(meeting_id)
        if existing:
            db.execute(
                """UPDATE minutes SET discussion=?, decisions=?, additional_notes=?,
                   updated_at=datetime('now','localtime') WHERE meeting_id=?""",
                (discussion, decisions, additional_notes, meeting_id)
            )
        else:
            db.execute(
                """INSERT INTO minutes (meeting_id, discussion, decisions, additional_notes)
                   VALUES (?, ?, ?, ?)""",
                (meeting_id, discussion, decisions, additional_notes)
            )

    @classmethod
    def delete_by_meeting(cls, meeting_id):
        db = DBManager()
        db.execute("DELETE FROM minutes WHERE meeting_id=?", (meeting_id,))
