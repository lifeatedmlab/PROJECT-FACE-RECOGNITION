# PROJECT-FACE-RECOGNITION

## Deskripsi

Proyek ini adalah aplikasi pengenalan wajah yang dibangun menggunakan Flask dan OpenCV. Aplikasi ini memungkinkan pengguna untuk mengenali wajah dalam gambar atau video menggunakan model yang telah dilatih.

## Struktur Proyek

- `requirements.txt`: File yang berisi library yang harus diinstal sebelum menjalankan project.
- `faceRecognition_files`: Directory yang berisi file-file dan folder utama project, berikut isinya:
  - `app.py`: File utama untuk menjalankan aplikasi Flask.
  - `database.py`: Mengelola koneksi dan operasi database.
  - `dataset.py`: Mengumpulkan data wajah.
  - `face_recognition.py`: Modul untuk pengenalan wajah.
  - `train_classifier.py`: Melatih model pengenalan wajah.
  - `absensi.py`: Berisi fungsi untuk memasukkan data absen ke database dan mengecek apakah sudah ada data absen pada database.
  - `addevent.py`: Berisi fungsi untuk menambah data event ke database, mengecek apakah sudah ada data event pada database, dan generate event_id otomatis.
  - `addperson.py`: Berisi fungsi untuk menambah data anggota ke database dan mengecek apakah sudah ada data anggota pada database.
  - `login.py`: Berisi fungsi untuk login sebagai admin.
  - `static/`: Direktori untuk file statis seperti CSS, JavaScript, dan Image.
  - `templates/`: Direktori untuk template HTML (page).
  - `faceRecognition_files/resources/haarcascade_frontalface_default.xml`: File Haarcascade untuk deteksi wajah.
  - `faceRecognition_files/classifier_XYZ`: File XML hasil training setiap wajah anggota.

## Konfigurasi Database

Gunakan informasi berikut untuk menghubungkan aplikasi ke database:

- **Host**: `sql12.freesqldatabase.com`
- **Database name**: `sql12720243`
- **Database user**: `sql12720243`
- **Database password**: `Censored. Hubungi Admin untuk Meminta Akses`
- **Port number**: `3306`

## Konfigurasi Cloudflare R2 (S3 Compatible)

Gunakan informasi berikut untuk menghubungkan Cloud:

- **endpoint_url**: `https://a1c30d551c1d5963fc6afe44c3a6777c.r2.cloudflarestorage.com`,
- **region_name**: `apac`,
- **aws_access_key_id**: `d1862c406a16ad26eba46f3bcaa30f62`,
- **aws_secret_access_key**: `2546d0a0d348fe0460924bedda9fa1213a5c7e26fc312cd82ed0a6eeb65c41bc`

## How to Use

- **Instal Dependensi**: `pip install -r requirements.txt`
- **Konfigurasi Database**: Sesuaikan kodingan dengan konfigurasi yang telah di berikan
- **Konfigurasi Database**: Sesuaikan kodingan dengan konfigurasi yang telah di berikan
- **Running Applications**: `python app.py`

## Error handling while running

### 1. **Error pada Koneksi Database**

Jika aplikasi tidak bisa terhubung ke database, Anda mungkin melihat pesan error seperti "Can't connect to MySQL server" atau "Access denied for user" atau "Time Out"

#### Solusi:

- **Periksa Koneksi Database**: Pastikan detail koneksi database (host, user, password, database) sudah benar dan database MySQL berjalan dengan baik.
- **Periksa Port:** Pastikan port MySQL (3306 secara default) tidak diblokir oleh firewall atau sudah diatur dengan benar.
- **Uji Koneksi Secara Manual**: Anda bisa mencoba menghubungkan ke database secara manual menggunakan alat seperti MySQL CLI atau phpMyAdmin untuk memastikan semuanya berfungsi dengan baik.
- **Pastikan Internet Berjalan Lancar**: Gunakan pesan error spesifik untuk mencari solusi di forum atau dokumentasi terkait.
- **Restart Aplikasi**: Coba hentikan dan jalankan ulang aplikasi. Terkadang, ini bisa menyelesaikan masalah sementara.

### 2. **Error Importing Library**

Jika ada error yang terkait dengan modul atau pustaka yang tidak ditemukan, seperti "ModuleNotFoundError" atau lainnya

#### Solusi:

- **Pastikan Dependensi Terinstal**: Jalankan kembali perintah berikut untuk memastikan semua dependensi terinstal dengan benar
- **Cek Versi Python**: Pastikan Anda menggunakan versi Python yang kompatibel (disarankan Python 3.8 atau lebih baru) bisa install ulang dengan menyalahkan environtmentnya.
- **Lingkungan Virtual**: Jika Anda menggunakan lingkungan virtual (venv), pastikan sudah diaktifkan sebelum menjalankan aplikasi.

### 3. **Error pada Cloudflare R2 (S3 Compatible)**

Error yang terkait dengan koneksi ke Cloudflare R2, seperti "Access Denied" atau "Endpoint URL not found"

#### Solusi:

- **Periksa Kredensial**: Pastikan aws_access_key_id dan aws_secret_access_key sudah benar dan memiliki izin yang diperlukan.
- **Periksa Endpoint URL**: Verifikasi bahwa endpoint_url sudah benar dan dapat diakses dari jaringan Anda.
- **Restart Aplikasi**: Coba hentikan dan jalankan ulang aplikasi. Terkadang, ini bisa menyelesaikan masalah sementara.

### 4. **Error pada Pengenalan Wajah**

Jika pengenalan wajah tidak berjalan sebagaimana mestinya atau model tidak mendeteksi wajah.

#### Solusi:

- **Periksa File Haarcascade dan Classifier**: Pastikan file berada di lokasi yang benar dan tidak rusak.
- **Minta Daftar ulang Wajah**: Jika hasil pengenalan tidak memuaskan, pertimbangkan untuk melatih ulang model dengan dataset yang lebih besar atau lebih beragam.

### 5. **Error Tidak Terduga**

#### Solusi:

- **Restart Aplikasi**
- **Clone Ulang Aplikasi**
- **Hubungi Admin untuk lebih lanjut**
