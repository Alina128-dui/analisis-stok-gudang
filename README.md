# Sistem Analisis Stok Barang Gudang

Aplikasi demo untuk menganalisis persediaan barang UPS dan sparepart menggunakan Python, Pandas, dan Streamlit.

## Fitur
- Membaca dataset CSV contoh atau CSV unggahan pengguna
- Menghitung stok akhir
- Mengelompokkan status stok: Aman, Menipis, Habis
- Filter kategori dan status
- Ringkasan dan grafik stok
- Mengunduh hasil analisis

## Rumus
Stok akhir = stok awal + barang masuk - barang keluar

Aturan status:
- Habis: stok akhir <= 0
- Menipis: stok akhir > 0 dan <= stok minimum
- Aman: stok akhir > stok minimum

## Menjalankan di komputer
1. Install Python.
2. Buka terminal di folder proyek.
3. Jalankan `pip install -r requirements.txt`.
4. Jalankan `streamlit run app.py`.
5. Buka alamat lokal yang ditampilkan Streamlit.

## Struktur file
- `app.py`: program utama
- `dataset_stok_gudang.csv`: dataset simulasi
- `requirements.txt`: daftar library
- `README.md`: petunjuk proyek

## Catatan dataset
Seluruh data pada dataset bawaan adalah data simulasi untuk pembelajaran. Jangan menganggapnya sebagai data stok aktual PT atau perusahaan mana pun.
