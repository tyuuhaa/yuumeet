"""
minutes_view.py
Dialog untuk mencatat notulen rapat: pembahasan agenda, keputusan, dan catatan tambahan.
Notulen disimpan otomatis (auto-save) setelah user berhenti mengetik.
"""

import tkinter as tk
from utils.theme import Theme
from controllers.minutes_controller import MinutesController
from views.components.dialogs import ModalDialog, ScrollableFrame
from views.components.form_fields import LabeledTextArea


class MinutesDialog(ModalDialog):
    def __init__(self, parent, meeting):
        super().__init__(parent, title=f"Notulen: {meeting.title}", width=620, height=650)
        self.meeting = meeting
        self._build()

    def _build(self):
        info_row = tk.Frame(self.content, bg=Theme.color("bg_primary"))
        info_row.pack(fill="x", pady=(0, 10))
        tk.Label(
            info_row, text=f"{self.meeting.date}  •  {self.meeting.time}  •  {self.meeting.location or '-'}",
            bg=Theme.color("bg_primary"), fg=Theme.color("text_secondary"), font=Theme.font(9)
        ).pack(anchor="w")

        self.status_label = tk.Label(
            self.content, text="", bg=Theme.color("bg_primary"),
            fg=Theme.color("success"), font=Theme.font(8, "bold")
        )
        self.status_label.pack(anchor="e")

        scroll = ScrollableFrame(self.content)
        scroll.pack(fill="both", expand=True)
        form = scroll.scrollable_frame

        existing = MinutesController.get_minutes(self.meeting.id)

        self.discussion_field = LabeledTextArea(form, "Hasil Pembahasan Agenda", height=6)
        self.discussion_field.pack(fill="x", pady=6)
        self.discussion_field.set(existing["discussion"])

        self.decisions_field = LabeledTextArea(form, "Keputusan Rapat", height=5)
        self.decisions_field.pack(fill="x", pady=6)
        self.decisions_field.set(existing["decisions"])

        self.notes_field = LabeledTextArea(form, "Catatan Tambahan", height=4)
        self.notes_field.pack(fill="x", pady=6)
        self.notes_field.set(existing["additional_notes"])

        # Auto-save setiap field
        self.discussion_field.bind_autosave(self._autosave)
        self.decisions_field.bind_autosave(self._autosave)
        self.notes_field.bind_autosave(self._autosave)

    def _autosave(self):
        MinutesController.auto_save(
            self.meeting.id, self.discussion_field.get(),
            self.decisions_field.get(), self.notes_field.get()
        )
        self.status_label.config(text="✓ Tersimpan otomatis")
        self.after(2000, lambda: self.status_label.config(text=""))
