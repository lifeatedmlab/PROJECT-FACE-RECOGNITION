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
- **Database name**: `sql12717385`
- **Database user**: `sql12717385`
- **Database password**: `9YhkHLjLSS`
- **Port number**: `3306`

## Use
- **requirement**: `pip install -r requirements.txt`
- **deleted.py**: `python deleted.py`
  
## Catatan Penting
- Hapus File `classifier.xml` : Setiap kali menggunakan aplikasi, harap hapus file `classifier.xml` dan backup file ini jika diperlukan.
- Hapus Foto di Direktori Dataset: Hapus foto-foto di direktori dataset setelah selesai penggunaan.
- jika database lemot bisa menggunakan local
