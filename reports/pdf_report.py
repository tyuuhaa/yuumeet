"""
pdf_report.py
Menghasilkan laporan PDF untuk rapat dan tugas menggunakan ReportLab.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime


class PDFReportGenerator:

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            "TitleStyle", parent=self.styles["Title"], textColor=colors.HexColor("#1E3A5F")
        )
        self.subtitle_style = ParagraphStyle(
            "SubtitleStyle", parent=self.styles["Normal"], textColor=colors.HexColor("#6B7280"),
            fontSize=10
        )

    def _base_doc(self, filepath):
        return SimpleDocTemplate(
            filepath, pagesize=A4,
            topMargin=2 * cm, bottomMargin=2 * cm, leftMargin=1.8 * cm, rightMargin=1.8 * cm
        )

    def generate_meetings_report(self, filepath, meetings):
        """Laporan seluruh rapat."""
        doc = self._base_doc(filepath)
        elements = [
            Paragraph("Laporan Rapat", self.title_style),
            Paragraph(f"Dihasilkan pada: {datetime.now().strftime('%d %B %Y %H:%M')}", self.subtitle_style),
            Spacer(1, 0.6 * cm),
        ]

        data = [["No", "Judul Rapat", "Tanggal", "Waktu", "Lokasi", "Ketua Rapat"]]
        for i, m in enumerate(meetings, start=1):
            data.append([str(i), m.title, m.date, m.time, m.location or "-", m.chairperson or "-"])

        table = Table(data, colWidths=[1.2 * cm, 5.5 * cm, 2.5 * cm, 2 * cm, 3.5 * cm, 3.5 * cm], repeatRows=1)
        table.setStyle(self._table_style())
        elements.append(table)
        elements.append(Spacer(1, 0.5 * cm))
        elements.append(Paragraph(f"Total Rapat: {len(meetings)}", self.styles["Normal"]))

        doc.build(elements)
        return filepath

    def generate_tasks_report(self, filepath, tasks, completion_percentage=None):
        """Laporan seluruh tugas & persentase penyelesaian."""
        doc = self._base_doc(filepath)
        elements = [
            Paragraph("Laporan Tugas (Action Items)", self.title_style),
            Paragraph(f"Dihasilkan pada: {datetime.now().strftime('%d %B %Y %H:%M')}", self.subtitle_style),
            Spacer(1, 0.6 * cm),
        ]

        data = [["No", "Nama Tugas", "Penanggung Jawab", "Prioritas", "Deadline", "Status"]]
        for i, t in enumerate(tasks, start=1):
            data.append([str(i), t.task_name, t.assignee or "-", t.priority, t.deadline or "-", t.status])

        table = Table(data, colWidths=[1.2 * cm, 5 * cm, 3.5 * cm, 2.3 * cm, 2.5 * cm, 3 * cm], repeatRows=1)
        table.setStyle(self._table_style())
        elements.append(table)
        elements.append(Spacer(1, 0.5 * cm))
        elements.append(Paragraph(f"Total Tugas: {len(tasks)}", self.styles["Normal"]))
        if completion_percentage is not None:
            elements.append(Paragraph(f"Persentase Penyelesaian: {completion_percentage}%", self.styles["Normal"]))

        doc.build(elements)
        return filepath

    def generate_monthly_stats_report(self, filepath, monthly_stats):
        """Laporan statistik jumlah rapat per bulan."""
        doc = self._base_doc(filepath)
        elements = [
            Paragraph("Statistik Rapat per Bulan", self.title_style),
            Paragraph(f"Dihasilkan pada: {datetime.now().strftime('%d %B %Y %H:%M')}", self.subtitle_style),
            Spacer(1, 0.6 * cm),
        ]
        data = [["Bulan", "Jumlah Rapat"]]
        for ym, total in monthly_stats:
            data.append([ym, str(total)])

        table = Table(data, colWidths=[5 * cm, 5 * cm])
        table.setStyle(self._table_style())
        elements.append(table)

        doc.build(elements)
        return filepath

    @staticmethod
    def _table_style():
        return TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A5F")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E5EA")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F6F8FB")]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
