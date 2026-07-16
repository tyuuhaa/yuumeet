"""
meeting_view.py
Halaman Meeting Management: daftar rapat, form tambah/edit rapat, dan riwayat.
"""

import tkinter as tk
from utils.theme import Theme
from utils.helpers import format_date_display
from controllers.meeting_controller import MeetingController
from utils.validators import ValidationError
from views.components.widgets import create_styled_treeview, populate_treeview, ModernButton
from views.components.dialogs import ModalDialog, ConfirmDialog, InfoDialog, ScrollableFrame
from views.components.form_fields import LabeledEntry, LabeledTextArea, DateEntry, TimeEntry
from views.minutes_view import MinutesDialog


class MeetingView(tk.Frame):
    def __init__(self, parent, controller_app):
        super().__init__(parent, bg=Theme.color("bg_primary"))
        self.controller_app = controller_app
        self.meetings = []
        self._build()
        self.refresh()

    def _build(self):
        top_bar = tk.Frame(self, bg=Theme.color("bg_primary"))
        top_bar.pack(fill="x", padx=25, pady=(20, 10))

        tk.Label(
            top_bar, text="Daftar Rapat", bg=Theme.color("bg_primary"),
            fg=Theme.color("text_primary"), font=Theme.font(13, "bold")
        ).pack(side="left")

        ModernButton(
            top_bar, "Tambah Rapat", icon="➕", command=self.open_create_form
        ).pack(side="right")

        table_frame = tk.Frame(self, bg=Theme.color("card_bg"), highlightthickness=1,
                                highlightbackground=Theme.color("border"))
        table_frame.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        columns = ("title", "date", "time", "location", "chairperson", "actions")
        headings = ("Judul Rapat", "Tanggal", "Waktu", "Lokasi", "Ketua Rapat", "Aksi")
        widths = (220, 100, 70, 140, 140, 160)

        container, self.tree = create_styled_treeview(table_frame, columns, headings, widths)
        container.pack(fill="both", expand=True, padx=1, pady=1)

        self.tree.bind("<Double-1>", self._on_row_double_click)
        self.tree.bind("<Button-3>", self._on_right_click)

        self._build_context_menu()

    def _build_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="📝 Buka Notulen", command=lambda: self._open_minutes(self._selected_meeting()))
        self.context_menu.add_command(label="✏ Edit Rapat", command=lambda: self.open_edit_form(self._selected_meeting()))
        self.context_menu.add_command(label="🗑 Hapus Rapat", command=lambda: self._confirm_delete(self._selected_meeting()))

    def _on_right_click(self, event):
        row_id = self.tree.identify_row(event.y)
        if row_id:
            self.tree.selection_set(row_id)
            self.context_menu.tk_popup(event.x_root, event.y_root)

    def _selected_meeting(self):
        selection = self.tree.selection()
        if not selection:
            return None
        index = self.tree.index(selection[0])
        return self.meetings[index] if index < len(self.meetings) else None

    def _on_row_double_click(self, event):
        meeting = self._selected_meeting()
        if meeting:
            self._open_minutes(meeting)

    def refresh(self, keyword=None):
        self.meetings = MeetingController.search_meetings(keyword) if keyword else MeetingController.get_all_meetings()
        rows = [
            (m.title, format_date_display(m.date), m.time, m.location or "-",
             m.chairperson or "-", "📝 Notulen  ✏ Edit  🗑 Hapus")
            for m in self.meetings
        ]
        populate_treeview(self.tree, rows)

    def open_create_form(self):
        MeetingFormDialog(self, on_saved=self.refresh)

    def open_edit_form(self, meeting):
        if meeting:
            MeetingFormDialog(self, meeting=meeting, on_saved=self.refresh)

    def _open_minutes(self, meeting):
        if meeting:
            MinutesDialog(self, meeting)

    def _confirm_delete(self, meeting):
        if not meeting:
            return

        def do_delete():
            MeetingController.delete_meeting(meeting.id)
            self.refresh()
            InfoDialog(self, "Berhasil", "Rapat berhasil dihapus.", kind="success")

        ConfirmDialog(
            self, f"Yakin ingin menghapus rapat '{meeting.title}'?\nSeluruh notulen dan tugas terkait juga akan dihapus.",
            on_confirm=do_delete
        )


class MeetingFormDialog(ModalDialog):
    """Form modal untuk menambah atau mengedit data rapat."""

    def __init__(self, parent, meeting=None, on_saved=None):
        title = "Edit Rapat" if meeting else "Tambah Rapat Baru"
        super().__init__(parent, title=title, width=560, height=640)
        self.meeting = meeting
        self.on_saved = on_saved
        self._build_form()

    def _build_form(self):
        scroll = ScrollableFrame(self.content)
        scroll.pack(fill="both", expand=True)
        form = scroll.scrollable_frame

        self.title_field = LabeledEntry(form, "Judul Rapat *")
        self.title_field.pack(fill="x", pady=6)

        date_time_row = tk.Frame(form, bg=Theme.color("bg_primary"))
        date_time_row.pack(fill="x", pady=6)
        self.date_field = DateEntry(date_time_row, "Tanggal *", default_today=True)
        self.date_field.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.time_field = TimeEntry(date_time_row, "Waktu *")
        self.time_field.pack(side="left", fill="x", expand=True)

        self.location_field = LabeledEntry(form, "Lokasi *")
        self.location_field.pack(fill="x", pady=6)

        self.chairperson_field = LabeledEntry(form, "Ketua Rapat *")
        self.chairperson_field.pack(fill="x", pady=6)

        self.participants_field = LabeledTextArea(form, "Daftar Peserta (pisahkan dengan koma)", height=3)
        self.participants_field.pack(fill="x", pady=6)

        self.agenda_field = LabeledTextArea(form, "Agenda Rapat", height=5)
        self.agenda_field.pack(fill="x", pady=6)

        if self.meeting:
            self.title_field.set(self.meeting.title)
            self.date_field.set(self.meeting.date)
            self.time_field.set(self.meeting.time)
            self.location_field.set(self.meeting.location)
            self.chairperson_field.set(self.meeting.chairperson)
            self.participants_field.set(self.meeting.participants)
            self.agenda_field.set(self.meeting.agenda)

        btn_row = tk.Frame(form, bg=Theme.color("bg_primary"))
        btn_row.pack(fill="x", pady=(15, 5))
        ModernButton(btn_row, "Simpan", icon="💾", command=self._save).pack(side="right")
        ModernButton(
            btn_row, "Batal", command=self.destroy, bg=Theme.color("border"),
            fg=Theme.color("text_primary"), hover_bg=Theme.color("border")
        ).pack(side="right", padx=(0, 8))

        # Shortcut keyboard: Ctrl+S untuk simpan
        self.bind("<Control-s>", lambda e: self._save())

    def _save(self):
        try:
            if self.meeting:
                MeetingController.update_meeting(
                    self.meeting.id, self.title_field.get(), self.date_field.get(),
                    self.time_field.get(), self.location_field.get(),
                    self.chairperson_field.get(), self.participants_field.get(),
                    self.agenda_field.get()
                )
            else:
                MeetingController.create_meeting(
                    self.title_field.get(), self.date_field.get(), self.time_field.get(),
                    self.location_field.get(), self.chairperson_field.get(),
                    self.participants_field.get(), self.agenda_field.get()
                )
            self.destroy()
            if self.on_saved:
                self.on_saved()
            InfoDialog(self.master, "Berhasil", "Data rapat berhasil disimpan.", kind="success")
        except ValidationError as e:
            InfoDialog(self, "Validasi Gagal", str(e), kind="error")
