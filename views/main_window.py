"""
main_window.py
Window utama aplikasi yang menggabungkan Sidebar, Topbar, dan area konten
yang berganti-ganti sesuai menu yang dipilih (mirip layout Notion/Trello).
"""

import tkinter as tk
from utils.theme import Theme
from controllers.settings_controller import SettingsController
from views.components.sidebar import Sidebar
from views.components.topbar import Topbar
from views.dashboard_view import DashboardView
from views.meeting_view import MeetingView
from views.task_view import TaskView
from views.calendar_view import CalendarView
from views.search_view import SearchView
from views.report_view import ReportView
from views.settings_view import SettingsView

PAGE_TITLES = {
    "dashboard": "Dashboard",
    "meetings": "Meeting Management",
    "tasks": "Action Items (Tugas)",
    "calendar": "Calendar & Timeline",
    "search": "Pencarian & Filter",
    "reports": "Laporan",
    "settings": "Pengaturan",
}


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Terapkan tema tersimpan sebelum membangun UI
        saved_mode = SettingsController.get_theme_mode()
        Theme.set_mode(saved_mode)

        self.title("Event Meeting Minutes Manager")
        self.geometry("1280x800")
        self.minsize(1024, 650)
        self.configure(bg=Theme.color("bg_primary"))

        self._current_page = "dashboard"
        self._pages = {}

        self._build_layout()
        self._bind_shortcuts()
        self.navigate("dashboard")

    def _build_layout(self):
        self.main_container = tk.Frame(self, bg=Theme.color("bg_primary"))
        self.main_container.pack(fill="both", expand=True)

        self.sidebar = Sidebar(self.main_container, on_navigate=self.navigate, current=self._current_page)
        self.sidebar.pack(side="left", fill="y")

        right_container = tk.Frame(self.main_container, bg=Theme.color("bg_primary"))
        right_container.pack(side="left", fill="both", expand=True)

        self.topbar = Topbar(right_container, title=PAGE_TITLES["dashboard"], on_search=self._on_quick_search)
        self.topbar.pack(fill="x")

        self.content_area = tk.Frame(right_container, bg=Theme.color("bg_primary"))
        self.content_area.pack(fill="both", expand=True)

    def _bind_shortcuts(self):
        # Shortcut keyboard global untuk navigasi cepat antar menu
        self.bind("<Control-Key-1>", lambda e: self.navigate("dashboard"))
        self.bind("<Control-Key-2>", lambda e: self.navigate("meetings"))
        self.bind("<Control-Key-3>", lambda e: self.navigate("tasks"))
        self.bind("<Control-Key-4>", lambda e: self.navigate("calendar"))
        self.bind("<Control-Key-5>", lambda e: self.navigate("search"))
        self.bind("<Control-Key-6>", lambda e: self.navigate("reports"))
        self.bind("<Control-Key-7>", lambda e: self.navigate("settings"))
        self.bind("<Control-f>", lambda e: self.navigate("search"))

    def navigate(self, page_key):
        self._current_page = page_key
        self.sidebar.set_active(page_key)
        self.topbar.set_title(PAGE_TITLES.get(page_key, page_key.title()))

        for widget in self.content_area.winfo_children():
            widget.pack_forget()

        if page_key not in self._pages:
            self._pages[page_key] = self._create_page(page_key)

        page = self._pages[page_key]
        # Refresh data setiap kali halaman dibuka (kecuali settings/report yang statis ringan)
        if hasattr(page, "refresh"):
            page.refresh()
        page.pack(fill="both", expand=True)

    def _create_page(self, page_key):
        mapping = {
            "dashboard": DashboardView,
            "meetings": MeetingView,
            "tasks": TaskView,
            "calendar": CalendarView,
            "search": SearchView,
            "reports": ReportView,
            "settings": SettingsView,
        }
        view_class = mapping.get(page_key, DashboardView)
        return view_class(self.content_area, self)

    def _on_quick_search(self, keyword):
        self.navigate("search")
        page = self._pages.get("search")
        if page and keyword:
            page.focus_search(keyword)

    def apply_theme(self, mode):
        """Menerapkan tema baru dengan membangun ulang seluruh layout."""
        Theme.set_mode(mode)
        current = self._current_page
        self.main_container.destroy()
        self._pages = {}
        self._build_layout()
        self.navigate(current)
