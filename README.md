# Tracker-sederhana
Tools anlitik untuk instagram 
# 📱 PANDUAN LENGKAP INSTAGRAM ANALYTICS TOOLS

## 🎯 Apa Itu Tools Ini?

Tools Python untuk analisis Instagram dengan 3 fitur utama:
1.Follower Tracke - Deteksi siapa yang unfollow Anda
2.Monitor Pertumbuha - Analisis pertumbuhan akun + grafik
3.Scraper Engagemen - Ambil data komentar & likes dari post

---




###Edit File main.py

Cari baris ini (sekitar baris 368):

```python
tools.login("username_anda", "password_anda")
```
Ganti dengan akun Instagram Anda

```python
tools.login("johndoe123", "passwordrahasia")
```

PENTING Simpan file setelah edit (`Cmd + S`)

---

##CARA MENGGUNAKAN

### Setiap Kali Mau Pakai Tools:

####STEP 1: Buka Terminal VSCod
```
Cmd + J
```

####STEP 2: Aktifkan Virtual Environmen
```bash
source venv/bin/activate
```

Akan muncul `(venv)` di terminal:
```
(venv) user@mac Python %
```

####STEP 3: Jalankan Tool
```bash
python main.py
```

####STEP 4: Pilih Fitu

Menu akan muncul:
```
============================================================
    INSTAGRAM ANALYTICS TOOLS
============================================================

============================================================
PILIH FITUR:
============================================================
1. Follower Tracker - Track followers & temukan unfollowers
2. Monitor Pertumbuhan - Analisis pertumbuhan akun
3. Scraper Engagement - Scrape komentar & likes dari post
============================================================

Pilih fitur (1/2/3):
```

Ketik,, atau, lalu Enter.

---

## PENJELASAN FITUR

### 1️ FOLLOWER TRACKER
Fungsi Deteksi siapa yang unfollow Anda atau ada follower baru
Cara Pakai
1. Pilih menu
2. Masukkan username target (bisa akun Anda atau akun lain)
3. Tunggu proses selesai
Output
- Daftar new followers
- Daftar unfollowers
- File JSON dengan history perubahan
File yang Dibuat
```
instagram_data/
├── username_followers.json     ← Data followers
└── username_changes.json       ← History perubahan
```
Tips
- Jalankan rutin (misal 1x sehari) untuk track perubahan
- Run pertama kali hanya simpan data, run kedua baru ada comparison

---

### 2 MONITOR PERTUMBUHAN
Fungsi Analisis pertumbuhan akun + buat grafik visual
Cara Pakai
1. Pilih menu
2. Masukkan username target
3. Tunggu proses selesai
Output
- Jumlah followers, following, posts
- Engagement rate otomatis dihitung
- Grafik pertumbuhan (PNG image)
File yang Dibuat
```
instagram_data/
├── username_growth.json        ← History data
└── username_growth_chart.png   ← Grafik visual
```
Yang Ditampilkan di Grafik
- Pertumbuhan Followers
- Pertumbuhan Following
- Jumlah Posts
- Engagement Rate
Tips
- Jalankan berkala untuk lihat tren
- Grafik muncul setelah ada minimal 2x data

---

### 3️ SCRAPER ENGAGEMENT
Fungsi Ambil data komentar & likes dari post tertentu
Cara Pakai
1. Pilih menu
2. Masukkan URL post Instagram
   ```
   Contoh: https://www.instagram.com/p/ABC123xyz/
   ```
3. Masukkan max komentar (default: 100)
4. Masukkan max likes (default: 100)
5. Tunggu proses selesai
Output
- List username yang like
- List komentar dengan username
- Export ke JSON dan Excel
File yang Dibuat
```
instagram_data/
├── post_ABC123xyz_engagement.json    ← Data mentah
└── post_ABC123xyz_engagement.xlsx    ← Excel file
```
Isi Excel File
- Sheet 1:Comment (username, text, created_at, likes)
- Sheet 2:Like (username, full_name)
Tips
- Bisa analisis kompetitor
- Riset audience yang engage
- Cari potential customers/collaborators

---

## 📂 STRUKTUR FOLDER PROJECT

```
Python/
├── main.py                  ← File kode utama
├── venv/                    ← Virtual environment (jangan hapus)
└── instagram_data/          ← Output data (auto-created)
    ├── *.json               ← Data mentah
    ├── *.xlsx               ← Excel files
    └── *.png                ← Grafik
```

---

##  TROUBLESHOOTING

