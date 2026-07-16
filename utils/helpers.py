"""
helpers.py
Fungsi bantu umum yang dipakai lintas komponen (formatting tanggal, warna prioritas, dll).
"""

import calendar
from datetime import datetime, date


def today_str():
    return date.today().strftime("%Y-%m-%d")


def format_date_display(date_str):
    """Mengubah YYYY-MM-DD menjadi format '16 Jul 2026'."""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        return d.strftime("%d %b %Y")
    except (ValueError, TypeError):
        return date_str or "-"


def priority_color(priority):
    from utils.theme import Theme
    mapping = {
        "High": Theme.color("danger"),
        "Medium": Theme.color("warning"),
        "Low": Theme.color("success"),
    }
    return mapping.get(priority, Theme.color("text_secondary"))


def status_color(status):
    from utils.theme import Theme
    mapping = {
        "To Do": Theme.color("text_secondary"),
        "In Progress": Theme.color("accent"),
        "Done": Theme.color("success"),
    }
    return mapping.get(status, Theme.color("text_secondary"))


def month_name_id(month_num):
    names = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
             "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    return names[month_num]


def get_month_calendar_matrix(year, month):
    """Mengembalikan matrix minggu x hari untuk kalender bulan tertentu."""
    cal = calendar.Calendar(firstweekday=0)  # Senin
    return cal.monthdayscalendar(year, month)


def days_until(deadline_str):
    """Menghitung selisih hari dari hari ini ke deadline. Negatif = terlambat."""
    try:
        d = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        return (d - date.today()).days
    except (ValueError, TypeError):
        return None


def truncate(text, length=40):
    if not text:
        return ""
    return text if len(text) <= length else text[:length - 3] + "..."
