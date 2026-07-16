"""
search_view.py
Halaman Search & Filter: pencarian rapat, peserta, dan tugas dengan berbagai filter.
"""

import tkinter as tk
from utils.theme import Theme
from utils.helpers import format_date_display
from controllers.meeting_controller import MeetingController
from controllers.task_controller import TaskController
from models.action_item_model import ActionItem
from views.components.widgets import create_styled_treeview, populate_treeview, ModernButton
from views.components.form_fields import LabeledEntry, LabeledCombobox, DateEntry


class SearchView(tk.Frame):
    def __init__(self, parent, controller_app):
        super().__init__(parent, bg=Theme.color("bg_primary"))
        self.controller_app = controller_app
        self._build()

    def _build(self):
        header = tk.Frame(self, bg=Theme.color("bg_primary"))
        header.pack(fill="x", padx=25, pady=(20, 10))
        tk.Label(
            header, text="Pencarian & Filter", bg=Theme.color("bg_primary"),
            fg=Theme.color("text_primary"), font=Theme.font(13, "bold")
        ).pack(anchor="w")

        # Search bar utama
        search_bar = tk.Frame(self, bg=Theme.color("bg_primary"))
        search_bar.pack(fill="x", padx=25, pady=(0, 10))

        self.keyword_field = LabeledEntry(search_bar, "Kata Kunci (judul rapat / peserta / nama tugas)")
        self.keyword_field.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.keyword_field.entry.bind("<Return>", lambda e: self._do_search())

        btn_frame = tk.Frame(search_bar, bg=Theme.color("bg_primary"))
        btn_frame.pack(side="left", anchor="s", pady=(0, 4))
        ModernButton(btn_frame, "Cari", icon="🔍", command=self._do_search).pack()

        # Filter tambahan untuk tugas
        filter_bar = tk.Frame(self, bg=Theme.color("bg_primary"))
        filter_bar.pack(fill="x", padx=25, pady=(0, 15))

        self.status_filter = LabeledCombobox(filter_bar, "Status Tugas", ["Semua"] + ActionItem.STATUSES, default="Semua")
        self.status_filter.pack(side="left", padx=(0, 10))

        self.assignee_filter = LabeledEntry(filter_bar, "Penanggung Jawab")
        self.assignee_filter.pack(side="left", padx=(0, 10))

        self.date_from_filter = DateEntry(filter_bar, "Dari Tanggal (Deadline)")
        self.date_from_filter.pack(side="left", padx=(0, 10))

        self.date_to_filter = DateEntry(filter_bar, "Sampai Tanggal (Deadline)")
        self.date_to_filter.pack(side="left", padx=(0, 10))

        btn_frame2 = tk.Frame(filter_bar, bg=Theme.color("bg_primary"))
        btn_frame2.pack(side="left", anchor="s", pady=(0, 4))
        ModernButton(btn_frame2, "Terapkan Filter", command=self._do_filter_tasks).pack()

        # Result area: dua tabel (rapat & tugas)
        result_area = tk.Frame(self, bg=Theme.color("bg_primary"))
        result_area.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        meeting_frame = tk.Frame(result_area, bg=Theme.color("card_bg"), highlightthickness=1,
                                  highlightbackground=Theme.color("border"))
        meeting_frame.pack(fill="both", expand=True, pady=(0, 10))
        tk.Label(
            meeting_frame, text="Hasil Pencarian Rapat", bg=Theme.color("card_bg"),
            fg=Theme.color("text_primary"), font=Theme.font(10, "bold")
        ).pack(anchor="w", padx=12, pady=(10, 4))

        m_container, self.meeting_tree = create_styled_treeview(
            meeting_frame, ("title", "date", "time", "location", "chairperson"),
            ("Judul Rapat", "Tanggal", "Waktu", "Lokasi", "Ketua Rapat"),
            (220, 100, 70, 140, 140)
        )
        m_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        task_frame = tk.Frame(result_area, bg=Theme.color("card_bg"), highlightthickness=1,
                               highlightbackground=Theme.color("border"))
        task_frame.pack(fill="both", expand=True)
        tk.Label(
            task_frame, text="Hasil Pencarian Tugas", bg=Theme.color("card_bg"),
            fg=Theme.color("text_primary"), font=Theme.font(10, "bold")
        ).pack(anchor="w", padx=12, pady=(10, 4))

        t_container, self.task_tree = create_styled_treeview(
            task_frame, ("task", "assignee", "priority", "deadline", "status"),
            ("Nama Tugas", "Penanggung Jawab", "Prioritas", "Deadline", "Status"),
            (220, 140, 100, 120, 120)
        )
        t_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _do_search(self, keyword=None):
        kw = keyword if keyword is not None else self.keyword_field.get()
        if keyword is not None:
            self.keyword_field.set(keyword)

        meetings = MeetingController.search_meetings(kw)
        tasks = TaskController.search_tasks(kw)

        m_rows = [(m.title, format_date_display(m.date), m.time, m.location or "-", m.chairperson or "-") for m in meetings]
        t_rows = [(t.task_name, t.assignee or "-", t.priority, format_date_display(t.deadline), t.status) for t in tasks]

        populate_treeview(self.meeting_tree, m_rows)
        populate_treeview(self.task_tree, t_rows)

    def _do_filter_tasks(self):
        status = self.status_filter.get()
        tasks = TaskController.filter_tasks(
            status=status if status != "Semua" else None,
            assignee=self.assignee_filter.get() or None,
            date_from=self.date_from_filter.get() or None,
            date_to=self.date_to_filter.get() or None,
        )
        t_rows = [(t.task_name, t.assignee or "-", t.priority, format_date_display(t.deadline), t.status) for t in tasks]
        populate_treeview(self.task_tree, t_rows)

    def focus_search(self, keyword):
        """Dipanggil dari topbar quick search."""
        self._do_search(keyword)
