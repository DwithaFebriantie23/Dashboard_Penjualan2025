        c_row1_c1.metric("Jumlah Baris Data", angka(len(df)))
        c_row1_c2.metric("Total Transaksi Unik", angka(df["ID TRANSAKSI"].nunique()))
        c_row1_c3.metric("Total Jenis Produk", angka(df["ITEM_NORMAL"].nunique()))

        st.divider()

        st.subheader("Informasi Kolom Dataset")
        kolom_asli = ["TANGGAL", "CUSTOMER", "ID TRANSAKSI", "ITEM", "QTY", "HARGA", "TOTAL"]
        informasi = pd.DataFrame({
            "Nama Kolom": kolom_asli,
            "Jumlah Data Terisi": [df[kolom].notna().sum() for kolom in kolom_asli],
            "Tipe Data": [str(df[kolom].dtype) for kolom in kolom_asli]
        })
        st.dataframe(informasi, use_container_width=True, hide_index=True)

        st.divider()

        st.subheader("Tabel Seluruh Data Transaksi")
        st.dataframe(
            df[["TANGGAL", "CUSTOMER", "ID TRANSAKSI", "ITEM", "QTY", "HARGA", "TOTAL"]],
            use_container_width=True,
            hide_index=True
        )

        csv = df[["TANGGAL", "CUSTOMER", "ID TRANSAKSI", "ITEM", "QTY", "HARGA", "TOTAL"]].to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 Unduh Seluruh Data Penjualan (CSV)",
            data=csv,
            file_name="data_penjualan_lengkap.csv",
            mime="text/csv"
        )


# =========================================================
# 9. MENU 3: HASIL APRIORI (DENGAN TAB)
# =========================================================

elif menu == "🔍 Hasil Apriori":

    st.title("🔍 Hasil Penelitian Apriori")

    tab_hasil, tab_kandidat, tab_pengujian = st.tabs([
        "📊 Parameter & Pola", 
        "📦 Kandidat Paket", 
        "⚙️ Evaluasi Pengujian"
    ])

    # ================= TAB 1: PARAMETER & POLA =================
    with tab_hasil:
        st.subheader("Parameter Terpilih & Pembentukan Pola")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Min Support", "0,010")
        col2.metric("Min Confidence", "0,20")
        col3.metric("Frequent Itemsets", "45")
        col4.metric("Aturan Asosiasi", "20")

        st.divider()

        st.subheader("Daftar Frequent Itemsets")
        st.write("Kombinasi produk yang memenuhi nilai minimum support (0,010):")
        st.dataframe(DATA_FREQUENT, use_container_width=True, hide_index=True)

        st.divider()

        st.subheader("Tabel Aturan Asosiasi (Association Rules)")
        st.write("Menampilkan informasi anteseden, konsekuen, support, confidence, dan lift ratio:")
        st.dataframe(DATA_RULES, use_container_width=True, hide_index=True)

        st.divider()

        st.subheader("Rata-rata Nilai Aturan Asosiasi")
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Support", "0,012129")
        col2.metric("Average Confidence", "85,54%")
        col3.metric("Average Lift", "64,262390")

        st.divider()

        st.subheader("Interpretasi Hasil")
        st.write(
            """
            Berdasarkan konfigurasi parameter terpilih, algoritma Apriori menghasilkan 
            45 frequent itemsets dan 20 aturan asosiasi. Nilai lift seluruh aturan lebih dari 1, 
            menunjukkan adanya asosiasi positif yang kuat antar produk.
            """
        )

    # ================= TAB 2: KANDIDAT PAKET =================
    with tab_kandidat:
        st.subheader("5 Kombinasi Kandidat Paket Penjualan")
        st.dataframe(DATA_KANDIDAT, use_container_width=True, hide_index=True)

        st.divider()

        st.subheader("Visualisasi Jumlah Transaksi per Kandidat")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.barh(
            DATA_KANDIDAT["Kandidat Paket"].iloc[::-1],
            DATA_KANDIDAT["Jumlah Transaksi"].iloc[::-1],
            color="#2ca02c"
        )
        ax.set_xlabel("Jumlah Transaksi")
        ax.set_ylabel("Kandidat Paket")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # ================= TAB 3: EVALUASI PENGUJIAN =================
    with tab_pengujian:
        st.subheader("Perbandingan Pengujian Parameter")
        st.dataframe(DATA_PENGUJIAN, use_container_width=True, hide_index=True)

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.write("**Frequent Itemsets**")
            fig, ax = plt.subplots(figsize=(5, 3.5))
            ax.bar(DATA_PENGUJIAN["Pengujian"], DATA_PENGUJIAN["Frequent Itemsets"], color="orange")
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        with col2:
            st.write("**Aturan Asosiasi**")
            fig, ax = plt.subplots(figsize=(5, 3.5))
