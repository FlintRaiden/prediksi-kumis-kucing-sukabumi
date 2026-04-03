# 🌿 Sistem Proyeksi Produksi Komoditi Kumis Kucing
### Kabupaten Sukabumi – Jawa Barat

Aplikasi web berbasis **Flask** untuk memprediksi produksi tanaman
Kumis Kucing di Kabupaten Sukabumi menggunakan metode **Regresi Linear**.

Dibuat sebagai tugas mata kuliah **Kecerdasan Buatan (AI)**
Program Studi Teknik Informatika.

---

## 🛠️ Teknologi yang Digunakan
- Python 3 + Flask
- Scikit-learn (Linear Regression)
- Pandas & NumPy
- Bootstrap 5 + Chart.js
- Dataset: Open Data Dinas Perkebunan Jawa Barat

## 📊 Hasil Evaluasi Model
| Metrik | Nilai |
|--------|-------|
| R²     | 0.6567 |
| MAE    | 9.23 Ton |
| RMSE   | 12.84 Ton |

## 🚀 Cara Menjalankan
1. Clone repository ini
2. Aktifkan virtual environment
3. Install dependensi
4. Jalankan aplikasi

```bash
git clone https://github.com/FlintRaiden/prediksi-kumis-kucing-sukabumi.git
cd prediksi-kumis-kucing-sukabumi
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Buka browser: http://127.0.0.1:5000

## 📁 Struktur Folder
```
├── app.py              ← Backend Flask & model ML
├── data.csv            ← Dataset perkebunan
├── requirements.txt    ← Daftar library
└── templates/
    └── index.html      ← Tampilan web
```