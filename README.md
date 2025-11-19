# 🍽️ FoodLover.AI

<div align="center">

![FoodLover Banner](https://img.shields.io/badge/FoodLover-AI%20Powered-orange?style=for-the-badge&logo=chef&logoColor=white)
[![C++](https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)](https://isocpp.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

**Aplikasi Rekomendasi Resep Cerdas dengan Fuzzy Logic & Machine Learning**

[Fitur](#-fitur-unggulan) • [Instalasi](#-instalasi) • [Penggunaan](#-cara-penggunaan) • [Teknologi](#-teknologi) • [Kontribusi](#-kontribusi)

</div>

---

## 📋 Tentang Project

**FoodLover.AI** adalah aplikasi desktop berbasis C++/CLI dengan backend Python Flask yang menggunakan **Fuzzy Logic** untuk memberikan rekomendasi resep makanan berdasarkan bahan-bahan yang Anda miliki di rumah. Aplikasi ini dilengkapi dengan sistem pembelajaran otomatis yang semakin pintar seiring penggunaan.

### 🎯 Masalah yang Diselesaikan
- ❌ Bingung mau masak apa dengan bahan seadanya
- ❌ Tidak tahu kombinasi bahan apa yang cocok
- ❌ Kesulitan mencari resep berdasarkan preferensi rasa
- ❌ Typo saat mencari bahan (misal: "bwang" vs "bawang")

### ✅ Solusi FoodLover.AI
- ✨ Input bahan yang ada, dapatkan rekomendasi resep instan
- ✨ Filter berdasarkan rasa (Pedas, Manis, Gurih, Asam, dll)
- ✨ Fuzzy matching untuk menangani typo dan sinonim
- ✨ Sistem feedback untuk pembelajaran berkelanjutan
- ✨ Database resep yang terus berkembang

---

## 🌟 Fitur Unggulan

### 1. 🔍 Pencarian Cerdas dengan Fuzzy Logic
- **Toleransi Typo**: Mengenali "ayam gorng" sebagai "ayam goreng"
- **Sinonim Detection**: Memahami "tomat" = "tomato"
- **Partial Matching**: "ayam" cocok dengan "daging ayam"
- **Score-based Ranking**: Resep dengan bahan paling cocok muncul di atas

### 2. 🎨 Interface User-Friendly
- **Modern GUI**: Antarmuka grafis yang intuitif dan menarik
- **Real-time Search**: Hasil muncul langsung saat pencarian
- **Detail Resep**: Menampilkan bahan lengkap dan bahan yang cocok
- **Filter Rasa**: Dropdown untuk memfilter resep berdasarkan preferensi

### 3. 📊 Sistem Feedback & Learning
- **User Feedback**: Rating resep untuk meningkatkan rekomendasi
- **Auto-save**: Feedback tersimpan otomatis di database
- **Learning Algorithm**: Sistem belajar dari preferensi pengguna
- **History Tracking**: Menyimpan riwayat pencarian

### 4. 🗄️ Database Management
- **Dynamic Database**: Tambah resep baru via API
- **JSON Storage**: Database ringan dan mudah di-maintain
- **Kamus Sinonim**: Database kata sinonim untuk pencarian lebih baik
- **RESTful API**: Backend terpisah untuk skalabilitas

---

## 🛠️ Teknologi

### Frontend (Desktop Application)
| Teknologi | Versi | Fungsi |
|-----------|-------|--------|
| C++/CLI | Visual Studio 2022 | Language utama aplikasi desktop |
| Windows Forms | .NET Framework | GUI Framework |
| JSON Parser | Native | Parsing data dari server |
| HTTP Client | System.Net | Komunikasi dengan backend |

### Backend (API Server)
| Teknologi | Versi | Fungsi |
|-----------|-------|--------|
| Python | 3.8+ | Language backend |
| Flask | 2.x | Web framework untuk REST API |
| TheFuzz | 0.19+ | Fuzzy string matching library |
| JSON | Built-in | Database storage |

### Algoritma & Logic
- **Fuzzy Logic**: Pencocokan bahan dengan toleransi kesalahan
- **Scoring System**: Algoritma ranking berdasarkan kecocokan
- **Synonym Mapping**: Database sinonim untuk pencarian lebih akurat
- **Machine Learning**: Pembelajaran dari feedback pengguna

---

## 📥 Instalasi

### Prerequisites
- Visual Studio 2022 (dengan C++/CLI support)
- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Step 1: Clone Repository
```bash
git clone https://github.com/RaffaelVeneh/FoodLover.AI.git
cd FoodLover.AI
```

### Step 2: Setup Backend (Python Server)
```bash
cd FoodServer
pip install flask thefuzz python-Levenshtein
python server.py
```
Server akan berjalan di `http://localhost:5000`

### Step 3: Setup Frontend (C++ Application)
1. Buka `Project1.sln` dengan Visual Studio 2022
2. Build Solution (Ctrl + Shift + B)
3. Run Project (F5)

### Step 4: Konfigurasi (Opsional)
Edit file konfigurasi jika perlu mengubah port server:
```cpp
// Di MainForm.h, ubah URL server jika diperlukan
String^ urlServer = "http://localhost:5000/cari";
```

---

## 🚀 Cara Penggunaan

### 1. Jalankan Server Backend
```bash
cd FoodServer
python server.py
```
Output:
```
[INFO] Kamus berhasil dimuat: 150 kata sinonim.
 * Running on http://127.0.0.1:5000
```

### 2. Jalankan Aplikasi Desktop
- Buka FoodLover.exe atau jalankan dari Visual Studio

### 3. Cari Resep
1. **Input Bahan**: Ketik bahan yang Anda punya (pisahkan dengan koma)
   ```
   Contoh: ayam, bawang, cabai, tomat
   ```

2. **Pilih Rasa**: Pilih preferensi rasa dari dropdown
   - Semua
   - Pedas
   - Manis
   - Gurih
   - Asam
   - Asin

3. **Klik "Cari Resep"**: Hasil akan muncul dalam bentuk list

4. **Lihat Detail**: Klik resep untuk melihat bahan lengkap

### 4. Berikan Feedback
- Pilih resep yang sudah dicoba
- Klik tombol "Feedback"
- Isi form rating dan komentar
- Sistem akan belajar dari feedback Anda!

---

## 📁 Struktur Project

```
FoodLover.AI/
│
├── FoodServer/                 # Backend Python Flask
│   ├── server.py              # Main server file
│   ├── resep.json             # Database resep
│   └── kamus.json             # Database sinonim
│
├── Project1/                   # Frontend C++/CLI
│   ├── FoodLover.cpp          # Entry point
│   ├── MainForm.h/cpp         # Form utama
│   ├── FeedbackForm.h/cpp     # Form feedback
│   ├── DataModels.h           # Data structures
│   ├── MenuData.h             # Menu models
│   └── feedback.txt           # User feedback storage
│
├── x64/Debug/                  # Build output
│   └── FoodLover.exe          # Executable file
│
├── Project1.sln               # Visual Studio Solution
└── README.md                  # Dokumentasi (file ini)
```

---

## 🔌 API Endpoints

### 1. Cari Resep
```http
POST /cari
Content-Type: application/json

{
  "bahan": "ayam, bawang, cabai",
  "rasa": "Pedas"
}
```

**Response:**
```json
[
  {
    "nama": "Ayam Rica-Rica",
    "rasa": "Pedas",
    "skor": 3,
    "bahan_lengkap": "ayam|bawang|cabai|tomat",
    "bahan_match": "ayam|bawang|cabai"
  }
]
```

### 2. Tambah Resep Baru
```http
POST /tambah
Content-Type: application/json

{
  "nama": "Soto Ayam",
  "rasa": "Gurih",
  "bahan": ["ayam", "kunyit", "serai", "daun jeruk"]
}
```

---

## 🧪 Contoh Penggunaan

### Skenario 1: Punya Bahan Terbatas
```
Input: "telur, nasi, kecap"
Filter: Semua
Output: 
  1. Nasi Goreng Pedas (Skor: 3)
  2. Telur Dadar Gurih (Skor: 1)
```

### Skenario 2: Mau Masak Pedas
```
Input: "ayam, cabai"
Filter: Pedas
Output:
  1. Ayam Rica-Rica (Skor: 2)
  2. Sambal Goreng Ayam (Skor: 2)
```

### Skenario 3: Typo di Input
```
Input: "bwang, telor, cabe"  (typo)
Filter: Semua
Output: Tetap menemukan resep yang cocok! ✨
```

---

## 🎓 Algoritma Fuzzy Logic

### Cara Kerja
```python
def cek_kemiripan(bahan_user, bahan_resep):
    # 1. Cek Sinonim
    bahan_user = KAMUS.get(bahan_user, bahan_user)
    
    # 2. Exact Match
    if bahan_user == bahan_resep:
        return True
    
    # 3. Fuzzy Matching (Typo Tolerance)
    skor = fuzz.ratio(bahan_user, bahan_resep)
    if skor > 80:  # 80% similarity
        return True
    
    # 4. Partial Match
    if bahan_user in bahan_resep:
        return True
    
    return False
```

### Scoring System
- **Perfect Match**: +1 point per bahan
- **Ranking**: Diurutkan dari skor tertinggi
- **Threshold**: Minimal 1 bahan cocok untuk masuk hasil

---

## 🤝 Kontribusi

Kontribusi sangat terbuka! Berikut cara berkontribusi:

1. **Fork** repository ini
2. **Clone** fork Anda
3. **Buat branch** baru (`git checkout -b fitur-baru`)
4. **Commit** perubahan (`git commit -m 'Menambah fitur X'`)
5. **Push** ke branch (`git push origin fitur-baru`)
6. Buat **Pull Request**

### Areas yang Bisa Dikontribusi
- 📝 Menambah database resep
- 🔧 Optimasi algoritma fuzzy logic
- 🎨 Perbaikan UI/UX
- 🌐 Menambah fitur multi-language
- 📱 Membuat versi mobile
- 🧪 Menambah unit testing

---

## 📝 TODO List

- [ ] Implementasi rating sistem yang lebih advanced
- [ ] Export/import resep ke PDF
- [ ] Integrasi dengan API resep online
- [ ] Mode offline dengan cache
- [ ] Nutrisi information untuk setiap resep
- [ ] Gambar/foto untuk setiap resep
- [ ] Voice input untuk bahan
- [ ] Meal planning feature

---

## 🐛 Known Issues

- [ ] Server perlu dijalankan manual sebelum aplikasi
- [ ] Belum support Unicode characters sepenuhnya
- [ ] Performance bisa lambat dengan database > 1000 resep

---

## 📄 Lisensi

Project ini dibuat untuk keperluan **Ujian Akhir Semester** mata kuliah Algoritma.

```
Copyright (c) 2025 Raffael Veneh
All Rights Reserved
```

---

## 👨‍💻 Developer

**Raffael Veneh**
- GitHub: [@RaffaelVeneh](https://github.com/RaffaelVeneh)
- Repository: [FoodLover.AI](https://github.com/RaffaelVeneh/FoodLover.AI)

---

## 🙏 Acknowledgments

- **TheFuzz Library** - Untuk algoritma fuzzy string matching
- **Flask Framework** - Untuk backend API yang mudah
- **Visual Studio** - IDE terbaik untuk C++ development
- **Stack Overflow Community** - Untuk solusi berbagai masalah teknis

---

## 📞 Dukungan

Jika mengalami masalah atau punya pertanyaan:

1. **Bug Report**: Buat issue di GitHub
2. **Feature Request**: Diskusi di GitHub Discussions
3. **Documentation**: Baca bagian [Cara Penggunaan](#-cara-penggunaan)

---

<div align="center">

### ⭐ Jika project ini membantu, berikan star di GitHub! ⭐

**Made with ❤️ and 🍕 by Raffael Veneh**

[⬆ Kembali ke atas](#️-foodloverai)

</div>