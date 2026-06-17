import sqlite3
import os
import random
from datetime import datetime, timedelta

DB_NAME = "supermarket_sales.db"

def init_db():
    """Membuat database dan tabel penjualan jika belum ada, lalu mengisinya dengan 55 data acak."""
    db_exists = os.path.exists(DB_NAME)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    if not db_exists:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TEXT,
                kategori TEXT,
                produk TEXT,
                jumlah INTEGER,
                harga REAL,
                total REAL
            )
        ''')
        
        # Data tiruan agar realistis
        kategori_list = ['Elektronik', 'Fashion', 'Makanan', 'Kesehatan', 'Otomotif']
        produk_dict = {
            'Elektronik': ['Smartphone', 'Laptop', 'Earphone'],
            'Fashion': ['Kemeja', 'Celana Jeans', 'Jaket'],
            'Makanan': ['Camilan', 'Susu', 'Roti'],
            'Kesehatan': ['Vitamin', 'Masker', 'Obat'],
            'Otomotif': ['Oli Motor', 'Helm', 'Kunci Pas']
        }
        
        # Generate 55 data transaksi (Kriteria tugas min 50 baris)
        start_date = datetime.now() - timedelta(days=30)
        for _ in range(55):  
            kat = random.choice(kategori_list)
            prod = random.choice(produk_dict[kat])
            qty = random.randint(1, 5)
            harga = random.choice([50000, 100000, 150000, 250000, 500000])
            total = qty * harga
            tgl = (start_date + timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
            
            cursor.execute('''
                INSERT INTO sales (tanggal, kategori, produk, jumlah, harga, total)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (tgl, kat, prod, qty, harga, total))
            
        conn.commit()
    conn.close()

def fetch_all_data():
    """Mengambil semua data dari database (Read)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return data

def insert_data(tanggal, kategori, produk, jumlah, harga):
    """Menambahkan data baru (Create)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    total = int(jumlah) * float(harga)
    cursor.execute('''
        INSERT INTO sales (tanggal, kategori, produk, jumlah, harga, total)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (tanggal, kategori, produk, jumlah, harga, total))
    conn.commit()
    conn.close()

def update_data(id_data, tanggal, kategori, produk, jumlah, harga):
    """Mengubah data yang sudah ada (Update)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    total = int(jumlah) * float(harga)
    cursor.execute('''
        UPDATE sales SET tanggal=?, kategori=?, produk=?, jumlah=?, harga=?, total=?
        WHERE id=?
    ''', (tanggal, kategori, produk, jumlah, harga, total, id_data))
    conn.commit()
    conn.close()

def delete_data(id_data):
    """Menghapus data (Delete)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sales WHERE id=?", (id_data,))
    conn.commit()
    conn.close()