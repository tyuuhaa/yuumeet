"""
settings_view.py
Halaman User Settings: dark/light mode, warna tema, backup & restore database,
dan lokasi penyimpanan data.
"""

import os
import tkinter as tk
from tkinter import filedialog
from utils.theme import Theme
from controllers.settings_controller import SettingsController
from views.components.cards import Card
from views.components.widgets import ModernButton
from views.components.dialogs import InfoDialog, ConfirmDialog


class SettingsView(tk.Frame):
    def __init__(self, parent, controller_app):
        super().__init__(parent, bg=Theme.color("bg_primary"))
        self.controller_app = controller_app
        self._build()

    def _build(self):
        header = tk.Frame(self, bg=Theme.color("bg_primary"))
        header.pack(fill="x", padx=25, pady=(20, 10))
        tk.Label(
            header, text="Pengaturan Aplikasi", bg=Theme.color("bg_primary"),
            fg=Theme.color("text_primary"), font=Theme.font(13, "bold")
        ).pack(anchor="w")

        body = tk.Frame(self, bg=Theme.color("bg_primary"))
        body.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        # Tema
        theme_card = Card(body, title="🎨 Tampilan", width=420)
        theme_card.pack(side="left", fill="y", padx=(0, 15))

        tk.Label(
            theme_card.body, text="Mode Tampilan", bg=Theme.color("card_bg"),
            fg=Theme.color("text_secondary"), font=Theme.font(9)
        ).pack(anchor="w", pady=(0, 6))

        mode_row = tk.Frame(theme_card.body, bg=Theme.color("card_bg"))
        mode_row.pack(fill="x", pady=(0, 15))
        current_mode = Theme.get_mode()

        self.light_btn = ModernButton(
            mode_row, "☀ Light Mode", command=lambda: self._set_theme("light"),
            bg=Theme.color("accent") if current_mode == "light" else Theme.color("border"),
            fg="white" if current_mode == "light" else Theme.color("text_primary")
        )
        self.light_btn.pack(side="left", padx=(0, 8))

        self.dark_btn = ModernButton(
            mode_row, "🌙 Dark Mode", command=lambda: self._set_theme("dark"),
            bg=Theme.color("accent") if current_mode == "dark" else Theme.color("border"),
            fg="white" if current_mode == "dark" else Theme.color("text_primary")
        )
        self.dark_btn.pack(side="left")

        tk.Label(
            theme_card.body, text="Warna Aksen Tema", bg=Theme.color("card_bg"),
            fg=Theme.color("text_secondary"), font=Theme.font(9)
        ).pack(anchor="w", pady=(10, 6))

        color_row = tk.Frame(theme_card.body, bg=Theme.color("card_bg"))
        color_row.pack(fill="x")
        accent_colors = ["#1E3A5F", "#2F6FED", "#22A06B", "#E5484D", "#6D4AAF"]
        for color in accent_colors:
            swatch = tk.Label(color_row, bg=color, width=3, height=1, cursor="hand2")
            swatch.pack(side="left", padx=4)
            swatch.bind("<Button-1>", lambda e, c=color: self._set_accent_color(c))

        # Backup & Restore
        backup_card = Card(body, title="💾 Backup & Restore Database", width=420)
        backup_card.pack(side="left", fill="y", padx=(0, 15))

        tk.Label(
            backup_card.body,
            text="Simpan salinan database secara berkala untuk mencegah kehilangan data.",
            bg=Theme.color("card_bg"), fg=Theme.color("text_secondary"), font=Theme.font(9),
            wraplength=360, justify="left"
        ).pack(anchor="w", pady=(0, 15))

        ModernButton(backup_card.body, "Backup Database Sekarang", icon="📦",
                     command=self._backup_now).pack(fill="x", pady=4)
        ModernButton(backup_card.body, "Restore dari Backup", icon="♻",
                     bg=Theme.color("warning"), hover_bg="#D6941F",
                     command=self._restore_dialog).pack(fill="x", pady=4)

        self.backup_list_label = tk.Label(
            backup_card.body, text="", bg=Theme.color("card_bg"),
            fg=Theme.color("text_secondary"), font=Theme.font(8), justify="left", anchor="w"
        )
        self.backup_list_label.pack(fill="x", pady=(10, 0))
        self._refresh_backup_list()

        # Lokasi Penyimpanan
        location_card = Card(body, title="📁 Lokasi Penyimpanan Data")
        location_card.pack(side="left", fill="both", expand=True)

        current_location = SettingsController.get_data_location() or "Default (folder aplikasi)"
        tk.Label(
            location_card.body, text="Lokasi database saat ini:", bg=Theme.color("card_bg"),
            fg=Theme.color("text_secondary"), font=Theme.font(9)
        ).pack(anchor="w")
        self.location_label = tk.Label(
            location_card.body, text=current_location, bg=Theme.color("card_bg"),
            fg=Theme.color("text_primary"), font=Theme.font(9, "bold"), wraplength=380, justify="left"
        )
        self.location_label.pack(anchor="w", pady=(4, 15))

        ModernButton(
            location_card.body, "Pilih Folder Penyimpanan Baru", icon="📂",
            command=self._choose_location
        ).pack(fill="x")

        tk.Label(
            location_card.body,
            text="Catatan: perubahan lokasi penyimpanan akan diterapkan setelah aplikasi dimulai ulang.",
            bg=Theme.color("card_bg"), fg=Theme.color("text_secondary"), font=Theme.font(8),
            wraplength=380, justify="left"
        ).pack(anchor="w", pady=(15, 0))

    def _set_theme(self, mode):
        SettingsController.set_theme_mode(mode)
        InfoDialog(self, "Tema Diubah", f"Mode {mode} diterapkan. Memuat ulang tampilan...", kind="success")
        self.controller_app.apply_theme(mode)

    def _set_accent_color(self, color):
        SettingsController.set_accent_color(color)
        InfoDialog(self, "Warna Diubah", "Warna aksen tema berhasil disimpan.", kind="success")

    def _backup_now(self):
        path = SettingsController.backup_database()
        InfoDialog(self, "Backup Berhasil", f"Database berhasil dibackup ke:\n{path}", kind="success")
        self._refresh_backup_list()

    def _refresh_backup_list(self):
        backups = SettingsController.list_backups()
        if backups:
            text = "Backup terbaru:\n" + "\n".join(os.path.basename(b) for b in backups[:5])
        else:
            text = "Belum ada backup."
        self.backup_list_label.config(text=text)

    def _restore_dialog(self):
        backups = SettingsController.list_backups()
        if not backups:
            InfoDialog(self, "Tidak Ada Backup", "Belum ada file backup yang tersedia.", kind="error")
            return

        filepath = filedialog.askopenfilename(
            title="Pilih file backup untuk direstore",
            initialdir=os.path.dirname(backups[0]),
            filetypes=[("Database SQLite", "*.db")]
        )
        if not filepath:
            return

        def do_restore():
            SettingsController.restore_database(filepath)
            InfoDialog(self, "Restore Berhasil", "Database berhasil direstore. Silakan mulai ulang aplikasi.", kind="success")

        ConfirmDialog(
            self, f"Yakin ingin merestore database dari:\n{os.path.basename(filepath)}?\nData saat ini akan digantikan.",
            on_confirm=do_restore
        )

    def _choose_location(self):
        folder = filedialog.askdirectory(title="Pilih folder penyimpanan data")
        if folder:
            SettingsController.set_data_location(folder)
            self.location_label.config(text=folder)
            InfoDialog(self, "Lokasi Disimpan", "Lokasi penyimpanan data berhasil diperbarui.", kind="success")
