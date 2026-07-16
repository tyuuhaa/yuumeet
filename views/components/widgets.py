"""
widgets.py
Kumpulan widget custom: tombol modern dengan hover effect, tabel zebra-stripe (Treeview),
badge status/prioritas, dan tooltip sederhana.
"""

import tkinter as tk
from tkinter import ttk
from utils.theme import Theme


class ModernButton(tk.Label):
    """Tombol berbasis Label agar tampilan lebih modern & mendukung hover custom."""

    def __init__(self, parent, text, command=None, bg=None, fg="white",
                 hover_bg=None, font_size=10, padx=18, pady=9, icon=""):
        self.bg_color = bg or Theme.color("accent")
        self.hover_bg = hover_bg or Theme.color("accent_hover")
        self.command = command
        display_text = f"{icon}  {text}" if icon else text
        super().__init__(
            parent, text=display_text, bg=self.bg_color, fg=fg,
            font=Theme.font(font_size, "bold"), padx=padx, pady=pady, cursor="hand2"
        )
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _on_enter(self, e):
        self.config(bg=self.hover_bg)

    def _on_leave(self, e):
        self.config(bg=self.bg_color)

    def _on_click(self, e):
        if self.command:
            self.command()

    def set_enabled(self, enabled):
        if enabled:
            self.config(state="normal", cursor="hand2")
        else:
            self.config(state="disabled", cursor="arrow")


class Badge(tk.Label):
    """Label kecil berwarna untuk menampilkan status/prioritas."""

    def __init__(self, parent, text, color):
        super().__init__(
            parent, text=text, bg=color, fg="white",
            font=Theme.font(8, "bold"), padx=8, pady=2
        )


def create_styled_treeview(parent, columns, headings, col_widths=None):
    """
    Membuat Treeview dengan style zebra-stripe modern.
    Mengembalikan (frame_container, treeview).
    """
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Modern.Treeview",
        background=Theme.color("table_row_odd"),
        foreground=Theme.color("text_primary"),
        fieldbackground=Theme.color("table_row_odd"),
        rowheight=32,
        font=Theme.font(9),
        borderwidth=0
    )
    style.configure(
        "Modern.Treeview.Heading",
        background=Theme.color("table_header"),
        foreground=Theme.color("table_header_text"),
        font=Theme.font(9, "bold"),
        borderwidth=0,
        relief="flat"
    )
    style.map("Modern.Treeview.Heading", background=[("active", Theme.color("table_header"))])
    style.map(
        "Modern.Treeview",
        background=[("selected", Theme.color("accent"))],
        foreground=[("selected", "white")]
    )

    container = tk.Frame(parent, bg=Theme.color("card_bg"))

    tree = ttk.Treeview(container, columns=columns, show="headings", style="Modern.Treeview")
    for i, col in enumerate(columns):
        tree.heading(col, text=headings[i])
        width = col_widths[i] if col_widths else 120
        tree.column(col, width=width, anchor="w")

    tree.tag_configure("oddrow", background=Theme.color("table_row_odd"))
    tree.tag_configure("evenrow", background=Theme.color("table_row_even"))

    vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

    return container, tree


def populate_treeview(tree, rows):
    """Mengisi treeview dengan data & menerapkan zebra-stripe otomatis."""
    tree.delete(*tree.get_children())
    for i, row in enumerate(rows):
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        tree.insert("", "end", values=row, tags=(tag,))


class Tooltip:
    """Tooltip sederhana untuk widget (muncul saat hover)."""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, text=self.text, bg="#333333", fg="white",
            font=Theme.font(8), padx=8, pady=4
        )
        label.pack()

    def hide(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


class LoadingIndicator(tk.Frame):
    """Indikator loading sederhana dengan animasi titik berjalan."""

    def __init__(self, parent, text="Memuat"):
        super().__init__(parent, bg=Theme.color("bg_primary"))
        self.label = tk.Label(
            self, text=text, bg=Theme.color("bg_primary"),
            fg=Theme.color("text_secondary"), font=Theme.font(10)
        )
        self.label.pack()
        self._dots = 0
        self._running = False

    def start(self):
        self._running = True
        self._animate()

    def stop(self):
        self._running = False

    def _animate(self):
        if not self._running:
            return
        self._dots = (self._dots + 1) % 4
        self.label.config(text=f"Memuat{'.' * self._dots}")
        self.after(400, self._animate)