###  Error: "Login failed"
Penyebab
- Username/password salah
- Instagram block login dari script
- Perlu verifikasi 2FA
Solusi
1. Cek username & password di `main.py`
2. Coba login manual di browser dulu
3. Kalau ada 2FA, gunakan session:

```python
# Login pertama kali (dengan password)
tools.login("username", "password")

# Login berikutnya (tanpa password)
tools.load_session("username")
```

---

### Error: "Rate limited"
Penyebab
Instagram limit request (terlalu banyak/cepat)
Solusi
- Tunggu 15-30 menit
- Jangan scrape terlalu banyak sekaligus
- Kurangi `max_comments` dan `max_likes`

---

### Error: "No module named 'instaloader'"
Penyebab
Virtual environment tidak aktif atau library belum terinstall
Solusi
```bash
# Aktifkan venv
source venv/bin/activate

# Install ulang
pip install instaloader pandas matplotlib openpyxl
```

---

### Error: "Private account"
Penyebab
Akun target private dan Anda tidak follow
Solusi
- Follow akun tersebut dulu
- Atau hanya bisa track akun public

---

## TIPS & BEST PRACTICES

### DO (Lakukan)

1.Jalankan di waktu yang sama setiap har
   - Misal: setiap pagi jam 9
   - Data lebih konsisten untuk analisis

2.Backup data secara berkal
   - Copy folder `instagram_data/`
   - Simpan di cloud atau external drive

3.Gunakan untuk akun sendir
   - Legal dan aman
   - Insight untuk strategi konten

4.Test dengan data kecil dul
   - Misal: max 50 comments, 50 likes
   - Kalau lancar, baru naikkan

5.Gunakan session setelah login pertam
   - Lebih aman dari block
   - Tidak perlu input password berulang

### DON'T (Jangan)

1.Jangan scrape terlalu agresi
   - Bisa kena rate limit atau banned
   - Max 100-200 request per jam

2.Jangan share password di kod
   - Kalau share kode, hapus password dulu
   - Atau gunakan environment variable

3.Jangan spam automatio
   - Instagram deteksi bot behavior
   - Fokus ke analytics, bukan automation

4.Jangan scrape akun orang terus-meneru
   - Bisa dianggap stalking
   - Respect privacy

---

## KEAMANAN

### Proteksi Password:

Kalau mau lebih aman, gunakan environment variable:

```python
import os

# Di terminal, set variable:
# export IG_USER="username_anda"
# export IG_PASS="password_anda"

# Di kode:
tools.login(os.getenv('IG_USER'), os.getenv('IG_PASS'))
```

### .gitignore:

Kalau pakai Git, buat file `.gitignore`:

```
venv/
instagram_data/
__pycache__/
.DS_Store
*.pyc
```

---

##  WORKFLOW HARIAN RECOMMENDED

### Morning Routine (10 menit):

```bash
# 1. Aktifkan venv
source venv/bin/activate

# 2. Track followers
python main.py
# Pilih: 1 (Follower Tracker)
# Input: username_anda

# 3. Monitor growth
python main.py
# Pilih: 2 (Monitor Pertumbuhan)
# Input: username_anda

# 4. Matikan venv
deactivate
```

### Weekly Analysis:

1. Buka grafik pertumbuhan di `instagram_data/`
2. Analisis tren followers
3. Cek engagement rate
4. Adjust strategi konten

---

##  COMMAND CHEAT SHEET

### Virtual Environment:
```bash
# Aktifkan
source venv/bin/activate

# Matikan
deactivate

# Cek apakah aktif
which python
```

### Jalankan Tools:
```bash
# Run dengan menu
python main.py

# Atau langsung dari kode (edit main.py)
python main.py
```

### Install/Update Library:
```bash
# Install semua
pip install instaloader pandas matplotlib openpyxl

# Update library
pip install --upgrade instaloader
```

### Cek Version:
```bash
# Cek Python
python3 --version

# Cek library
pip list | grep instaloader
```

---

## NEED HELP?

### Dokumentasi Library:
-Instaloader https://instaloader.github.io/
-Pandas https://pandas.pydata.org/
-Matplotlib https://matplotlib.org/

### Common Issues:
1.Login erro → Cek kredensial di `main.py`
2.Rate limi → Tunggu 30 menit, coba lagi
3.Module erro → Pastikan venv aktif
4.Private accoun → Follow dulu atau pilih akun public
---
Last Updated November 2024  Python Version 3.8+  OS macOS (compatible with Linux/Windows)
