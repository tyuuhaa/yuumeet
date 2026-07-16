"""
form_fields.py
Komponen input form dengan style modern (label + entry/combobox/textarea),
digunakan berulang di form Meeting dan Task agar tidak ada duplikasi kode.
"""

import tkinter as tk
from tkinter import ttk
from utils.theme import Theme


class LabeledEntry(tk.Frame):
    def __init__(self, parent, label, placeholder="", show=None, width=None):
        super().__init__(parent, bg=Theme.color("bg_primary"))
        tk.Label(
            self, text=label, bg=Theme.color("bg_primary"),
            fg=Theme.color("text_primary"), font=Theme.font(9, "bold")
        ).pack(anchor="w", pady=(0, 4))

        self.var = tk.StringVar()
        entry_kwargs = {"show": show} if show else {}
        self.entry = tk.Entry(
            self, textvariable=self.var, font=Theme.font(10),
            bg=Theme.color("bg_secondary"), fg=Theme.color("text_primary"),
            insertbackground=Theme.color("text_primary"),
            highlightthickness=1, highlightbackground=Theme.color("border"),
            highlightcolor=Theme.color("accent"), relief="flat", **entry_kwargs
        )
        self.entry.pack(fill="x", ipady=7)
        if width:
            self.entry.config(width=width)

        self.error_label = tk.Label(
            self, text="", bg=Theme.color("bg_primary"),
            fg=Theme.color("danger"), font=Theme.font(8)
        )
        self.error_label.pack(anchor="w")

        if placeholder:
            self._set_placeholder(placeholder)

    def _set_placeholder(self, placeholder):
        self.entry.insert(0, placeholder)
        self.entry.config(fg=Theme.color("text_secondary"))

        def on_focus_in(e):
            if self.entry.get() == placeholder:
                self.entry.delete(0, tk.END)
                self.entry.config(fg=Theme.color("text_primary"))

        def on_focus_out(e):
            if not self.entry.get():
                self.entry.insert(0, placeholder)
                self.entry.config(fg=Theme.color("text_secondary"))

        self.entry.bind("<FocusIn>", on_focus_in)
        self.entry.bind("<FocusOut>", on_focus_out)

    def get(self):
        return self.var.get().strip()

    def set(self, value):
        self.var.set(value)
        self.entry.config(fg=Theme.color("text_primary"))

    def show_error(self, message):
        self.error_label.config(text=message)
        self.entry.config(highlightbackground=Theme.color("danger"))

    def clear_error(self):
        self.error_label.config(text="")
        self.entry.config(highlightbackground=Theme.color("border"))


class LabeledCombobox(tk.Frame):
    def __init__(self, parent, label, values, default=None):
        super().__init__(parent, bg=Theme.color("bg_primary"))
        tk.Label(
            self, text=label, bg=Theme.color("bg_primary"),
            fg=Theme.color("text_primary"), font=Theme.font(9, "bold")
        ).pack(anchor="w", pady=(0, 4))

        style = ttk.Style()
        style.configure("Modern.TCombobox", padding=6)

        self.var = tk.StringVar(value=default or (values[0] if values else ""))
        self.combo = ttk.Combobox(
            self, textvariable=self.var, values=values, state="readonly",
            font=Theme.font(10), style="Modern.TCombobox"
        )
        self.combo.pack(fill="x", ipady=4)

    def get(self):
        return self.var.get()

    def set(self, value):
        self.var.set(value)


class LabeledTextArea(tk.Frame):
    def __init__(self, parent, label, height=5):
        super().__init__(parent, bg=Theme.color("bg_primary"))
        tk.Label(
            self, text=label, bg=Theme.color("bg_primary"),
            fg=Theme.color("text_primary"), font=Theme.font(9, "bold")
        ).pack(anchor="w", pady=(0, 4))

        frame = tk.Frame(self, highlightthickness=1, highlightbackground=Theme.color("border"))
        frame.pack(fill="both", expand=True)

        self.text = tk.Text(
            frame, height=height, font=Theme.font(10), bg=Theme.color("bg_secondary"),
            fg=Theme.color("text_primary"), insertbackground=Theme.color("text_primary"),
            relief="flat", wrap="word", padx=8, pady=8
        )
        self.text.pack(fill="both", expand=True)

    def get(self):
        return self.text.get("1.0", "end").strip()

    def set(self, value):
        self.text.delete("1.0", "end")
        self.text.insert("1.0", value or "")

    def bind_autosave(self, callback, delay_ms=1200):
        """Memicu callback autosave beberapa saat setelah user berhenti mengetik."""
        self._autosave_job = None

        def on_key(event):
            if self._autosave_job:
                self.after_cancel(self._autosave_job)
            self._autosave_job = self.after(delay_ms, callback)

        self.text.bind("<KeyRelease>", on_key)


class DateEntry(LabeledEntry):
    """Entry khusus tanggal dengan placeholder format YYYY-MM-DD."""

    def __init__(self, parent, label, default_today=False):
        super().__init__(parent, label, placeholder="YYYY-MM-DD")
        if default_today:
            from utils.helpers import today_str
            self.set(today_str())


class TimeEntry(LabeledEntry):
    """Entry khusus waktu dengan placeholder format HH:MM."""

    def __init__(self, parent, label):
        super().__init__(parent, label, placeholder="HH:MM")
