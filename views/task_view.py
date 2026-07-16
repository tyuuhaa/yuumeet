"""
task_view.py
Halaman Action Items (Tugas): daftar tugas dengan filter status, form tambah/edit,
dan drag & drop sederhana untuk mengubah status.
"""

import tkinter as tk
from utils.theme import Theme
from utils.helpers import format_date_display, days_until
from controllers.task_controller import TaskController
from controllers.meeting_controller import MeetingController
from utils.validators import ValidationError
from models.action_item_model import ActionItem
from views.components.widgets import create_styled_treeview, populate_treeview, ModernButton, Badge
from views.components.dialogs import ModalDialog, ConfirmDialog, InfoDialog
from views.components.form_fields import LabeledEntry, LabeledCombobox, DateEntry


class TaskView(tk.Frame):
    def __init__(self, parent, controller_app):
        super().__init__(parent, bg=Theme.color("bg_primary"))
        self.controller_app = controller_app
        self.tasks = []
        self._build()
        self.refresh()

    def _build(self):
        top_bar = tk.Frame(self, bg=Theme.color("bg_primary"))
        top_bar.pack(fill="x", padx=25, pady=(20, 10))

        tk.Label(
            top_bar, text="Action Items (Tugas)", bg=Theme.color("bg_primary"),
            fg=Theme.color("text_primary"), font=Theme.font(13, "bold")
        ).pack(side="left")

        ModernButton(top_bar, "Tambah Tugas", icon="➕", command=self.open_create_form).pack(side="right")

        # Filter bar
        filter_bar = tk.Frame(self, bg=Theme.color("bg_primary"))
        filter_bar.pack(fill="x", padx=25, pady=(0, 10))

        self.status_filter = LabeledCombobox(filter_bar, "Filter Status", ["Semua"] + ActionItem.STATUSES, default="Semua")
        self.status_filter.pack(side="left", padx=(0, 10))
        self.status_filter.combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filter())

        self.priority_filter = LabeledCombobox(filter_bar, "Filter Prioritas", ["Semua"] + ActionItem.PRIORITIES, default="Semua")
        self.priority_filter.pack(side="left", padx=(0, 10))
        self.priority_filter.combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filter())

        self.assignee_filter = LabeledEntry(filter_bar, "Filter Penanggung Jawab")
        self.assignee_filter.pack(side="left", padx=(0, 10))
        self.assignee_filter.entry.bind("<KeyRelease>", lambda e: self.apply_filter())

        table_frame = tk.Frame(self, bg=Theme.color("card_bg"), highlightthickness=1,
                                highlightbackground=Theme.color("border"))
        table_frame.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        columns = ("task", "assignee", "priority", "deadline", "status")
        headings = ("Nama Tugas", "Penanggung Jawab", "Prioritas", "Deadline", "Status")
        widths = (250, 150, 100, 130, 130)

        container, self.tree = create_styled_treeview(table_frame, columns, headings, widths)
        container.pack(fill="both", expand=True, padx=1, pady=1)

        self.tree.bind("<Double-1>", self._on_row_double_click)
        self.tree.bind("<Button-3>", self._on_right_click)

        self._build_context_menu()

    def _build_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="✏ Edit Tugas", command=lambda: self.open_edit_form(self._selected_task()))
        submenu = tk.Menu(self.context_menu, tearoff=0)
        for status in ActionItem.STATUSES:
            submenu.add_command(label=status, command=lambda s=status: self._change_status(s))
        self.context_menu.add_cascade(label="🔄 Ubah Status", menu=submenu)
        self.context_menu.add_command(label="🗑 Hapus Tugas", command=lambda: self._confirm_delete(self._selected_task()))

    def _on_right_click(self, event):
        row_id = self.tree.identify_row(event.y)
        if row_id:
            self.tree.selection_set(row_id)
            self.context_menu.tk_popup(event.x_root, event.y_root)

    def _selected_task(self):
        selection = self.tree.selection()
        if not selection:
            return None
        index = self.tree.index(selection[0])
        return self.tasks[index] if index < len(self.tasks) else None

    def _on_row_double_click(self, event):
        task = self._selected_task()
        if task:
            self.open_edit_form(task)

    def _change_status(self, status):
        task = self._selected_task()
        if task:
            TaskController.update_status(task.id, status)
            self.refresh()

    def refresh(self):
        self.tasks = TaskController.get_all_tasks()
        self._render_rows(self.tasks)

    def apply_filter(self):
        status = self.status_filter.get()
        priority = self.priority_filter.get()
        assignee = self.assignee_filter.get()
        self.tasks = TaskController.filter_tasks(
            status=status if status != "Semua" else None,
            priority=priority if priority != "Semua" else None,
            assignee=assignee if assignee else None
        )
        self._render_rows(self.tasks)

    def search(self, keyword):
        self.tasks = TaskController.search_tasks(keyword)
        self._render_rows(self.tasks)

    def _render_rows(self, tasks):
        rows = []
        for t in tasks:
            days = days_until(t.deadline)
            deadline_text = format_date_display(t.deadline)
            if days is not None and days < 0 and t.status != "Done":
                deadline_text += " ⚠"
            rows.append((t.task_name, t.assignee or "-", t.priority, deadline_text, t.status))
        populate_treeview(self.tree, rows)

    def open_create_form(self):
        TaskFormDialog(self, on_saved=self.refresh)

    def open_edit_form(self, task):
        if task:
            TaskFormDialog(self, task=task, on_saved=self.refresh)

    def _confirm_delete(self, task):
        if not task:
            return

        def do_delete():
            TaskController.delete_task(task.id)
            self.refresh()
            InfoDialog(self, "Berhasil", "Tugas berhasil dihapus.", kind="success")

        ConfirmDialog(self, f"Yakin ingin menghapus tugas '{task.task_name}'?", on_confirm=do_delete)


