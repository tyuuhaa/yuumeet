"""
sidebar.py
Komponen Sidebar navigasi kiri, terinspirasi dari Notion/Trello.
"""

import tkinter as tk
from utils.theme import Theme


class Sidebar(tk.Frame):
    MENU_ITEMS = [
        ("dashboard", "🏠", "Dashboard"),
        ("meetings", "📅", "Rapat"),
        ("tasks", "✅", "Tugas"),
        ("calendar", "🗓", "Kalender"),
        ("search", "🔍", "Pencarian"),
        ("reports", "📊", "Laporan"),
        ("settings", "⚙", "Pengaturan"),
    ]

    def __init__(self, parent, on_navigate, current="dashboard"):
        super().__init__(parent, bg=Theme.color("bg_sidebar"), width=230)
        self.on_navigate = on_navigate
        self.current = current
        self.buttons = {}
        self.pack_propagate(False)
        self._build()

    def _build(self):
        # Logo / Brand
        brand = tk.Frame(self, bg=Theme.color("bg_sidebar"), height=70)
        brand.pack(fill="x")
        brand.pack_propagate(False)
        tk.Label(
            brand, text="📋 YuuMeet", bg=Theme.color("bg_sidebar"),
            fg=Theme.color("text_on_sidebar"), font=Theme.font(14, "bold")
        ).pack(pady=22, padx=20, anchor="w")

        sep = tk.Frame(self, bg=Theme.color("bg_sidebar_hover"), height=1)
        sep.pack(fill="x", padx=10)

        # Menu items
        menu_frame = tk.Frame(self, bg=Theme.color("bg_sidebar"))
        menu_frame.pack(fill="both", expand=True, pady=10)

        for key, icon, label in self.MENU_ITEMS:
            btn = self._create_menu_button(menu_frame, key, icon, label)
            self.buttons[key] = btn

        # Footer
        footer = tk.Frame(self, bg=Theme.color("bg_sidebar"), height=50)
        footer.pack(fill="x", side="bottom")
        tk.Label(
            footer, text="v1.0.0", bg=Theme.color("bg_sidebar"),
            fg=Theme.color("text_secondary"), font=Theme.font(8)
        ).pack(pady=15)

        self._highlight_active()

    def _create_menu_button(self, parent, key, icon, label):
        is_active = key == self.current
        bg_color = Theme.color("bg_sidebar_active") if is_active else Theme.color("bg_sidebar")

        frame = tk.Frame(parent, bg=bg_color, cursor="hand2")
        frame.pack(fill="x", padx=10, pady=2)

        lbl = tk.Label(
            frame, text=f"  {icon}   {label}", bg=bg_color,
            fg=Theme.color("text_on_sidebar"), font=Theme.font(11),
            anchor="w", padx=8, pady=10
        )
        lbl.pack(fill="x")

        # Efek hover
        def on_enter(e):
            if self.current != key:
                frame.config(bg=Theme.color("bg_sidebar_hover"))
                lbl.config(bg=Theme.color("bg_sidebar_hover"))

        def on_leave(e):
            if self.current != key:
                frame.config(bg=Theme.color("bg_sidebar"))
                lbl.config(bg=Theme.color("bg_sidebar"))

        def on_click(e):
            self.set_active(key)
            self.on_navigate(key)

        for widget in (frame, lbl):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)

        frame.lbl = lbl
        return frame

    def set_active(self, key):
        self.current = key
        self._highlight_active()

    def _highlight_active(self):
        for key, frame in self.buttons.items():
            is_active = key == self.current
            color = Theme.color("bg_sidebar_active") if is_active else Theme.color("bg_sidebar")
            frame.config(bg=color)
            frame.lbl.config(bg=color)
