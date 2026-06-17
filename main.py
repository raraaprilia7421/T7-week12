import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, 
                             QLabel, QComboBox, QLineEdit, QDateEdit, QFormLayout, QMessageBox, QHeaderView)
from PySide6.QtCore import Qt, QDate
import database
from chart_widget import DashboardChartWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Penjualan - Aplikasi CRUD & Visualisasi")
        self.resize(1100, 750)
        
        # Jalankan inisialisasi database SQLite
        database.init_db()
        
        # Kontainer Utama
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # ----------------- PANEL ATAS: FILTER & TOMBOL -----------------
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Filter Kategori:"))
        
        self.combo_filter = QComboBox()
        self.combo_filter.addItems(["Semua", "Elektronik", "Fashion", "Makanan", "Kesehatan", "Otomotif"])
        self.combo_filter.currentTextChanged.connect(self.load_data_to_ui)
        top_layout.addWidget(self.combo_filter)
        
        top_layout.addStretch()  # Dorong tombol ke sebelah kanan
        
        self.btn_refresh = QPushButton("🔄 Refresh")
        self.btn_refresh.clicked.connect(self.load_data_to_ui)
        top_layout.addWidget(self.btn_refresh)
        
        self.btn_export = QPushButton("📸 Export Chart ke PNG")
        self.btn_export.clicked.connect(self.export_chart_action)
        top_layout.addWidget(self.btn_export)
        
        main_layout.addLayout(top_layout)
        
        # ----------------- PANEL TENGAH: GRAFIK -----------------
        self.chart_widget = DashboardChartWidget()
        main_layout.addWidget(self.chart_widget, stretch=3) # Mengambil porsi layar lebih besar
        
        # ----------------- PANEL BAWAH: TABEL & FORM INPUT -----------------
        bottom_layout = QHBoxLayout()
        
        # Tabel Data Mentah
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Tanggal", "Kategori", "Produk", "Qty", "Harga", "Total"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Memicu pemindahan data ke form saat kotak mana saja di tabel diklik
        self.table_widget.cellClicked.connect(self.fill_form_from_clicked_cell)
        bottom_layout.addWidget(self.table_widget, stretch=3)
        
        # Form Input CRUD
        form_container = QWidget()
        form_layout = QFormLayout(form_container)
        
        self.txt_id = QLineEdit()
        self.txt_id.setDisabled(True) # ID tidak boleh diedit manual karena auto-increment
        
        # Menggunakan komponen QDateEdit berupa Kalender Pop-up Otomatis
        self.txt_tanggal = QDateEdit()
        self.txt_tanggal.setCalendarPopup(True)
        self.txt_tanggal.setDate(QDate.currentDate()) # Default tanggal hari ini
        
        self.combo_kategori = QComboBox()
        self.combo_kategori.addItems(["Elektronik", "Fashion", "Makanan", "Kesehatan", "Otomotif"])
        
        self.txt_produk = QLineEdit()
        self.txt_jumlah = QLineEdit()
        self.txt_harga = QLineEdit()
        
        form_layout.addRow("ID (Otomatis):", self.txt_id)
        form_layout.addRow("Tanggal:", self.txt_tanggal)
        form_layout.addRow("Kategori:", self.combo_kategori)
        form_layout.addRow("Nama Produk:", self.txt_produk)
        form_layout.addRow("Jumlah (Qty):", self.txt_jumlah)
        form_layout.addRow("Harga Satuan:", self.txt_harga)
        
        # Layout Tombol Aksi CRUD
        crud_buttons = QHBoxLayout()
        self.btn_create = QPushButton("Tambah Data")
        self.btn_update = QPushButton("Ubah")
        self.btn_delete = QPushButton("Hapus")
        self.btn_oke = QPushButton("Oke") # Tombol Oke Baru
        
        # Sembunyikan tombol Oke di awal aplikasi berjalan
        self.btn_oke.setVisible(False)
        
        self.btn_create.clicked.connect(self.prepare_for_add) # Pemicu kosongkan form & ganti tombol
        self.btn_update.clicked.connect(self.action_update)
        self.btn_delete.clicked.connect(self.action_delete)
        self.btn_oke.clicked.connect(self.action_save_new_data) # Pemicu eksekusi simpan data baru
        
        crud_buttons.addWidget(self.btn_create)
        crud_buttons.addWidget(self.btn_update)
        crud_buttons.addWidget(self.btn_delete)
        crud_buttons.addWidget(self.btn_oke)
        form_layout.addRow(crud_buttons)
        
        bottom_layout.addWidget(form_container, stretch=2)
        main_layout.addLayout(bottom_layout, stretch=2)
        
        # Muat data pertama kali
        self.load_data_to_ui()

    # ----------------- LOGIKA SISTEM & KONTROL -----------------
    def load_data_to_ui(self):
        """Mengambil data dari SQLite, memfilter, lalu mengupdate Tabel dan Grafik."""
        all_data = database.fetch_all_data()
        current_filter = self.combo_filter.currentText()
        
        # Filter data untuk tabel
        if current_filter == "Semua":
            display_data = all_data
        else:
            display_data = [row for row in all_data if row[2] == current_filter]
            
        # Update Tabel
        self.table_widget.setRowCount(0)
        for row_idx, row_data in enumerate(display_data):
            self.table_widget.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                if col_idx in [4, 5, 6]: # Angka rata kanan
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table_widget.setItem(row_idx, col_idx, item)
                
        # Update Grafik
        self.chart_widget.update_charts(all_data, current_filter)
        self.reset_ui_state()

    def fill_form_from_clicked_cell(self, row, column):
        """Mengambil semua data dari baris yang diklik dan memasukkannya ke form."""
        try:
            # Kembalikan mode tombol ke CRUD standar jika pengguna klik tabel kembali
            self.reset_ui_state()
            
            self.txt_id.setText(self.table_widget.item(row, 0).text())
            
            # Mengubah format string tanggal (YYYY-MM-DD) dari tabel menjadi objek kalender UI
            tanggal_str = self.table_widget.item(row, 1).text()
            self.txt_tanggal.setDate(QDate.fromString(tanggal_str, "yyyy-MM-dd"))
            
            self.combo_kategori.setCurrentText(self.table_widget.item(row, 2).text())
            self.txt_produk.setText(self.table_widget.item(row, 3).text())
            self.txt_jumlah.setText(self.table_widget.item(row, 4).text())
            self.txt_harga.setText(self.table_widget.item(row, 5).text())
        except Exception as e:
            pass

    def prepare_for_add(self):
        """1. MENGOSONGKAN FORM & MENAMPILKAN TOMBOL OKE"""
        self.txt_id.clear()
        self.txt_tanggal.setDate(QDate.currentDate()) # Reset ke hari ini
        self.txt_produk.clear()
        self.txt_jumlah.clear()
        self.txt_harga.clear()
        self.table_widget.clearSelection() # Hilangkan seleksi biru di tabel
        
        # Tukar Tampilan Tombol
        self.btn_create.setVisible(False)
        self.btn_update.setVisible(False)
        self.btn_delete.setVisible(False)
        self.btn_oke.setVisible(True) # Tampilkan tombol Oke
        
        # Arahkan kursor langsung ke input Nama Produk agar siap diketik
        self.txt_produk.setFocus()

    def reset_ui_state(self):
        """Mengembalikan form dan susunan tombol ke kondisi normal."""
        self.txt_id.clear()
        self.txt_tanggal.setDate(QDate.currentDate())
        self.txt_produk.clear()
        self.txt_jumlah.clear()
        self.txt_harga.clear()
        
        # Kembalikan tombol ke default
        self.btn_create.setVisible(True)
        self.btn_update.setVisible(True)
        self.btn_delete.setVisible(True)
        self.btn_oke.setVisible(False) # Sembunyikan tombol Oke

    # ----------------- LOGIKA EKSKUSI TOMBOL (CRUD) -----------------
    def action_save_new_data(self):
        """2. KETIKA TOMBOL OKE DIKLIK -> SIMPAN DATA BARU"""
        # Validasi kolom kosong
        if not self.txt_produk.text() or not self.txt_jumlah.text() or not self.txt_harga.text():
            QMessageBox.warning(self, "Peringatan", "Semua kolom input wajib diisi terlebih dahulu sebelum menekan Oke!")
            return
        try:
            tgl_fix = self.txt_tanggal.date().toString("yyyy-MM-dd")
            database.insert_data(
                tgl_fix, self.combo_kategori.currentText(),
                self.txt_produk.text(), int(self.txt_jumlah.text()), float(self.txt_harga.text())
            )
            # Muat ulang tabel & otomatis mengembalikan mode tombol ke default lewat reset_ui_state()
            self.load_data_to_ui()
            QMessageBox.information(self, "Berhasil", "Data baru berhasil disimpan!")
        except Exception as e:
            QMessageBox.warning(self, "Gagal", f"Format input angka salah!\nError: {e}")

    def action_update(self):
        if not self.txt_id.text():
            QMessageBox.warning(self, "Peringatan", "Silakan klik/pilih salah satu data di dalam tabel terlebih dahulu!")
            return
        if not self.txt_produk.text() or not self.txt_jumlah.text() or not self.txt_harga.text():
            QMessageBox.warning(self, "Peringatan", "Kolom input tidak boleh dikosongkan saat mengedit!")
            return
        try:
            tgl_fix = self.txt_tanggal.date().toString("yyyy-MM-dd")
            database.update_data(
                int(self.txt_id.text()), tgl_fix, self.combo_kategori.currentText(),
                self.txt_produk.text(), int(self.txt_jumlah.text()), float(self.txt_harga.text())
            )
            self.load_data_to_ui()
            QMessageBox.information(self, "Berhasil", "Data berhasil diperbarui!")
        except Exception as e:
            QMessageBox.warning(self, "Gagal", f"Gagal memperbarui data. Periksa format input Anda.\nError: {e}")

    def action_delete(self):
        if not self.txt_id.text():
            QMessageBox.warning(self, "Peringatan", "Silakan klik/pilih salah satu data di dalam tabel yang ingin dihapus!")
            return
        ask = QMessageBox.question(self, "Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?", QMessageBox.Yes | QMessageBox.No)
        if ask == QMessageBox.Yes:
            database.delete_data(int(self.txt_id.text()))
            self.load_data_to_ui()

    def export_chart_action(self):
        try:
            self.chart_widget.export_to_png("dashboard_output.png")
            QMessageBox.information(self, "Sukses Ekspor", "Grafik berhasil diekspor menjadi file 'dashboard_output.png'!")
        except Exception as e:
            QMessageBox.critical(self, "Gagal", f"Terjadi kesalahan saat mengekspor: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())