class TaskFormDialog(ModalDialog):
    """Form modal untuk menambah atau mengedit Action Item."""

    def __init__(self, parent, task=None, on_saved=None):
        title = "Edit Tugas" if task else "Tambah Tugas Baru"
        super().__init__(parent, title=title, width=480, height=560)
        self.task = task
        self.on_saved = on_saved
        self._build_form()

    def _build_form(self):
        form = self.content

        self.name_field = LabeledEntry(form, "Nama Tugas *")
        self.name_field.pack(fill="x", pady=6)

        self.assignee_field = LabeledEntry(form, "Penanggung Jawab *")
        self.assignee_field.pack(fill="x", pady=6)

        row = tk.Frame(form, bg=Theme.color("bg_primary"))
        row.pack(fill="x", pady=6)
        self.priority_field = LabeledCombobox(row, "Prioritas *", ActionItem.PRIORITIES, default="Medium")
        self.priority_field.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.status_field = LabeledCombobox(row, "Status *", ActionItem.STATUSES, default="To Do")
        self.status_field.pack(side="left", fill="x", expand=True)

        self.deadline_field = DateEntry(form, "Deadline *", default_today=True)
        self.deadline_field.pack(fill="x", pady=6)

        meetings = MeetingController.get_all_meetings()
        meeting_options = ["Tidak terkait rapat"] + [f"{m.id} - {m.title}" for m in meetings]
        self.meeting_field = LabeledCombobox(form, "Terkait Rapat (opsional)", meeting_options, default=meeting_options[0])
        self.meeting_field.pack(fill="x", pady=6)

        if self.task:
            self.name_field.set(self.task.task_name)
            self.assignee_field.set(self.task.assignee)
            self.priority_field.set(self.task.priority)
            self.status_field.set(self.task.status)
            self.deadline_field.set(self.task.deadline)
            if self.task.meeting_id:
                for opt in meeting_options:
                    if opt.startswith(f"{self.task.meeting_id} -"):
                        self.meeting_field.set(opt)
                        break

        btn_row = tk.Frame(form, bg=Theme.color("bg_primary"))
        btn_row.pack(fill="x", pady=(20, 5))
        ModernButton(btn_row, "Simpan", icon="💾", command=self._save).pack(side="right")
        ModernButton(
            btn_row, "Batal", command=self.destroy, bg=Theme.color("border"),
            fg=Theme.color("text_primary"), hover_bg=Theme.color("border")
        ).pack(side="right", padx=(0, 8))

        self.bind("<Control-s>", lambda e: self._save())

    def _save(self):
        try:
            meeting_value = self.meeting_field.get()
            meeting_id = None
            if meeting_value != "Tidak terkait rapat":
                meeting_id = int(meeting_value.split(" - ")[0])

            if self.task:
                TaskController.update_task(
                    self.task.id, self.name_field.get(), self.assignee_field.get(),
                    self.priority_field.get(), self.deadline_field.get(),
                    self.status_field.get(), meeting_id
                )
            else:
                TaskController.create_task(
                    self.name_field.get(), self.assignee_field.get(),
                    self.priority_field.get(), self.deadline_field.get(),
                    self.status_field.get(), meeting_id
                )
            self.destroy()
            if self.on_saved:
                self.on_saved()
            InfoDialog(self.master, "Berhasil", "Data tugas berhasil disimpan.", kind="success")
        except ValidationError as e:
            InfoDialog(self, "Validasi Gagal", str(e), kind="error")
