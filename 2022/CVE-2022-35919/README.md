# Minio Security Vulnerability Checker

## Deskripsi

Program ini adalah alat (*tool*) yang dibuat untuk memeriksa keamanan sistem Minio terkait dengan kerentanan CVE-2022-35919. Alat ini dirancang untuk membantu pengguna dalam mendeteksi potensi kerentanan di dalam konfigurasi Minio mereka.

## Cara Penggunaan

1. Pastikan Anda telah menginstal Python (versi 3.x) di sistem Anda.
2. Unduh skrip `minio_security_checker.py` dari repositori ini.
3. Buka terminal atau command prompt, dan jalankan skrip dengan perintah:

    ```bash
    python minio_security_checker.py -u <URL_Target> -a <Minio_AccessKey> -s <Minio_SecretKey>
    ```

    Gantilah `<URL_Target>`, `<Minio_AccessKey>`, dan `<Minio_SecretKey>` dengan informasi yang sesuai.

4. Tunggu hingga skrip menyelesaikan prosesnya. Hasil akan ditampilkan di terminal.

## Kegunaan

Alat ini berguna untuk:

- Mendeteksi kerentanan keamanan CVE-2022-35919 pada sistem Minio.
- Memberikan informasi tentang potensi masalah di dalam URL yang disediakan.

## Author

Nama: ifulxpkoit  
Email: ifulxploit@gmail.com

**Catatan**: Pastikan untuk menggunakan alat ini secara etis dan hanya untuk tujuan keamanan yang sah. Jangan mencoba mengeksploitasi sistem yang bukan milik Anda tanpa izin.
