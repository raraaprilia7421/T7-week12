import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import QWidget, QVBoxLayout
import pandas as pd

class DashboardChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Membuat 1 bidang (figure) berisi 2 sub-plot (kiri dan kanan)
        self.figure, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 4))
        self.canvas = FigureCanvas(self.figure)
        
        # Tempel canvas Matplotlib ke dalam layout PySide6
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
    def update_charts(self, raw_data, filter_kategori="Semua"):
        """Membersihkan grafik lama dan menggambar grafik baru berdasarkan data terbaru."""
        self.ax1.clear()
        self.ax2.clear()
        
        if not raw_data:
            self.canvas.draw()
            return

        # Ubah data tuple SQLite menjadi Pandas DataFrame agar mudah dikelompokkan
        df = pd.DataFrame(raw_data, columns=['ID', 'Tanggal', 'Kategori', 'Produk', 'Jumlah', 'Harga', 'Total'])
        
        # Logika filter kategori
        if filter_kategori != "Semua":
            df = df[df['Kategori'] == filter_kategori]
            
        if df.empty:
            self.canvas.draw()
            return

        # --- CHART 1: Bar Chart (Grafik Batang) ---
        if filter_kategori == "Semua":
            summary_cat = df.groupby('Kategori')['Total'].sum()
            summary_cat.plot(kind='bar', ax=self.ax1, color='#3498db')
            self.ax1.set_title("Total Pendapatan per Kategori")
            self.ax1.set_xticklabels(summary_cat.index, rotation=30, ha='right')
        else:
            summary_prod = df.groupby('Produk')['Jumlah'].sum()
            summary_prod.plot(kind='bar', ax=self.ax1, color='#2ecc71')
            self.ax1.set_title(f"Jumlah Terjual di Kategori {filter_kategori}")
            self.ax1.set_xticklabels(summary_prod.index, rotation=30, ha='right')
        self.ax1.set_ylabel("Nilai")

        # --- CHART 2: Line Chart (Grafik Garis Tren) ---
        df['Tanggal'] = pd.to_datetime(df['Tanggal'])
        trend = df.groupby('Tanggal')['Total'].sum().sort_index()
        trend.plot(kind='line', ax=self.ax2, marker='o', color='#e74c3c', linewidth=2)
        self.ax2.set_title("Tren Penjualan Harian")
        self.ax2.set_ylabel("Total Penjualan (Rp)")
        self.ax2.tick_params(axis='x', rotation=30)

        # Atur layout otomatis agar tidak bertabrakan/terpotong saat window di-resize
        self.figure.tight_layout()
        self.canvas.draw()

    def export_to_png(self, filename="dashboard_chart.png"):
        """Menyimpan grafik aktif menjadi file gambar PNG."""
        self.figure.savefig(filename, dpi=300)