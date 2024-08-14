# PROJECT-FACE-RECOGNITION

## Deskripsi
Proyek ini adalah aplikasi pengenalan wajah yang dibangun menggunakan Flask dan OpenCV. Aplikasi ini memungkinkan pengguna untuk mengenali wajah dalam gambar atau video menggunakan model yang telah dilatih.

## Struktur Proyek


- `faceRecognition_files`: Directory yang berisi file-file dan folder utama project, berikut isinya:
  - `app.py`: File utama untuk menjalankan aplikasi Flask.
  - `database.py`: Mengelola koneksi dan operasi database.
  - `dataset.py`: Mengumpulkan data wajah.
  - `face_recognition.py`: Modul untuk pengenalan wajah.
  - `train_classifier.py`: Melatih model pengenalan wajah.
  - `static/`: Direktori untuk file statis seperti CSS, JavaScript, dan gambar.
  - `templates/`: Direktori untuk template HTML.
  - `faceRecognition_files/resources/haarcascade_frontalface_default.xml`: File Haarcascade untuk deteksi wajah.


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
