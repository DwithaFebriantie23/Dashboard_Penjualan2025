from pathlib import Path

source_path = Path("/mnt/data/Teks yang ditempel (1)(20261124-022557).txt")
source = source_path.read_text(encoding="utf-8")

# Preserve the user's original app.py and add a normalized key solely for
# counting distinct product codes. The original ITEM column remains unchanged.
old_item_block = '''    # Mempertahankan nama item asli
    df["ITEM"] = (
        df["ITEM"].astype(str).str.strip()
    )
'''
new_item_block = '''    # Mempertahankan nama item asli untuk ditampilkan pada dashboard
    df["ITEM"] = (
        df["ITEM"].astype(str).str.strip()
    )

    # Kunci normalisasi untuk menghitung jenis produk unik.
    # Normalisasi ini menyamakan huruf besar-kecil dan menghapus spasi,
    # tanpa mengubah nilai ITEM asli yang digunakan pada tampilan.
    df["ITEM_NORMAL"] = (
        df["ITEM"]
        .str.upper()
        .str.replace(r"\\\\s+", "", regex=True)
    )
'''
if old_item_block not in source:
    raise ValueError("Blok pembersihan ITEM tidak ditemukan; file tidak diubah.")
source = source.replace(old_item_block, new_item_block, 1)

old_home_count = '    total_produk = df["ITEM"].nunique()'
new_home_count = '    total_produk = df["ITEM_NORMAL"].nunique()'
if old_home_count not in source:
    raise ValueError("Perhitungan total_produk pada Beranda tidak ditemukan.")
source = source.replace(old_home_count, new_home_count, 1)

old_dataset_count = '        c_row1_c3.metric("Total Jenis Produk", angka(df["ITEM"].nunique()))'
new_dataset_count = '        c_row1_c3.metric("Total Jenis Produk", angka(df["ITEM_NORMAL"].nunique()))'
if old_dataset_count not in source:
    raise ValueError("Perhitungan Total Jenis Produk pada Karakteristik Dataset tidak ditemukan.")
source = source.replace(old_dataset_count, new_dataset_count, 1)

# Save a runnable Python file.
output_path = Path("/mnt/data/app.py")
output_path.write_text(source, encoding="utf-8")

print(f"File berhasil dibuat: {output_path}")
print(f"Ukuran file: {output_path.stat().st_size:,} byte")
print("Perubahan: menambahkan ITEM_NORMAL dan menggunakannya untuk dua metrik jumlah jenis produk.")
