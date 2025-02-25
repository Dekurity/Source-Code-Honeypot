# 🛡️ Aplikasi Honeypot

Ini adalah aplikasi honeypot yang dikembangkan oleh Dekurity. Aplikasi ini dirancang untuk mensimulasikan server yang rentan dan mencatat upaya akses tidak sah. Aplikasi ini mengirimkan notifikasi melalui WhatsApp menggunakan CallMeAPI dan menyediakan dasbor untuk memantau statistik serangan.

## 📋 Fitur

- 🕵️ Endpoint rentan yang disimulasikan untuk menarik penyerang
- 📝 Pencatatan upaya akses tidak sah
- ⏱️ Pembatasan tingkat (rate limiting) untuk mencegah penyalahgunaan
- 🚫 Pemblokiran IP setelah ambang batas upaya serangan tercapai
- 📲 Notifikasi melalui WhatsApp menggunakan CallMeAPI
- 📊 Dasbor untuk memvisualisasikan statistik serangan dan log
- 🧹 Fitur untuk menghapus log

## 🛠️ Persyaratan

- Python 3.9 atau lebih tinggi
- Flask
- Requests
- Flask-Limiter
- Akun CallMeAPI dan kunci API

## 🚀 Instalasi

1. **Klon repo:**
    ```bash
    git clone https://github.com/Dekurity/Source-Code-Honeypot.git
    cd Source-Code-Honeypot
    ```

2. **Buat lingkungan virtual dan aktifkan:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Pada Windows gunakan `venv\Scripts\activate`
    ```

3. **Instal dependensi:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Atur variabel lingkungan:**
    ```bash
    export CALLMEAPI_KEY="your_callmeapi_key"
    export CALLMEAPI_PHONE_NUMBER="your_phone_number"
    ```
    > ⚠️ **Penting:** Gantilah `your_callmeapi_key` dengan API key Anda dari CallMeAPI dan `your_phone_number` dengan nomor telepon yang akan menerima notifikasi WhatsApp.

5. **Jalankan aplikasi:**
    ```bash
    python honeypot.py
    ```

## 🐳 Docker

Anda juga dapat menjalankan aplikasi menggunakan Docker:

1. **Bangun image Docker:**
    ```bash
    docker build -t honeypot .
    ```

2. **Jalankan container Docker:**
    ```bash
    docker run -d -p 5000:5000 -e CALLMEAPI_KEY="your_callmeapi_key" -e CALLMEAPI_PHONE_NUMBER="your_phone_number" honeypot
    ```
    > ⚠️ **Penting:** Gantilah `your_callmeapi_key` dengan API key Anda dari CallMeAPI dan `your_phone_number` dengan nomor telepon yang akan menerima notifikasi WhatsApp.

## 📚 Penggunaan

Aplikasi menyediakan endpoint berikut:

- `/` - Halaman utama
- `/admin` - Halaman admin yang disimulasikan
- `/login` - Halaman login yang disimulasikan
- `/db` - Halaman akses database yang disimulasikan
- `/robots.txt` - File robots.txt yang disimulasikan
- `/config` - Akses file konfigurasi yang disimulasikan
- `/wp-login.php` - Halaman login WordPress yang disimulasikan
- `/backup.zip` - File backup yang disimulasikan
- `/shell.php` - Halaman upload web shell yang disimulasikan
- `/api/admin` - Akses API admin yang disimulasikan
- `/honeypot-stats` - Endpoint JSON untuk mendapatkan statistik serangan
- `/clear-logs` - Endpoint untuk menghapus log (permintaan POST)
- `/dashboard` - Dasbor untuk memvisualisasikan statistik serangan dan log

## 📊 Dasbor

Dasbor menyediakan tampilan detail log serangan terbaru dan statistik serangan. Anda dapat mengaksesnya di `/dashboard`.

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan buka issue atau kirim pull request untuk perbaikan atau bug fix.

## 📄 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT.
