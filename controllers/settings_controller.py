"""
settings_controller.py
Logika bisnis untuk pengaturan aplikasi: tema, warna, backup & restore database.
"""

import os
import sys
from models.settings_model import Settings
from database.db_manager import DBManager


class SettingsController:

    @staticmethod
    def get_theme_mode():
        return Settings.get("theme", "light")

    @staticmethod
    def set_theme_mode(mode):
        Settings.set("theme", mode)

    @staticmethod
    def get_accent_color():
        return Settings.get("accent_color", "#1E3A5F")

    @staticmethod
    def set_accent_color(color):
        Settings.set("accent_color", color)

    @staticmethod
    def get_data_location():
        return Settings.get("data_location", "")

    @staticmethod
    def set_data_location(path):
        Settings.set("data_location", path)

    @staticmethod
    def backup_database():
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        backup_dir = os.path.join(base_dir, "exports", "backups")
        db = DBManager()
        return db.backup_database(backup_dir)

    @staticmethod
    def restore_database(backup_file):
        db = DBManager()
        return db.restore_database(backup_file)

    @staticmethod
    def list_backups():
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        backup_dir = os.path.join(base_dir, "exports", "backups")
        if not os.path.exists(backup_dir):
            return []
        files = [os.path.join(backup_dir, f) for f in os.listdir(backup_dir) if f.endswith(".db")]
        return sorted(files, reverse=True)
