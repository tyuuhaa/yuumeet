"""
validators.py
Kumpulan fungsi validasi input untuk form-form aplikasi.
"""

import re
from datetime import datetime


def is_not_empty(value):
    return value is not None and str(value).strip() != ""


def is_valid_date(value, fmt="%Y-%m-%d"):
    if not value:
        return False
    try:
        datetime.strptime(value, fmt)
        return True
    except ValueError:
        return False


def is_valid_time(value, fmt="%H:%M"):
    if not value:
        return False
    try:
        datetime.strptime(value, fmt)
        return True
    except ValueError:
        return False


def is_valid_priority(value):
    return value in ("Low", "Medium", "High")


def is_valid_status(value):
    return value in ("To Do", "In Progress", "Done")


class ValidationError(Exception):
    """Exception khusus untuk kesalahan validasi form."""
    pass


def validate_meeting_form(title, date, time, location, chairperson):
    errors = []
    if not is_not_empty(title):
        errors.append("Judul rapat wajib diisi.")
    if not is_valid_date(date):
        errors.append("Format tanggal tidak valid (gunakan YYYY-MM-DD).")
    if not is_valid_time(time):
        errors.append("Format waktu tidak valid (gunakan HH:MM).")
    if not is_not_empty(location):
        errors.append("Lokasi rapat wajib diisi.")
    if not is_not_empty(chairperson):
        errors.append("Ketua rapat wajib diisi.")
    if errors:
        raise ValidationError("\n".join(errors))
    return True


def validate_task_form(task_name, assignee, priority, deadline, status):
    errors = []
    if not is_not_empty(task_name):
        errors.append("Nama tugas wajib diisi.")
    if not is_not_empty(assignee):
        errors.append("Penanggung jawab wajib diisi.")
    if not is_valid_priority(priority):
        errors.append("Prioritas harus salah satu dari Low, Medium, High.")
    if not is_valid_date(deadline):
        errors.append("Format deadline tidak valid (gunakan YYYY-MM-DD).")
    if not is_valid_status(status):
        errors.append("Status harus salah satu dari To Do, In Progress, Done.")
    if errors:
        raise ValidationError("\n".join(errors))
    return True
