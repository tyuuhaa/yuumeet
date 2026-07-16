"""
db_manager.py
Mengelola koneksi SQLite, inisialisasi skema, serta backup & restore database.
Menggunakan pola Singleton agar koneksi database konsisten di seluruh aplikasi.
"""

import sqlite3
import os
import shutil
import sys
from datetime import datetime


class DBManager:
    """Singleton class untuk mengelola koneksi database SQLite."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DBManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_path=None):
        # Hindari re-inisialisasi jika instance sudah ada
        if hasattr(self, "_initialized") and self._initialized:
            return

        if getattr(sys, 'frozen', False):
            base_dir_app = sys._MEIPASS
            exe_dir = os.path.dirname(sys.executable)
            self.db_path = db_path or os.path.join(exe_dir, "database", "meeting_manager.db")
            self.schema_path = os.path.join(base_dir_app, "database", "schema.sql")
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.db_path = db_path or os.path.join(base_dir, "database", "meeting_manager.db")
            self.schema_path = os.path.join(base_dir, "database", "schema.sql")
        self.connection = None
        self._initialized = True
        self.connect()
        self.init_schema()

    def connect(self):
        """Membuka koneksi ke database SQLite."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        return self.connection

    def init_schema(self):
        """Menjalankan skema SQL untuk membuat tabel jika belum ada."""
        if os.path.exists(self.schema_path):
            with open(self.schema_path, "r", encoding="utf-8") as f:
                sql_script = f.read()
            self.connection.executescript(sql_script)
            self.connection.commit()

    def get_connection(self):
        if self.connection is None:
            self.connect()
        return self.connection

    def execute(self, query, params=()):
        """Menjalankan query INSERT/UPDATE/DELETE dan mengembalikan cursor."""
        cur = self.connection.cursor()
        cur.execute(query, params)
        self.connection.commit()
        return cur

    def fetch_all(self, query, params=()):
        cur = self.connection.cursor()
        cur.execute(query, params)
        return cur.fetchall()

    def fetch_one(self, query, params=()):
        cur = self.connection.cursor()
        cur.execute(query, params)
        return cur.fetchone()

    def backup_database(self, backup_dir):
        """Membuat salinan file database (backup) ke direktori tujuan."""
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"backup_{timestamp}.db")
        self.connection.commit()
        shutil.copy2(self.db_path, backup_file)
        return backup_file

    def restore_database(self, backup_file):
        """Merestore database dari file backup yang dipilih."""
        self.connection.close()
        shutil.copy2(backup_file, self.db_path)
        self.connect()
        return True

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
