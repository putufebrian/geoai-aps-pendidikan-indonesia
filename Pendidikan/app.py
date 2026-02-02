import sys
import os
from flask import Flask, request
import pandas as pd
import geopandas as gpd
import folium
import pickle

# Konfigurasi Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

app = Flask(__name__)

# =========================
# LOAD MODEL & GEOJSON
# =========================
# Pastikan Anda sudah menjalankan buat_model_pkl.py setelah update model_kebijakan_pendidikan.py
MODEL_PATH = os.path.join(BASE_DIR, "model", "model_kebijakan_pendidikan_2025.pkl")
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Memuat data GeoJSON Provinsi
GEOJSON_PATH = os.path.join(BASE_DIR, "data", "gabungan_38_wilayah_batas_provinsi.geojson")
gdf = gpd.read_file(GEOJSON_PATH)
gdf["name"] = gdf["name"].str.upper().str.strip()

WARNA = {
    "RENDAH": "#d73027",  # Merah
    "SEDANG": "#fee08b",  # Kuning
    "TINGGI": "#1a9850"   # Hijau
}

# =========================
# FUNGSI MEMBUAT MAP
# =========================
def buat_map(data=None):
    # Titik tengah Indonesia
    peta = folium.Map(
        location=[-2.5, 118],
        zoom_start=5,
        tiles="cartodbpositron"
    )

    if data is not None:
        # Gabungkan data Excel yang sudah diprediksi dengan GeoJSON
        gabungan = gdf.merge(
            data,
            left_on="name",
            right_on="38 Provinsi",
            how="left"
        )

        folium.GeoJson(
            gabungan,
            style_function=lambda f: {
                "fillColor": WARNA.get(
                    f["properties"].get("Kategori Pendidikan"),
                    "#cccccc" # Abu-abu jika data tidak ditemukan
                ),
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.8
            },
            tooltip=folium.GeoJsonTooltip(
                fields=[
                    "name",
                    "APS_7_12",
                    "APS_13_15",
                    "APS_16_18",
                    "APS_19_23",
                    "Kategori Pendidikan"
                ],
                aliases=[
                    "Provinsi:",
                    "APS Usia 7-12:",
                    "APS Usia 13-15:",
                    "APS Usia 16-18:",
                    "APS Usia 19-23:",
                    "Status:"
                ]
            ),
            popup=folium.GeoJsonPopup(
                fields=["Keputusan Pemerintah"],
                aliases=["Rekomendasi Kebijakan:"]
            )
        ).add_to(peta)

    return peta._repr_html_()

# =========================
# ROUTE UTAMA
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    map_html = buat_map()

    if request.method == "POST":
        if 'file' not in request.files:
            return "No file uploaded"
            
        file = request.files["file"]
        
        # 1. Skip 4 baris pertama (menyesuaikan format BPS)
        df = pd.read_excel(file, skiprows=4, header=None)

        # 2. Nama kolom disesuaikan dengan data APS terbaru
        df = df.iloc[:, [0, 1, 2, 3, 4]] # Ambil 5 kolom pertama saja
        df.columns = ["38 Provinsi", "APS_7_12", "APS_13_15", "APS_16_18", "APS_19_23"]

        # 3. Bersihkan Data
        df = df.dropna(subset=["38 Provinsi"])
        df["38 Provinsi"] = df["38 Provinsi"].str.upper().str.strip()

        # 4. Konversi nilai ke angka (coerce akan mengubah simbol '-' menjadi NaN)
        kolom_aps = ["APS_7_12", "APS_13_15", "APS_16_18", "APS_19_23"]
        for col in kolom_aps:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # 5. Prediksi menggunakan Model AI (APS version)
        hasil = model.predict(df)

        map_html = buat_map(hasil)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GeoAI Pendidikan</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 30px; }}
            .container {{ max-width: 1000px; margin: auto; }}
            .map-box {{ height: 600px; border: 1px solid #ccc; margin-top: 20px; }}
            .upload-section {{ background: #f9f9f9; padding: 20px; border-radius: 8px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Analisis Geospasial Angka Partisipasi Sekolah (APS) 2025</h2>
            
            <div class="upload-section">
                <form method="POST" enctype="multipart/form-data">
                    <label>Upload File Excel BPS (APS):</label><br><br>
                    <input type="file" name="file" accept=".xlsx" required>
                    <button type="submit" style="padding: 5px 15px; cursor: pointer;">Analisis Data</button>
                </form>
            </div>

            <div class="map-box">
                {map_html}
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True, port=5000)