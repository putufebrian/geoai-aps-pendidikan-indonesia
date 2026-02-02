# GeoAI Pendidikan Indonesia (APS 2025)

Aplikasi GeoAI untuk analisis geospasial Angka Partisipasi Sekolah (APS) 2025 di Indonesia.  
Sistem ini mengintegrasikan data BPS, model kebijakan pendidikan berbobot, dan visualisasi peta interaktif (Folium) untuk menghasilkan rekomendasi kebijakan pendidikan otomatis per provinsi.
Proyek ini dikembangkan sebagai Sistem Pendukung Keputusan (SPK) berbasis GeoAI untuk analisis kebijakan pendidikan nasional.
Fokus: GeoAI, Sistem Pendukung Keputusan, dan Visualisasi Geospasial
---

## Fitur Utama
- Upload file Excel APS BPS 2025
- Prediksi Skor Pendidikan per provinsi
- Klasifikasi otomatis (RENDAH, SEDANG, TINGGI)
- Rekomendasi Keputusan Kebijakan Pemerintah
- Visualisasi peta interaktif provinsi Indonesia

---

## Konsep Model Kebijakan Pendidikan

Model menggunakan pembobotan Angka Partisipasi Sekolah (APS) berdasarkan prioritas Wajib Belajar nasional:

| Kelompok Umur | Bobot |
| ------------- | ----- |
| 7–12 Tahun (SD) | 0.30 |
| 13–15 Tahun (SMP) | 0.30 |
| 16–18 Tahun (SMA/SMK) | 0.25 |
| 19–23 Tahun (Perguruan Tinggi) | 0.15 |

Klasifikasi kategori pendidikan dilakukan menggunakan metode kuantil (qcut) agar pembagian kategori adil berdasarkan sebaran data nasional.

---

## Struktur Folder Proyek

```
geoai_django/
├── manage.py
├── data/
│   ├── gabungan_38_wilayah_batas_provinsi.geojson
│   └── gabungan_38_wilayah_batas_kabkota.geojson
├── model/
│   ├── buat_model_pkl.py
│   ├── model_kebijakan_pendidikan.py
│   ├── model_kebijakan_pendidikan_2025.pkl
│   └── __init__.py
├── geoai_django/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __init__.py
└── pendidikan/
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    ├── migrations/
    │   └── __init__.py
    └── templates/
        └── index.html
```

---

## Sumber Data

Badan Pusat Statistik Indonesia.  
Angka Partisipasi Sekolah (APS) Menurut Provinsi dan Kelompok Umur, 2025.  
Diakses pada 2 Februari 2026.  
https://www.bps.go.id/id/statistics-table/2/MjIxMSMy/angka-partisipasi-sekolah--aps--menurut-provinsi-dan-kelompok-umur.html

---

## Teknologi yang Digunakan
- Python 3.10
- Django
- Pandas
- GeoPandas
- Folium
- Pickle
- HTML

---

## Cara Menjalankan Aplikasi

Clone repository:
```
git clone https://github.com/username/geoai-aps-pendidikan-indonesia.git
cd geoai-aps-pendidikan-indonesia
```

Install dependency:
```
pip install django pandas geopandas folium openpyxl
```

Jalankan server Django:
```
python manage.py runserver
```

Akses aplikasi di browser:
```
http://127.0.0.1:8000/
```

---

## Cara Menggunakan Aplikasi
1. Upload file Excel APS dari BPS
2. Sistem membaca dan membersihkan data secara otomatis
3. Model kebijakan menghitung skor dan kategori pendidikan
4. Peta interaktif ditampilkan dengan warna kategori, tooltip informasi, dan popup rekomendasi kebijakan

---

## Output Sistem
- Skor Pendidikan per Provinsi
- Kategori Pendidikan (RENDAH, SEDANG, TINGGI)
- Keputusan Kebijakan Pemerintah:
  - Intervensi khusus
  - Penguatan sistem pendidikan
  - Maintenance dan inovasi pendidikan
