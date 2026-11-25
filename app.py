import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analisis Stok Gudang UPS", page_icon="📦", layout="wide")
st.title("📦 Sistem Analisis Stok Barang Gudang")
st.caption("Demo analisis persediaan barang UPS dan sparepart menggunakan dataset contoh.")

@st.cache_data
def load_default_data():
    return pd.read_csv("dataset_stok_gudang.csv")

uploaded = st.sidebar.file_uploader("Upload dataset CSV (opsional)", type=["csv"])
try:
    data = pd.read_csv(uploaded) if uploaded else load_default_data()
except Exception as e:
    st.error(f"Dataset tidak dapat dibaca: {e}")
    st.stop()

required = {"kode_barang","nama_barang","kategori","stok_awal","barang_masuk","barang_keluar","stok_minimum"}
missing = required - set(data.columns)
if missing:
    st.error("Kolom dataset belum lengkap: " + ", ".join(sorted(missing)))
    st.stop()

# Convert numeric fields and calculate stock to avoid relying on prefilled values.
for col in ["stok_awal", "barang_masuk", "barang_keluar", "stok_minimum"]:
    data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)
data["stok_akhir"] = data["stok_awal"] + data["barang_masuk"] - data["barang_keluar"]
data["status_stok"] = data.apply(
    lambda r: "Habis" if r["stok_akhir"] <= 0 else
    ("Menipis" if r["stok_akhir"] <= r["stok_minimum"] else "Aman"), axis=1
)

st.sidebar.header("Filter")
categories = ["Semua"] + sorted(data["kategori"].dropna().astype(str).unique().tolist())
selected_category = st.sidebar.selectbox("Kategori barang", categories)
status_options = ["Semua", "Aman", "Menipis", "Habis"]
selected_status = st.sidebar.selectbox("Status stok", status_options)

filtered = data.copy()
if selected_category != "Semua":
    filtered = filtered[filtered["kategori"] == selected_category]
if selected_status != "Semua":
    filtered = filtered[filtered["status_stok"] == selected_status]

total_items = len(filtered)
total_stock = int(filtered["stok_akhir"].clip(lower=0).sum())
low_stock = int((filtered["status_stok"] == "Menipis").sum())
out_stock = int((filtered["status_stok"] == "Habis").sum())

c1, c2, c3, c4 = st.columns(4)
c1.metric("Jenis barang", f"{total_items}")
c2.metric("Total stok akhir", f"{total_stock:,}")
c3.metric("Stok menipis", f"{low_stock}")
c4.metric("Stok habis", f"{out_stock}")

st.subheader("Ringkasan stok")
left, right = st.columns(2)
with left:
    status_counts = filtered["status_stok"].value_counts().reindex(["Aman","Menipis","Habis"], fill_value=0)
    st.bar_chart(status_counts)
with right:
    category_stock = filtered.groupby("kategori")["stok_akhir"].sum().sort_values(ascending=False)
    st.bar_chart(category_stock)

st.subheader("Tabel analisis persediaan")
st.dataframe(filtered, use_container_width=True, hide_index=True)

if not filtered.empty:
    st.subheader("Perlu perhatian")
    attention = filtered[filtered["status_stok"].isin(["Menipis", "Habis"])]
    if attention.empty:
        st.success("Tidak ada barang yang berstatus menipis atau habis pada filter ini.")
    else:
        st.warning(f"Ada {len(attention)} jenis barang yang perlu diperiksa.")
        st.dataframe(attention[["kode_barang","nama_barang","stok_akhir","stok_minimum","status_stok"]], use_container_width=True, hide_index=True)

st.download_button(
    "⬇️ Unduh hasil analisis CSV",
    data=filtered.to_csv(index=False).encode("utf-8-sig"),
    file_name="hasil_analisis_stok.csv",
    mime="text/csv"
)

with st.expander("Metode perhitungan"):
    st.write("Stok akhir = stok awal + barang masuk − barang keluar.")
    st.write("Status Habis: stok akhir ≤ 0. Status Menipis: stok akhir > 0 dan ≤ stok minimum. Selain itu berstatus Aman.")
    st.write("Dataset ini merupakan data simulasi untuk tugas, bukan data persediaan aktual perusahaan.")
