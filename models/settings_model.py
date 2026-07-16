"""
settings_model.py
Model untuk menyimpan pengaturan aplikasi (key-value) seperti tema, warna, dan lokasi data.
"""

from database.db_manager import DBManager


class Settings:
    DEFAULTS = {
        "theme": "light",
        "accent_color": "#1E3A5F",
        "data_location": "",
    }

    @classmethod
    def get(cls, key, default=None):
        db = DBManager()
        row = db.fetch_one("SELECT value FROM settings WHERE key=?", (key,))
        if row:
            return row["value"]
        return default if default is not None else cls.DEFAULTS.get(key)

    @classmethod
    def set(cls, key, value):
        db = DBManager()
        db.execute(
            """INSERT INTO settings (key, value) VALUES (?, ?)
               ON CONFLICT(key) DO UPDATE SET value=excluded.value""",
            (key, value)
        )

    @classmethod
    def get_all(cls):
        db = DBManager()
        rows = db.fetch_all("SELECT key, value FROM settings")
        result = dict(cls.DEFAULTS)
        for r in rows:
            result[r["key"]] = r["value"]
        return result
