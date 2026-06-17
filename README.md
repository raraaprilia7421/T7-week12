# Dashboard Penjualan Supermarket - Aplikasi CRUD & Visualisasi Data

Tugas Mandiri Pekan 12 (T7-week12) - Integrasi PySide6, SQLite, Pandas, dan Matplotlib.

## 👤 Identitas Mahasiswa
\* \*\*Nama:\*\* \[Rara Apriliana]

\* \*\*NIM:\*\* \[F1D020086]

\* \*\*Kelas:\*\* \[Pemerograman Visual C]

---

## 🚀 Deskripsi Project
Aplikasi ini adalah dashboard manajemen dan visualisasi data penjualan supermarket berbasis desktop menggunakan **PySide6**. Data disimpan secara lokal menggunakan database **SQLite** dan diolah menggunakan library **Pandas** untuk menghasilkan grafik tren penjualan interaktif melalui **Matplotlib**.

### ✨ Fitur Utama (Nilai Plus)
1. **Sistem CRUD Otomatis**: Fitur menambah (Create), membaca (Read), mengubah (Update), dan menghapus (Delete) data penjualan langsung dari UI.
2. **Input Kalender Interaktif (`QDateEdit`)**: Memudahkan user memilih tanggal tanpa risiko error format penulisan (`YYYY-MM-DD`).
3. **Smart Add Mode**: Ketika tombol "Tambah Data" diklik, form otomatis kosong, tombol CRUD lain disembunyikan, dan muncul tombol "Oke" untuk konfirmasi simpan data baru.
4. **Filter Kategori Dinamis**: Grafik dan tabel akan otomatis terupdate secara *real-time* saat kategori drop-down diubah.
5. **Ekspor Grafik**: Fitur menyimpan grafik visualisasi ke dalam file gambar `.png`.

---

## 📁 Struktur Project
```text
dashboard_supermarket/
│
├── main.py                # File utama aplikasi (UI dan Logika CRUD)
├── database.py            # Konfigurasi SQLite & query database
├── chart_widget.py        # Komponen grafik Matplotlib & Pandas
├── supermarket_sales.db   # Database SQLite tempat penyimpanan data
└── Readme.md              # Dokumentasi project (File ini)
