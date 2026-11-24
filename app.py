import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# =========================================================
# 1. KONFIGURASI DASHBOARD
# =========================================================

st.set_page_config(
    page_title="Dashboard Penjualan PT CKL",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
FILE_EXCEL = BASE_DIR / "Penjualan2025.xlsx"


# =========================================================
# 2. MEMBACA DAN MEMBERSIHKAN DATA EXCEL
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_excel(
        FILE_EXCEL,
        sheet_name="Rekap 2025",
        header=1
    )

    # Mengikuti preprocessing pada Google Colab:
    # mengeluarkan seluruh baris dengan TOTAL = 0 terlebih dahulu.
    # Salah satu baris tersebut memiliki ID TRANSAKSI kosong.
    df["TOTAL"] = pd.to_numeric(df["TOTAL"], errors="coerce")
    df = df[df["TOTAL"] != 0].copy()

    # Memastikan atribut utama tersedia setelah preprocessing
    df = df.dropna(
        subset=["ID TRANSAKSI", "ITEM"]
    ).copy()

    # Normalisasi ID transaksi
    def normalisasi_id(value):
        if isinstance(value, pd.Timestamp):
            return value.strftime("%Y-%m-%d")
        return str(value).strip()

    df["ID TRANSAKSI"] = (
        df["ID TRANSAKSI"].apply(normalisasi_id)
    )

    # Mempertahankan nama item asli untuk ditampilkan pada dashboard
    df["ITEM"] = (
        df["ITEM"].astype(str).str.strip()
    )

    # Membersihkan nama pelanggan
    df["CUSTOMER"] = (
        df["CUSTOMER"]
        .fillna("Tidak Diketahui")
        .astype(str)
        .str.strip()
    )

    # Mengubah tanggal
    df["TANGGAL"] = pd.to_datetime(
        df["TANGGAL"],
        errors="coerce"
    )

    # Mengubah kolom numerik
    for kolom in ["QTY", "HARGA", "TOTAL"]:
        df[kolom] = pd.to_numeric(
            df[kolom],
            errors="coerce"
        )

    # Membuat kolom bulan
    df["BULAN"] = (
        df["TANGGAL"].dt.to_period("M")
    )

    # Pemeriksaan jumlah data agar konsisten dengan hasil preprocessing Colab
    if len(df) != 1883:
        st.warning(
            f"Jumlah baris setelah preprocessing adalah {len(df):,}, "
            "sedangkan hasil Google Colab adalah 1.883 baris. "
            "Periksa kembali file Excel yang digunakan."
        )

    return df

