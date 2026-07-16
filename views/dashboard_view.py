"""
dashboard_view.py
Halaman Dashboard: ringkasan rapat, tugas, kalender agenda, dan statistik progres.
"""

import tkinter as tk
from utils.theme import Theme
from utils.helpers import format_date_display, days_until, priority_color, month_name_id
from controllers.dashboard_controller import DashboardController
from views.components.cards import StatCard, Card, ProgressBar
from views.components.widgets import Badge


class DashboardView(tk.Frame):
    def __init__(self, parent, controller_app):
        super().__init__(parent, bg=Theme.color("bg_primary"))
        self.controller_app = controller_app
        self.refresh()

    def refresh(self):
        for widget in self.winfo_children():
            widget.destroy()

        summary = DashboardController.get_summary()
        upcoming_meetings = DashboardController.get_upcoming_meetings(5)
        deadline_tasks = DashboardController.get_upcoming_deadline_tasks(7)
        status_stats = DashboardController.get_task_status_stats()
        productivity = DashboardController.get_productivity_score()

        scroll_canvas = tk.Canvas(self, bg=Theme.color("bg_primary"), highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=scroll_canvas.yview)
        content = tk.Frame(scroll_canvas, bg=Theme.color("bg_primary"))

        content.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))
        window = scroll_canvas.create_window((0, 0), window=content, anchor="nw")
        scroll_canvas.bind("<Configure>", lambda e: scroll_canvas.itemconfig(window, width=e.width))
        scroll_canvas.configure(yscrollcommand=scrollbar.set)

        def _on_mousewheel(event):
            scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        scroll_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        scroll_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ===== Stat Cards Row =====
        cards_row = tk.Frame(content, bg=Theme.color("bg_primary"))
        cards_row.pack(fill="x", padx=25, pady=(20, 10))

        StatCard(cards_row, "📅", "Total Rapat", summary["total_meetings"],
                 color=Theme.color("accent")).pack(side="left", padx=(0, 15))
        StatCard(cards_row, "📌", "Tugas Belum Selesai", summary["unfinished_tasks"],
                 color=Theme.color("warning")).pack(side="left", padx=(0, 15))
        StatCard(cards_row, "⏰", "Deadline 7 Hari Kedepan", summary["upcoming_deadlines"],
                 color=Theme.color("danger")).pack(side="left", padx=(0, 15))
        StatCard(cards_row, "📈", "Penyelesaian Tugas", f"{summary['completion_percentage']}%",
                 color=Theme.color("success")).pack(side="left")

        # ===== Middle Row: Upcoming Meetings + Task Progress =====
        middle_row = tk.Frame(content, bg=Theme.color("bg_primary"))
        middle_row.pack(fill="x", padx=25, pady=10)

        meeting_card = Card(middle_row, title="📅 Agenda Rapat Mendatang", width=480, height=280)
        meeting_card.pack(side="left", padx=(0, 15), fill="y")
        self._build_upcoming_meetings(meeting_card.body, upcoming_meetings)

        progress_card = Card(middle_row, title="📊 Statistik Tugas", width=480, height=280)
        progress_card.pack(side="left", fill="both", expand=True)
        self._build_task_stats(progress_card.body, status_stats, productivity)

        # ===== Bottom Row: Deadlines =====
        bottom_row = tk.Frame(content, bg=Theme.color("bg_primary"))
        bottom_row.pack(fill="both", expand=True, padx=25, pady=(10, 25))

        deadline_card = Card(bottom_row, title="⏰ Tugas Akan Jatuh Tempo (7 Hari)")
        deadline_card.pack(fill="both", expand=True)
        self._build_deadline_list(deadline_card.body, deadline_tasks)

    def _build_upcoming_meetings(self, parent, meetings):
        if not meetings:
            tk.Label(
                parent, text="Belum ada rapat mendatang.", bg=Theme.color("card_bg"),
                fg=Theme.color("text_secondary"), font=Theme.font(9)
            ).pack(pady=20)
            return

        for m in meetings:
            row = tk.Frame(parent, bg=Theme.color("card_bg"))
            row.pack(fill="x", pady=6)

            date_box = tk.Label(
                row, text=format_date_display(m.date).split(" ")[0], bg=Theme.color("accent"),
                fg="white", font=Theme.font(11, "bold"), width=4, height=2
            )
            date_box.pack(side="left", padx=(0, 10))

            info = tk.Frame(row, bg=Theme.color("card_bg"))
            info.pack(side="left", fill="x", expand=True)
            tk.Label(
                info, text=m.title, bg=Theme.color("card_bg"), fg=Theme.color("text_primary"),
                font=Theme.font(10, "bold"), anchor="w"
            ).pack(fill="x")
            tk.Label(
                info, text=f"{format_date_display(m.date)} • {m.time} • {m.location or '-'}",
                bg=Theme.color("card_bg"), fg=Theme.color("text_secondary"),
                font=Theme.font(8), anchor="w"
            ).pack(fill="x")

    def _build_task_stats(self, parent, status_stats, productivity):
        info_row = tk.Frame(parent, bg=Theme.color("card_bg"))
        info_row.pack(fill="x", pady=(0, 10))
        tk.Label(
            info_row, text="Productivity Score", bg=Theme.color("card_bg"),
            fg=Theme.color("text_secondary"), font=Theme.font(9)
        ).pack(anchor="w")
        tk.Label(
            info_row, text=f"{productivity}", bg=Theme.color("card_bg"),
            fg=Theme.color("success"), font=Theme.font(20, "bold")
        ).pack(anchor="w")
        ProgressBar(parent, width=440, height=10, percentage=productivity,
                    color=Theme.color("success")).pack(anchor="w", pady=(0, 15))

        for status, count in status_stats.items():
            row = tk.Frame(parent, bg=Theme.color("card_bg"))
            row.pack(fill="x", pady=4)
            tk.Label(
                row, text=status, bg=Theme.color("card_bg"),
                fg=Theme.color("text_primary"), font=Theme.font(9), width=14, anchor="w"
            ).pack(side="left")
            total = sum(status_stats.values()) or 1
            pct = (count / total) * 100
            ProgressBar(row, width=250, height=10, percentage=pct).pack(side="left", padx=8)
            tk.Label(
                row, text=str(count), bg=Theme.color("card_bg"),
                fg=Theme.color("text_secondary"), font=Theme.font(9)
            ).pack(side="left")

    def _build_deadline_list(self, parent, tasks):
        if not tasks:
            tk.Label(
                parent, text="Tidak ada tugas yang akan jatuh tempo dalam 7 hari.",
                bg=Theme.color("card_bg"), fg=Theme.color("text_secondary"), font=Theme.font(9)
            ).pack(pady=20)
            return

        for t in tasks:
            row = tk.Frame(parent, bg=Theme.color("card_bg"))
            row.pack(fill="x", pady=5)

            Badge(row, t.priority, priority_color(t.priority)).pack(side="left")
            tk.Label(
                row, text=t.task_name, bg=Theme.color("card_bg"), fg=Theme.color("text_primary"),
                font=Theme.font(9, "bold"), anchor="w"
            ).pack(side="left", padx=10)
            tk.Label(
                row, text=f"PJ: {t.assignee or '-'}", bg=Theme.color("card_bg"),
                fg=Theme.color("text_secondary"), font=Theme.font(8)
            ).pack(side="left", padx=10)

            days = days_until(t.deadline)
            label_text = f"Jatuh tempo: {format_date_display(t.deadline)}"
            if days is not None:
                if days < 0:
                    label_text += f" (Terlambat {abs(days)} hari)"
                elif days == 0:
                    label_text += " (Hari ini!)"
                else:
                    label_text += f" ({days} hari lagi)"

            tk.Label(
                row, text=label_text, bg=Theme.color("card_bg"),
                fg=Theme.color("danger") if (days is not None and days <= 1) else Theme.color("text_secondary"),
                font=Theme.font(8)
            ).pack(side="right", padx=10)
