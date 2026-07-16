"""
cards.py
Komponen kartu (cards) untuk Dashboard bergaya Notion/Trello.
"""

import tkinter as tk
from utils.theme import Theme


class StatCard(tk.Frame):
    """Kartu ringkasan statistik dengan ikon, nilai, dan label."""

    def __init__(self, parent, icon, label, value, color=None, width=230, height=110):
        super().__init__(
            parent, bg=Theme.color("card_bg"), highlightthickness=1,
            highlightbackground=Theme.color("border"), width=width, height=height
        )
        self.pack_propagate(False)
        self.color = color or Theme.color("accent")
        self._build(icon, label, value)

    def _build(self, icon, label, value):
        top = tk.Frame(self, bg=Theme.color("card_bg"))
        top.pack(fill="x", padx=18, pady=(16, 0))

        icon_box = tk.Label(
            top, text=icon, bg=self.color, fg="white",
            font=Theme.font(14), width=2, height=1
        )
        icon_box.pack(side="left")

        self.value_label = tk.Label(
            self, text=str(value), bg=Theme.color("card_bg"),
            fg=Theme.color("text_primary"), font=Theme.font(22, "bold")
        )
        self.value_label.pack(anchor="w", padx=18, pady=(10, 0))

        tk.Label(
            self, text=label, bg=Theme.color("card_bg"),
            fg=Theme.color("text_secondary"), font=Theme.font(9)
        ).pack(anchor="w", padx=18, pady=(0, 12))

    def update_value(self, value):
        self.value_label.config(text=str(value))


class Card(tk.Frame):
    """Kartu container generik dengan judul, dipakai untuk section dashboard/panel lain."""

    def __init__(self, parent, title=None, width=None, height=None):
        super().__init__(
            parent, bg=Theme.color("card_bg"), highlightthickness=1,
            highlightbackground=Theme.color("border")
        )
        if width:
            self.config(width=width)
        if height:
            self.config(height=height)
        if width or height:
            self.pack_propagate(False)

        if title:
            header = tk.Frame(self, bg=Theme.color("card_bg"))
            header.pack(fill="x", padx=16, pady=(14, 4))
            tk.Label(
                header, text=title, bg=Theme.color("card_bg"),
                fg=Theme.color("text_primary"), font=Theme.font(12, "bold")
            ).pack(anchor="w")

        self.body = tk.Frame(self, bg=Theme.color("card_bg"))
        self.body.pack(fill="both", expand=True, padx=16, pady=(4, 14))


class ProgressBar(tk.Frame):
    """Progress bar sederhana dibuat dari Canvas (karena ttk.Progressbar kurang stylish)."""

    def __init__(self, parent, width=200, height=14, percentage=0, color=None):
        super().__init__(parent, bg=Theme.color("card_bg"))
        self.width = width
        self.height = height
        self.color = color or Theme.color("accent")
        self.canvas = tk.Canvas(
            self, width=width, height=height, bg=Theme.color("border"),
            highlightthickness=0
        )
        self.canvas.pack()
        self.set_percentage(percentage)

    def set_percentage(self, percentage):
        self.canvas.delete("all")
        percentage = max(0, min(100, percentage))
        fill_width = int(self.width * (percentage / 100))
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill=Theme.color("border"), width=0)
        if fill_width > 0:
            self.canvas.create_rectangle(0, 0, fill_width, self.height, fill=self.color, width=0)
