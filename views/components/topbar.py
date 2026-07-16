"""
topbar.py
Komponen Topbar: judul halaman, quick search, dan profil pengguna.
"""

import tkinter as tk
from utils.theme import Theme


class Topbar(tk.Frame):
    def __init__(self, parent, title="Dashboard", on_search=None):
        super().__init__(parent, bg=Theme.color("bg_secondary"), height=64)
        self.on_search = on_search
        self.pack_propagate(False)
        self._build(title)

    def _build(self, title):
        border = tk.Frame(self, bg=Theme.color("border"), height=1)
        border.pack(fill="x", side="bottom")

        self.title_label = tk.Label(
            self, text=title, bg=Theme.color("bg_secondary"),
            fg=Theme.color("text_primary"), font=Theme.font(16, "bold")
        )
        self.title_label.pack(side="left", padx=25)

        right_frame = tk.Frame(self, bg=Theme.color("bg_secondary"))
        right_frame.pack(side="right", padx=25)

        # Quick search box
        search_frame = tk.Frame(right_frame, bg=Theme.color("bg_primary"), highlightthickness=1,
                                 highlightbackground=Theme.color("border"))
        search_frame.pack(side="left", padx=(0, 20), pady=14)

        tk.Label(search_frame, text="🔍", bg=Theme.color("bg_primary"),
                  fg=Theme.color("text_secondary"), font=Theme.font(10)).pack(side="left", padx=(8, 0))

        self.search_var = tk.StringVar()
        entry = tk.Entry(
            search_frame, textvariable=self.search_var, bg=Theme.color("bg_primary"),
            fg=Theme.color("text_primary"), font=Theme.font(10), bd=0, width=24,
            insertbackground=Theme.color("text_primary")
        )
        entry.pack(side="left", ipady=6, padx=6)
        entry.bind("<Return>", self._trigger_search)

        # Profile
        profile_frame = tk.Frame(right_frame, bg=Theme.color("bg_secondary"))
        profile_frame.pack(side="left", pady=14)
        avatar = tk.Label(
            profile_frame, text="👤", bg=Theme.color("accent"), fg="white",
            font=Theme.font(11), width=3, height=1
        )
        avatar.pack(side="left")
        tk.Label(
            profile_frame, text="Admin", bg=Theme.color("bg_secondary"),
            fg=Theme.color("text_primary"), font=Theme.font(10, "bold")
        ).pack(side="left", padx=8)

    def _trigger_search(self, event=None):
        if self.on_search:
            self.on_search(self.search_var.get())

    def set_title(self, title):
        self.title_label.config(text=title)
