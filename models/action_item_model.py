"""
action_item_model.py
Model untuk entitas Action Item (Tugas hasil rapat).
"""

from database.db_manager import DBManager


class ActionItem:
    PRIORITIES = ["Low", "Medium", "High"]
    STATUSES = ["To Do", "In Progress", "Done"]

    def __init__(self, id=None, meeting_id=None, task_name="", assignee="",
                 priority="Medium", deadline="", status="To Do",
                 created_at=None, updated_at=None):
        self.id = id
        self.meeting_id = meeting_id
        self.task_name = task_name
        self.assignee = assignee
        self.priority = priority
        self.deadline = deadline
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def _row_to_obj(row):
        if row is None:
            return None
        return ActionItem(
            id=row["id"], meeting_id=row["meeting_id"], task_name=row["task_name"],
            assignee=row["assignee"], priority=row["priority"], deadline=row["deadline"],
            status=row["status"], created_at=row["created_at"], updated_at=row["updated_at"]
        )

    @classmethod
    def create(cls, task_name, assignee, priority, deadline, status="To Do", meeting_id=None):
        db = DBManager()
        cur = db.execute(
            """INSERT INTO action_items (meeting_id, task_name, assignee, priority, deadline, status)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (meeting_id, task_name, assignee, priority, deadline, status)
        )
        return cur.lastrowid

    @classmethod
    def update(cls, item_id, task_name, assignee, priority, deadline, status, meeting_id=None):
        db = DBManager()
        db.execute(
            """UPDATE action_items SET task_name=?, assignee=?, priority=?, deadline=?,
               status=?, meeting_id=?, updated_at=datetime('now','localtime') WHERE id=?""",
            (task_name, assignee, priority, deadline, status, meeting_id, item_id)
        )

    @classmethod
    def update_status(cls, item_id, status):
        db = DBManager()
        db.execute(
            "UPDATE action_items SET status=?, updated_at=datetime('now','localtime') WHERE id=?",
            (status, item_id)
        )

    @classmethod
    def delete(cls, item_id):
        db = DBManager()
        db.execute("DELETE FROM action_items WHERE id=?", (item_id,))

    @classmethod
    def get_by_id(cls, item_id):
        db = DBManager()
        row = db.fetch_one("SELECT * FROM action_items WHERE id=?", (item_id,))
        return cls._row_to_obj(row)

    @classmethod
    def get_all(cls, order_by="deadline ASC"):
        db = DBManager()
        rows = db.fetch_all(f"SELECT * FROM action_items ORDER BY {order_by}")
        return [cls._row_to_obj(r) for r in rows]

    @classmethod
    def get_by_meeting(cls, meeting_id):
        db = DBManager()
        rows = db.fetch_all("SELECT * FROM action_items WHERE meeting_id=?", (meeting_id,))
        return [cls._row_to_obj(r) for r in rows]

    @classmethod
    def search(cls, keyword):
        db = DBManager()
        like = f"%{keyword}%"
        rows = db.fetch_all(
            "SELECT * FROM action_items WHERE task_name LIKE ? OR assignee LIKE ? ORDER BY deadline ASC",
            (like, like)
        )
        return [cls._row_to_obj(r) for r in rows]

    @classmethod
    def filter(cls, status=None, assignee=None, priority=None, date_from=None, date_to=None):
        db = DBManager()
        query = "SELECT * FROM action_items WHERE 1=1"
        params = []
        if status and status != "Semua":
            query += " AND status=?"
            params.append(status)
        if assignee:
            query += " AND assignee LIKE ?"
            params.append(f"%{assignee}%")
        if priority and priority != "Semua":
            query += " AND priority=?"
            params.append(priority)
        if date_from:
            query += " AND deadline >= ?"
            params.append(date_from)
        if date_to:
            query += " AND deadline <= ?"
            params.append(date_to)
        query += " ORDER BY deadline ASC"
        rows = db.fetch_all(query, tuple(params))
        return [cls._row_to_obj(r) for r in rows]

    @classmethod
    def count_by_status(cls):
        db = DBManager()
        rows = db.fetch_all("SELECT status, COUNT(*) as total FROM action_items GROUP BY status")
        result = {s: 0 for s in cls.STATUSES}
        for r in rows:
            result[r["status"]] = r["total"]
        return result

    @classmethod
    def count_unfinished(cls):
        db = DBManager()
        row = db.fetch_one("SELECT COUNT(*) as total FROM action_items WHERE status != 'Done'")
        return row["total"] if row else 0

    @classmethod
    def upcoming_deadlines(cls, days=7):
        db = DBManager()
        rows = db.fetch_all(
            """SELECT * FROM action_items
               WHERE status != 'Done' AND deadline BETWEEN date('now','localtime')
               AND date('now', ?)
               ORDER BY deadline ASC""",
            (f"+{days} day",)
        )
        return [cls._row_to_obj(r) for r in rows]

    @classmethod
    def overdue(cls):
        db = DBManager()
        rows = db.fetch_all(
            """SELECT * FROM action_items WHERE status != 'Done'
               AND deadline < date('now','localtime') ORDER BY deadline ASC"""
        )
        return [cls._row_to_obj(r) for r in rows]

    @classmethod
    def completion_percentage(cls):
        db = DBManager()
        total = db.fetch_one("SELECT COUNT(*) as t FROM action_items")["t"]
        if not total:
            return 0
        done = db.fetch_one("SELECT COUNT(*) as d FROM action_items WHERE status='Done'")["d"]
        return round((done / total) * 100, 1)
