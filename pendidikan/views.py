import os
import pandas as pd
import geopandas as gpd
import folium
import pickle
from django.shortcuts import render
from django.conf import settings

# =========================
# PATH AMAN (DJANGO WAY)
# =========================
BASE_DIR = settings.BASE_DIR

MODEL_PATH = os.path.join(BASE_DIR, "model", "model_kebijakan_pendidikan_2025.pkl")
GEOJSON_PATH = os.path.join(BASE_DIR, "data", "gabungan_38_wilayah_batas_provinsi.geojson")

# =========================
# LOAD MODEL
# =========================
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# =========================
# LOAD GEOJSON
# =========================
gdf = gpd.read_file(GEOJSON_PATH)
gdf["name"] = gdf["name"].str.upper().str.strip()

WARNA = {
    "RENDAH": "#d73027",
    "SEDANG": "#fee08b",
    "TINGGI": "#1a9850"
}

# =========================
# FUNGSI MAP
# =========================
def buat_map(data=None):
    peta = folium.Map(
        location=[-2.5, 118],
        zoom_start=5,
        tiles="cartodbpositron"
    )

    if data is not None:
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
                    "#cccccc"
                ),
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.8
            },
            tooltip=folium.GeoJsonTooltip(
                fields=[
                    "name",
                    "Skor Pendidikan",
                    "Kategori Pendidikan"
                ],
                aliases=[
                    "Provinsi:",
                    "Skor Pendidikan:",
                    "Kategori:"
                ],
                localize=True
            ),
            popup=folium.GeoJsonPopup(
                fields=["Keputusan Pemerintah"],
                aliases=["Rekomendasi Kebijakan:"],
                localize=True
            )
        ).add_to(peta)

    return peta._repr_html_()

# =========================
# VIEW UTAMA
# =========================
def index(request):
    map_html = buat_map()

    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]

        df = pd.read_excel(file, skiprows=4, header=None)
        df = df.iloc[:, [0, 1, 2, 3, 4]]
        df.columns = [
            "38 Provinsi",
            "APS_7_12",
            "APS_13_15",
            "APS_16_18",
            "APS_19_23"
        ]

        df = df.dropna(subset=["38 Provinsi"])
        df["38 Provinsi"] = df["38 Provinsi"].str.upper().str.strip()

        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # 🔥 INI INTI NYA
        hasil = model.predict(df)

        map_html = buat_map(hasil)

    return render(request, "index.html", {"map": map_html})
