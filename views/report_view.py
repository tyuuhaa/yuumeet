"""
report_view.py
Halaman Reports: laporan rapat, laporan tugas, statistik, dan export ke PDF/Excel.
"""

import os
import subprocess
import platform
import tkinter as tk
from utils.theme import Theme
from controllers.report_controller import ReportController
from views.components.cards import Card, StatCard, ProgressBar
from views.components.widgets import ModernButton
from views.components.dialogs import InfoDialog


class ReportView(tk.Frame):
    def __init__(self, parent, controller_app):
        super().__init__(parent, bg=Theme.color("bg_primary"))
        self.controller_app = controller_app
        self.report_controller = ReportController()
        self._build()

    def _build(self):
        header = tk.Frame(self, bg=Theme.color("bg_primary"))
        header.pack(fill="x", padx=25, pady=(20, 10))
        tk.Label(
            header, text="Laporan & Statistik", bg=Theme.color("bg_primary"),
            fg=Theme.color("text_primary"), font=Theme.font(13, "bold")
        ).pack(anchor="w")

        summary = self.report_controller.get_report_summary()

        stat_row = tk.Frame(self, bg=Theme.color("bg_primary"))
        stat_row.pack(fill="x", padx=25, pady=10)
        StatCard(stat_row, "📅", "Total Rapat", summary["total_meetings"]).pack(side="left", padx=(0, 15))
        StatCard(stat_row, "✅", "Total Tugas", summary["total_tasks"]).pack(side="left", padx=(0, 15))
        StatCard(stat_row, "📈", "Persentase Selesai", f"{summary['completion_percentage']}%").pack(side="left")

        body = tk.Frame(self, bg=Theme.color("bg_primary"))
        body.pack(fill="both", expand=True, padx=25, pady=(10, 20))

        # Panel export laporan rapat
        meeting_card = Card(body, title="📄 Laporan Rapat", width=380)
        meeting_card.pack(side="left", fill="y", padx=(0, 15))
        tk.Label(
            meeting_card.body, text="Ekspor seluruh riwayat rapat beserta detailnya.",
            bg=Theme.color("card_bg"), fg=Theme.color("text_secondary"), font=Theme.font(9),
            wraplength=320, justify="left"
        ).pack(anchor="w", pady=(0, 15))
        ModernButton(meeting_card.body, "Export ke PDF", icon="📕",
                     command=self._export_meetings_pdf).pack(fill="x", pady=4)
        ModernButton(meeting_card.body, "Export ke Excel", icon="📗",
                     bg=Theme.color("success"), hover_bg="#1C8A5A",
                     command=self._export_meetings_excel).pack(fill="x", pady=4)

        # Panel export laporan tugas
        task_card = Card(body, title="✅ Laporan Tugas", width=380)
        task_card.pack(side="left", fill="y", padx=(0, 15))
        tk.Label(
            task_card.body, text="Ekspor seluruh tugas beserta status dan persentase penyelesaian.",
            bg=Theme.color("card_bg"), fg=Theme.color("text_secondary"), font=Theme.font(9),
            wraplength=320, justify="left"
        ).pack(anchor="w", pady=(0, 15))
        ModernButton(task_card.body, "Export ke PDF", icon="📕",
                     command=self._export_tasks_pdf).pack(fill="x", pady=4)
        ModernButton(task_card.body, "Export ke Excel", icon="📗",
                     bg=Theme.color("success"), hover_bg="#1C8A5A",
                     command=self._export_tasks_excel).pack(fill="x", pady=4)

        # Panel statistik & laporan lengkap
        stat_card = Card(body, title="📊 Statistik & Laporan Lengkap")
        stat_card.pack(side="left", fill="both", expand=True)

        tk.Label(
            stat_card.body, text="Statistik Jumlah Rapat per Bulan", bg=Theme.color("card_bg"),
            fg=Theme.color("text_primary"), font=Theme.font(9, "bold")
        ).pack(anchor="w")

        if summary["monthly_stats"]:
            max_total = max(t for _, t in summary["monthly_stats"]) or 1
            for ym, total in summary["monthly_stats"][-6:]:
                row = tk.Frame(stat_card.body, bg=Theme.color("card_bg"))
                row.pack(fill="x", pady=3)
                tk.Label(
                    row, text=ym, bg=Theme.color("card_bg"), fg=Theme.color("text_secondary"),
                    font=Theme.font(8), width=10, anchor="w"
                ).pack(side="left")
                ProgressBar(row, width=140, height=10, percentage=(total / max_total) * 100).pack(side="left", padx=6)
                tk.Label(
                    row, text=str(total), bg=Theme.color("card_bg"), fg=Theme.color("text_primary"), font=Theme.font(8, "bold")
                ).pack(side="left")
        else:
            tk.Label(
                stat_card.body, text="Belum ada data rapat.", bg=Theme.color("card_bg"),
                fg=Theme.color("text_secondary"), font=Theme.font(9)
            ).pack(anchor="w", pady=10)

        ModernButton(
            stat_card.body, "Export Laporan Lengkap (Excel)", icon="📦",
            command=self._export_full_excel
        ).pack(fill="x", pady=(15, 4))
        ModernButton(
            stat_card.body, "Export Statistik Bulanan (PDF)", icon="📈",
            bg=Theme.color("border"), fg=Theme.color("text_primary"), hover_bg=Theme.color("border"),
            command=self._export_stats_pdf
        ).pack(fill="x", pady=4)

    def _notify_and_open(self, filepath):
        InfoDialog(self, "Ekspor Berhasil", f"Laporan disimpan di:\n{filepath}", kind="success")
        try:
            if platform.system() == "Windows":
                os.startfile(filepath)
            elif platform.system() == "Darwin":
                subprocess.call(["open", filepath])
            else:
                subprocess.call(["xdg-open", filepath])
        except Exception:
            pass  # Jika gagal membuka otomatis, file tetap tersimpan

    def _export_meetings_pdf(self):
        path = self.report_controller.export_meetings_pdf()
        self._notify_and_open(path)

    def _export_meetings_excel(self):
        path = self.report_controller.export_meetings_excel()
        self._notify_and_open(path)

    def _export_tasks_pdf(self):
        path = self.report_controller.export_tasks_pdf()
        self._notify_and_open(path)

    def _export_tasks_excel(self):
        path = self.report_controller.export_tasks_excel()
        self._notify_and_open(path)

    def _export_full_excel(self):
        path = self.report_controller.export_full_excel()
        self._notify_and_open(path)

    def _export_stats_pdf(self):
        path = self.report_controller.export_monthly_stats_pdf()
        self._notify_and_open(path)
