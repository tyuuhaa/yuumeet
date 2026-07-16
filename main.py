"""
main.py
Entry point aplikasi Event Meeting Minutes Manager.
Menjalankan inisialisasi database dan membuka window utama (Tkinter MVC app).
"""

import sys
import os

# Pastikan root project ada di path agar import antar-package (models, views, dll) berjalan
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DBManager
from views.main_window import MainWindow


def main():
    # Inisialisasi database (membuat file .db & tabel jika belum ada)
    DBManager()

    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
