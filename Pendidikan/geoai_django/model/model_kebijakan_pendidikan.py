import pandas as pd

class ModelKebijakanPendidikan:
    def __init__(self):
        # Bobot disesuaikan dengan prioritas Wajib Belajar (7-15 tahun)
        self.bobot = {
            "APS_7_12": 0.30,  # Usia SD
            "APS_13_15": 0.30, # Usia SMP
            "APS_16_18": 0.25, # Usia SMA/SMK
            "APS_19_23": 0.15  # Usia Perguruan Tinggi
        }

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        # 1. Normalisasi nama provinsi (agar cocok dengan GeoJSON)
        df["38 Provinsi"] = df["38 Provinsi"].str.upper().str.strip()

        # 2. Hitung Skor Partisipasi Pendidikan
        # Menjumlahkan nilai APS dikalikan bobot masing-masing kelompok umur
        df["Skor Pendidikan"] = (
            df["APS_7_12"] * self.bobot["APS_7_12"] +
            df["APS_13_15"] * self.bobot["APS_13_15"] +
            df["APS_16_18"] * self.bobot["APS_16_18"] +
            df["APS_19_23"] * self.bobot["APS_19_23"]
        )

        # 3. Klasifikasi (Rendah, Sedang, Tinggi)
        # Menggunakan kuantil agar pembagian kategori adil berdasarkan sebaran data
        df["Kategori Pendidikan"] = pd.qcut(
            df["Skor Pendidikan"],
            q=3,
            labels=["RENDAH", "SEDANG", "TINGGI"]
        )

        # 4. Keputusan Kebijakan Otomatis
        df["Keputusan Pemerintah"] = df["Kategori Pendidikan"].map({
            "RENDAH": (
                "INTERVENSI KHUSUS: Percepatan program wajib belajar, "
                "pemberian beasiswa KIP (Kartu Indonesia Pintar), "
                "dan pembangunan sekolah di area terpencil."
            ),
            "SEDANG": (
                "PENGUATAN: Optimalisasi fasilitas sekolah yang ada, "
                "peningkatan kualitas tenaga pendidik, dan kampanye lanjut sekolah."
            ),
            "TINGGI": (
                "MAINTENANCE: Pengembangan inovasi pendidikan digital "
                "dan peningkatan akses ke perguruan tinggi (usia 19-23)."
            )
        })

        return df