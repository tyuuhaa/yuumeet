"""
calendar_view.py
Halaman Calendar & Timeline: menampilkan kalender bulanan agenda rapat
dan timeline deadline tugas, dengan filter bulan/tahun.
"""

import tkinter as tk
from datetime import date
from utils.theme import Theme
from utils.helpers import get_month_calendar_matrix, month_name_id, format_date_display, days_until
from controllers.meeting_controller import MeetingController
from controllers.task_controller import TaskController
from views.components.cards import Card
from views.components.widgets import ModernButton, Badge
from utils.helpers import priority_color


class CalendarView(tk.Frame):
    def __init__(self, parent, controller_app):
        super().__init__(parent, bg=Theme.color("bg_primary"))
        self.controller_app = controller_app
        today = date.today()
        self.year = today.year
        self.month = today.month
        self._build()
        self.refresh()

    def _build(self):
        nav_bar = tk.Frame(self, bg=Theme.color("bg_primary"))
        nav_bar.pack(fill="x", padx=25, pady=(20, 10))

        ModernButton(nav_bar, "◀", command=self._prev_month, padx=12).pack(side="left")
        self.month_label = tk.Label(
            nav_bar, text="", bg=Theme.color("bg_primary"),
            fg=Theme.color("text_primary"), font=Theme.font(13, "bold")
        )
        self.month_label.pack(side="left", padx=15)
        ModernButton(nav_bar, "▶", command=self._next_month, padx=12).pack(side="left")

        ModernButton(nav_bar, "Hari Ini", command=self._go_today,
                     bg=Theme.color("border"), fg=Theme.color("text_primary"),
                     hover_bg=Theme.color("border")).pack(side="left", padx=15)

        body = tk.Frame(self, bg=Theme.color("bg_primary"))
        body.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        self.calendar_card = Card(body, title="🗓 Kalender Agenda Rapat")
        self.calendar_card.pack(side="left", fill="both", expand=True, padx=(0, 15))

        self.timeline_card = Card(body, title="⏳ Timeline Deadline Tugas", width=320)
        self.timeline_card.pack(side="left", fill="y")

    def _prev_month(self):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self.refresh()

    def _next_month(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.refresh()

    def _go_today(self):
        today = date.today()
        self.year, self.month = today.year, today.month
        self.refresh()

    def refresh(self):
        self.month_label.config(text=f"{month_name_id(self.month)} {self.year}")
        self._render_calendar()
        self._render_timeline()

    def _render_calendar(self):
        for widget in self.calendar_card.body.winfo_children():
            widget.destroy()

        meetings = MeetingController.get_meetings_by_month(self.year, self.month)
        meetings_by_day = {}
        for m in meetings:
            day = int(m.date.split("-")[2])
            meetings_by_day.setdefault(day, []).append(m)

        day_names = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]
        header_row = tk.Frame(self.calendar_card.body, bg=Theme.color("card_bg"))
        header_row.pack(fill="x")
        for name in day_names:
            tk.Label(
                header_row, text=name, bg=Theme.color("card_bg"), fg=Theme.color("text_secondary"),
                font=Theme.font(9, "bold"), width=10
            ).pack(side="left", padx=1, pady=4)

        matrix = get_month_calendar_matrix(self.year, self.month)
        today = date.today()

        for week in matrix:
            week_row = tk.Frame(self.calendar_card.body, bg=Theme.color("card_bg"))
            week_row.pack(fill="x")
            for day in week:
                is_today = (day == today.day and self.year == today.year and self.month == today.month)
                cell_bg = Theme.color("accent") if is_today else Theme.color("bg_primary")
                cell = tk.Frame(
                    week_row, bg=cell_bg, width=95, height=70,
                    highlightthickness=1, highlightbackground=Theme.color("border")
                )
                cell.pack(side="left", padx=1, pady=1)
                cell.pack_propagate(False)

                if day != 0:
                    fg = "white" if is_today else Theme.color("text_primary")
                    tk.Label(
                        cell, text=str(day), bg=cell_bg, fg=fg, font=Theme.font(9, "bold")
                    ).pack(anchor="nw", padx=4, pady=2)

                    if day in meetings_by_day:
                        for m in meetings_by_day[day][:2]:
                            tk.Label(
                                cell, text=f"• {m.title[:12]}", bg=cell_bg,
                                fg="white" if is_today else Theme.color("accent"),
                                font=Theme.font(7), anchor="w"
                            ).pack(fill="x", padx=4)

    def _render_timeline(self):
        for widget in self.timeline_card.body.winfo_children():
            widget.destroy()

        tasks = TaskController.get_all_tasks()
        tasks_sorted = sorted([t for t in tasks if t.deadline], key=lambda t: t.deadline)

        if not tasks_sorted:
            tk.Label(
                self.timeline_card.body, text="Tidak ada tugas dengan deadline.",
                bg=Theme.color("card_bg"), fg=Theme.color("text_secondary"), font=Theme.font(9)
            ).pack(pady=20)
            return

        canvas = tk.Canvas(self.timeline_card.body, bg=Theme.color("card_bg"), highlightthickness=0)
        scrollbar = tk.Scrollbar(self.timeline_card.body, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=Theme.color("card_bg"))
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw", width=280)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for t in tasks_sorted:
            row = tk.Frame(inner, bg=Theme.color("card_bg"))
            row.pack(fill="x", pady=6)

            Badge(row, t.priority, priority_color(t.priority)).pack(anchor="w")
            tk.Label(
                row, text=t.task_name, bg=Theme.color("card_bg"), fg=Theme.color("text_primary"),
                font=Theme.font(9, "bold"), anchor="w", wraplength=260, justify="left"
            ).pack(fill="x", pady=(3, 0))
            tk.Label(
                row, text=f"{format_date_display(t.deadline)} • {t.status}",
                bg=Theme.color("card_bg"), fg=Theme.color("text_secondary"), font=Theme.font(8), anchor="w"
            ).pack(fill="x")

            sep = tk.Frame(inner, bg=Theme.color("border"), height=1)
            sep.pack(fill="x", pady=4)
