"""
report_controller.py
Menjembatani View dengan generator laporan PDF & Excel.
"""

import os
import sys
from datetime import datetime

from models.meeting_model import Meeting
from models.action_item_model import ActionItem
from reports.pdf_report import PDFReportGenerator
from reports.excel_report import ExcelReportGenerator


class ReportController:

    def __init__(self):
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.export_dir = os.path.join(base_dir, "exports")
        os.makedirs(self.export_dir, exist_ok=True)
        self.pdf_gen = PDFReportGenerator()
        self.excel_gen = ExcelReportGenerator()

    def _timestamp(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def export_meetings_pdf(self):
        meetings = Meeting.get_all()
        filepath = os.path.join(self.export_dir, f"laporan_rapat_{self._timestamp()}.pdf")
        return self.pdf_gen.generate_meetings_report(filepath, meetings)

    def export_meetings_excel(self):
        meetings = Meeting.get_all()
        filepath = os.path.join(self.export_dir, f"laporan_rapat_{self._timestamp()}.xlsx")
        return self.excel_gen.generate_meetings_report(filepath, meetings)

    def export_tasks_pdf(self):
        tasks = ActionItem.get_all()
        completion = ActionItem.completion_percentage()
        filepath = os.path.join(self.export_dir, f"laporan_tugas_{self._timestamp()}.pdf")
        return self.pdf_gen.generate_tasks_report(filepath, tasks, completion)

    def export_tasks_excel(self):
        tasks = ActionItem.get_all()
        filepath = os.path.join(self.export_dir, f"laporan_tugas_{self._timestamp()}.xlsx")
        return self.excel_gen.generate_tasks_report(filepath, tasks)

    def export_monthly_stats_pdf(self):
        stats = Meeting.count_per_month()
        filepath = os.path.join(self.export_dir, f"statistik_bulanan_{self._timestamp()}.pdf")
        return self.pdf_gen.generate_monthly_stats_report(filepath, stats)

    def export_full_excel(self):
        meetings = Meeting.get_all()
        tasks = ActionItem.get_all()
        stats = Meeting.count_per_month()
        completion = ActionItem.completion_percentage()
        filepath = os.path.join(self.export_dir, f"laporan_lengkap_{self._timestamp()}.xlsx")
        return self.excel_gen.generate_full_report(filepath, meetings, tasks, stats, completion)

    def get_report_summary(self):
        return {
            "total_meetings": Meeting.count_all(),
            "total_tasks": len(ActionItem.get_all()),
            "completion_percentage": ActionItem.completion_percentage(),
            "monthly_stats": Meeting.count_per_month(),
        }
