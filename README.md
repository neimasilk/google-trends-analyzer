# Google Trends Analyzer Indonesia

Proyek Python untuk menganalisis dan mengambil data trending dari Google Trends Indonesia. Mendukung pengambilan trend umum, trend teknologi, dan memiliki fitur filter untuk menghapus konten temporer (seperti berita olahraga).

## Fitur

- 🔍 Mengambil trending searches dari Google Trends Indonesia
- 🏷️ Mendukung pengambilan trend berdasarkan kategori (teknologi, dll)
- ⏱️ Filter otomatis untuk konten temporer dan berita olahraga
- 📊 Output dalam format Markdown yang rapi
- 🔄 Mendukung multiple timeframes untuk trend teknologi

## Persyaratan Sistem

- Python 3.9+
- pandas 2.1.0+
- pytrends 4.9.0+

## Instalasi

### Menggunakan Anaconda (Direkomendasikan)
1. Clone repository ini:
```bash
git clone [URL_REPOSITORY]
cd google-trends-analyzer
```

2. Buat environment baru dengan file environment.yml:
```bash
conda env create -f environment.yml
```

### Menggunakan pip
1. Clone repository ini:
```bash
git clone [URL_REPOSITORY]
cd google-trends-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Penggunaan

### Mengambil Trend Umum
```bash
python get_trends.py
```
Output akan disimpan dalam file `trends_[TIMESTAMP].md`

### Mengambil Trend Teknologi
```bash
python get_tech_trends.py
```
Output akan disimpan dalam file `tech_trends_[TIMESTAMP].md`

### Melihat Kategori yang Tersedia
```bash
python get_categories.py
```

## Struktur Proyek

```
google-trends-analyzer/
├── get_trends.py          # Script utama untuk mengambil trend umum
├── get_tech_trends.py     # Script untuk mengambil trend teknologi
├── get_categories.py      # Script untuk melihat kategori yang tersedia
├── requirements.txt       # Daftar dependencies untuk pip
├── environment.yml        # File konfigurasi environment Anaconda
└── README.md             # Dokumentasi proyek
```

## Kontribusi

Silakan berkontribusi dengan membuat pull request atau melaporkan issues.

## Lisensi

MIT License - lihat file [LICENSE](LICENSE) untuk detail lebih lanjut.

## Author

Mukhlis Amien

---
_Dibuat dengan ❤️ untuk komunitas developer Indonesia_ 