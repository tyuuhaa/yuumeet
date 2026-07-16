"""
meeting_model.py
Model untuk entitas Meeting (Rapat). Bertanggung jawab atas semua operasi
CRUD terhadap tabel 'meetings' di database.
"""

from database.db_manager import DBManager


class Meeting:
    def __init__(self, id=None, title="", date="", time="", location="",
                 chairperson="", participants="", agenda="",
                 created_at=None, updated_at=None):
        self.id = id
        self.title = title
        self.date = date
        self.time = time
        self.location = location
        self.chairperson = chairperson
        self.participants = participants
        self.agenda = agenda
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def _row_to_meeting(row):
        if row is None:
            return None
        return Meeting(
            id=row["id"], title=row["title"], date=row["date"], time=row["time"],
            location=row["location"], chairperson=row["chairperson"],
            participants=row["participants"], agenda=row["agenda"],
            created_at=row["created_at"], updated_at=row["updated_at"]
        )

    @classmethod
    def create(cls, title, date, time, location, chairperson, participants, agenda):
        db = DBManager()
        cur = db.execute(
            """INSERT INTO meetings (title, date, time, location, chairperson, participants, agenda)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (title, date, time, location, chairperson, participants, agenda)
        )
        return cur.lastrowid

    @classmethod
    def update(cls, meeting_id, title, date, time, location, chairperson, participants, agenda):
        db = DBManager()
        db.execute(
            """UPDATE meetings SET title=?, date=?, time=?, location=?, chairperson=?,
               participants=?, agenda=?, updated_at=datetime('now','localtime')
               WHERE id=?""",
            (title, date, time, location, chairperson, participants, agenda, meeting_id)
        )

    @classmethod
    def delete(cls, meeting_id):
        db = DBManager()
        db.execute("DELETE FROM meetings WHERE id=?", (meeting_id,))

    @classmethod
    def get_by_id(cls, meeting_id):
        db = DBManager()
        row = db.fetch_one("SELECT * FROM meetings WHERE id=?", (meeting_id,))
        return cls._row_to_meeting(row)

    @classmethod
    def get_all(cls, order_by="date DESC"):
        db = DBManager()
        rows = db.fetch_all(f"SELECT * FROM meetings ORDER BY {order_by}")
        return [cls._row_to_meeting(r) for r in rows]

    @classmethod
    def search(cls, keyword):
        db = DBManager()
        like = f"%{keyword}%"
        rows = db.fetch_all(
            """SELECT * FROM meetings WHERE title LIKE ? OR location LIKE ?
               OR chairperson LIKE ? OR participants LIKE ? ORDER BY date DESC""",
            (like, like, like, like)
        )
        return [cls._row_to_meeting(r) for r in rows]

    @classmethod
    def filter_by_date(cls, date_str):
        db = DBManager()
        rows = db.fetch_all("SELECT * FROM meetings WHERE date=? ORDER BY time", (date_str,))
        return [cls._row_to_meeting(r) for r in rows]

    @classmethod
    def filter_by_month(cls, year, month):
        db = DBManager()
        month_str = f"{year:04d}-{month:02d}"
        rows = db.fetch_all(
            "SELECT * FROM meetings WHERE strftime('%Y-%m', date)=? ORDER BY date",
            (month_str,)
        )
        return [cls._row_to_meeting(r) for r in rows]

    @classmethod
    def count_all(cls):
        db = DBManager()
        row = db.fetch_one("SELECT COUNT(*) as total FROM meetings")
        return row["total"] if row else 0

    @classmethod
    def upcoming(cls, limit=5):
        db = DBManager()
        rows = db.fetch_all(
            """SELECT * FROM meetings WHERE date >= date('now','localtime')
               ORDER BY date ASC, time ASC LIMIT ?""",
            (limit,)
        )
        return [cls._row_to_meeting(r) for r in rows]

    @classmethod
    def count_per_month(cls):
        """Mengembalikan statistik jumlah rapat per bulan (untuk laporan)."""
        db = DBManager()
        rows = db.fetch_all(
            """SELECT strftime('%Y-%m', date) as ym, COUNT(*) as total
               FROM meetings GROUP BY ym ORDER BY ym"""
        )
        return [(r["ym"], r["total"]) for r in rows]
