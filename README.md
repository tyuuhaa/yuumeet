# YuuMeet

Aplikasi desktop untuk mengelola hasil rapat, action items (tugas), dan deadline
dalam organisasi, perusahaan, maupun kepanitiaan. Dibangun menggunakan **Python + Tkinter**
dengan arsitektur **MVC (Model-View-Controller)** dan database **SQLite**.

## Fitur Utama

1. **Dashboard** — ringkasan rapat, tugas belum selesai, deadline mendatang, kalender agenda, dan statistik progres.
2. **Meeting Management** — CRUD rapat lengkap (judul, tanggal, waktu, lokasi, ketua, peserta, agenda) + riwayat.
3. **Meeting Minutes** — pencatatan hasil pembahasan, keputusan rapat, dan catatan tambahan dengan **auto-save**.
4. **Action Items (Tugas)** — CRUD tugas dengan prioritas, deadline, status (To Do/In Progress/Done), dan reminder.
5. **Calendar & Timeline** — kalender bulanan agenda rapat + timeline deadline tugas.
6. **Search & Filter** — pencarian rapat/peserta/tugas dengan berbagai filter kombinasi.
7. **Reports** — laporan rapat & tugas, statistik bulanan, **export ke PDF dan Excel**.
8. **User Settings** — Dark/Light Mode, warna tema, backup & restore database, lokasi penyimpanan data.

## Struktur Folder

```
event_meeting_manager/
├── main.py                  # Entry point aplikasi
├── requirements.txt
├── models/                  # Layer Model (akses & operasi data)
│   ├── meeting_model.py
│   ├── minutes_model.py
│   ├── action_item_model.py
│   └── settings_model.py
├── views/                   # Layer View (tampilan UI Tkinter)
│   ├── main_window.py
│   ├── dashboard_view.py
│   ├── meeting_view.py
│   ├── minutes_view.py
│   ├── task_view.py
│   ├── calendar_view.py
│   ├── search_view.py
│   ├── report_view.py
│   ├── settings_view.py
│   └── components/          # Komponen UI reusable (sidebar, topbar, cards, dialogs, dst)
├── controllers/              # Layer Controller (logika bisnis, menjembatani Model & View)
│   ├── dashboard_controller.py
│   ├── meeting_controller.py
│   ├── minutes_controller.py
│   ├── task_controller.py
│   ├── report_controller.py
│   └── settings_controller.py
├── database/
│   ├── db_manager.py         # Koneksi & inisialisasi SQLite
│   ├── schema.sql            # Skema tabel database
│   └── meeting_manager.db    # File database (dibuat otomatis saat pertama dijalankan)
├── utils/
│   ├── theme.py               # Tema warna (light/dark) & font
│   ├── validators.py          # Validasi input form
│   └── helpers.py             # Fungsi bantu (format tanggal, warna prioritas, dll)
├── reports/
│   ├── pdf_report.py          # Generator laporan PDF (ReportLab)
│   └── excel_report.py        # Generator laporan Excel (openpyxl)
├── exports/                   # Folder output hasil export laporan & backup database
│   └── backups/
└── assets/
    └── icons/
```

## Cara Menjalankan

1. Pastikan Python 3.9+ sudah terpasang.
2. Install dependency:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi:
   ```bash
   python main.py
   ```

Database SQLite (`meeting_manager.db`) beserta seluruh tabelnya akan dibuat secara otomatis
di folder `database/` pada saat aplikasi pertama kali dijalankan.

## Shortcut Keyboard

| Shortcut     | Aksi                          |
|--------------|-------------------------------|
| Ctrl+1       | Buka halaman Dashboard         |
| Ctrl+2       | Buka halaman Meeting Management |
| Ctrl+3       | Buka halaman Action Items      |
| Ctrl+4       | Buka halaman Calendar          |
| Ctrl+5       | Buka halaman Search            |
| Ctrl+6       | Buka halaman Reports           |
| Ctrl+7       | Buka halaman Settings          |
| Ctrl+F       | Fokus ke halaman Search        |
| Ctrl+S       | Simpan form (saat modal form terbuka) |
| Klik kanan   | Membuka context menu (edit/hapus/ubah status) |

## Catatan Pengembangan

- Kode mengikuti prinsip **Clean Code** dan **OOP**, dengan pemisahan tegas antara
  logika bisnis (Controller/Model) dan tampilan (View).
- Seluruh komponen UI reusable (sidebar, topbar, card, tabel, dialog, form field)
  dipisahkan di `views/components/` agar tidak ada duplikasi kode.
- Validasi input dilakukan di layer `utils/validators.py` dan dipanggil dari Controller
  sebelum data disimpan ke database.
- Auto-save notulen rapat menggunakan mekanisme debounce (delay setelah user berhenti mengetik).
