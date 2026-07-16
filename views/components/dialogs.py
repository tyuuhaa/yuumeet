"""
dialogs.py
Komponen dialog modal kustom (pengganti tampilan messagebox bawaan yang kuno)
dan ScrollableFrame untuk konten panjang.
"""

import tkinter as tk
from utils.theme import Theme
from views.components.widgets import ModernButton


class ModalDialog(tk.Toplevel):
    """Dialog modal dasar dengan header bergaya modern."""

    def __init__(self, parent, title="Dialog", width=520, height=560):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.configure(bg=Theme.color("bg_primary"))
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self._center(parent, width, height)

        header = tk.Frame(self, bg=Theme.color("bg_sidebar"), height=54)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header, text=title, bg=Theme.color("bg_sidebar"),
            fg=Theme.color("text_on_sidebar"), font=Theme.font(13, "bold")
        ).pack(side="left", padx=20, pady=14)

        close_btn = tk.Label(
            header, text="✕", bg=Theme.color("bg_sidebar"), fg=Theme.color("text_on_sidebar"),
            font=Theme.font(12, "bold"), cursor="hand2"
        )
        close_btn.pack(side="right", padx=20)
        close_btn.bind("<Button-1>", lambda e: self.destroy())

        self.content = tk.Frame(self, bg=Theme.color("bg_primary"))
        self.content.pack(fill="both", expand=True, padx=24, pady=18)

    def _center(self, parent, width, height):
        parent.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{max(x,0)}+{max(y,0)}")


class ConfirmDialog(ModalDialog):
    """Dialog konfirmasi sebelum menghapus data (menggantikan messagebox default)."""

    def __init__(self, parent, message, on_confirm):
        super().__init__(parent, title="Konfirmasi", width=380, height=180)
        self.on_confirm = on_confirm

        tk.Label(
            self.content, text=message, bg=Theme.color("bg_primary"),
            fg=Theme.color("text_primary"), font=Theme.font(10), wraplength=320, justify="left"
        ).pack(pady=(10, 20))

        btn_frame = tk.Frame(self.content, bg=Theme.color("bg_primary"))
        btn_frame.pack(fill="x")

        ModernButton(
            btn_frame, "Batal", command=self.destroy,
            bg=Theme.color("border"), fg=Theme.color("text_primary"),
            hover_bg=Theme.color("border")
        ).pack(side="right", padx=(8, 0))

        ModernButton(
            btn_frame, "Hapus", command=self._confirm,
            bg=Theme.color("danger"), hover_bg="#C13A3E"
        ).pack(side="right")

    def _confirm(self):
        self.destroy()
        if self.on_confirm:
            self.on_confirm()


class InfoDialog(ModalDialog):
    """Dialog notifikasi info/sukses/error sederhana."""

    def __init__(self, parent, title, message, kind="info"):
        super().__init__(parent, title=title, width=380, height=180)
        color = {
            "success": Theme.color("success"),
            "error": Theme.color("danger"),
            "info": Theme.color("accent"),
        }.get(kind, Theme.color("accent"))

        icon = {"success": "✓", "error": "✕", "info": "ℹ"}.get(kind, "ℹ")

        tk.Label(
            self.content, text=icon, bg=Theme.color("bg_primary"), fg=color,
            font=Theme.font(24, "bold")
        ).pack(pady=(6, 6))

        tk.Label(
            self.content, text=message, bg=Theme.color("bg_primary"),
            fg=Theme.color("text_primary"), font=Theme.font(10), wraplength=320, justify="center"
        ).pack(pady=(0, 16))

        ModernButton(self.content, "OK", command=self.destroy).pack()


class ScrollableFrame(tk.Frame):
    """Frame dengan scrollbar vertikal, untuk konten panjang seperti form."""

    def __init__(self, parent, bg=None):
        bg = bg or Theme.color("bg_primary")
        super().__init__(parent, bg=bg)

        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self._bind_mousewheel()

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _bind_mousewheel(self):
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
