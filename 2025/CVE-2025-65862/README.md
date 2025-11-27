# CVE-2025-65862 — Dokumentasi, Analisis, dan Automation Tool (Research Purposes Only)

> ⚠️ **Peringatan Etika & Legal**
> Seluruh materi dalam repository ini disediakan hanya untuk:
> - penelitian keamanan,
> - pembelajaran,
> - analisis kerentanan,
> - dan pengujian di lingkungan yang dimiliki atau memiliki izin eksplisit.
>
> Melakukan eksploitasi, penyalahgunaan bug, atau pengunggahan file berbahaya ke server pihak ketiga **tanpa izin** adalah tindakan ilegal dan melanggar hukum Indonesia (UU ITE) serta hukum internasional.  
> Penulis tidak bertanggung jawab atas penyalahgunaan alat atau teknik yang dijelaskan.

---

## 📌 Ringkasan CVE-2025-65862

- **CVE ID** : CVE-2025-65862  
- **Produk terdampak** : SLiMS Bulian v9.7.2  
- **Klasifikasi** : Arbitrary File Write → Remote Code Execution (RCE)  
- **Tingkat Keparahan** : Tinggi  
- **Sumber publik penelitian** :  
  https://medium.com/@xpl0dec/zeroday-slims9-bulian-v9-7-2-arbitrary-file-write-to-rce-6a458ad7960f

### 🧩 Apa masalahnya?

Pada SLiMS Bulian 9.7.2, terdapat **misconfiguration** ketika pengguna (dengan kredensial lemah) mengunggah file ZIP plugin.

Alurnya:

1. Aplikasi menerima upload file ZIP.
2. Sistem melakukan ekstraksi otomatis.
3. File hasil ekstraksi ditempatkan ke:
4. **Semua file di dalam ZIP ikut diekstraksi**, termasuk file `.php`.
5. Jika ZIP berisi file backdoor seperti:
   ```zip/
   └── myplugin/
   └── shell.php
   ```
   Maka file dapat diakses melalui: **/plugins/myplugin/shell.php**
6. Ini dapat menyebabkan **arbitrary file write** → **remote code execution** apabila admin memakai password lemah.

---

## 🔍 Indikator Kompromi (IOC)

Jika Anda mengelola SLiMS, perhatikan hal berikut:

- Terdapat folder mencurigakan di `/plugins/`
- File PHP asing di dalam folder plugin
- Log upload plugin dari akun dengan password lemah
- Aktivitas file yang tidak biasa setelah upload ZIP
- Request mencurigakan ke: 
   /plugins/<nama-plugin>/something.php

---

## 🛡️ Mitigasi & Rekomendasi

1. **Update SLiMS ke versi terbaru atau patch keamanan yang tersedia.**  
2. **Ganti password admin/user** dengan standar kuat (aturan CISA.gov).  
3. **Nonaktifkan upload plugin** jika tidak digunakan.  
4. **Pantau direktori `/plugins/`** dan hapus file yang tidak dikenal.  
5. **Audit log admin** untuk melihat upload tidak sah.  
6. **Isolasi sistem** jika diduga terkompromi.  
7. **Restore dari backup** sebelum insiden terjadi.

---

## ⚙️ Dokumentasi Automation Script

Skript ini digunakan untuk:
- melakukan automasi pengujian terhadap misconfiguration CVE-2025-65862,
- menguji apakah sebuah instance SLiMS rentan,
- mengunggah ZIP plugin yang berisi payload *untuk penelitian*.

--- 

### 🎛️ **Arguments**

| Flag | Fungsi                                                           |
|------|------------------------------------------------------------------|
|  -l  | Path file list target SLiMS                                      |
|  -f  | ZIP plugin yang ingin diuji (berisi payload/backdoor penelitian) |
|  -o  | Untuk menyimpan hasil                                            |

---

## ▶️ Contoh Penggunaan
Gambar (contoh UI CLI):  
![Penggunaan](run.png)

--- 

## 📦 Dependency

Install library berikut sebelum menjalankan alat: **pip install httpx beautifulsoup4 urllib3**

Library bawaan Python (tidak perlu install):
- argparse  
- random  
- datetime  
- time  
- os  
- re  
- concurrent.futures  

---

## 🔐 Licensing

Repository ini menggunakan lisensi **Proprietary — All Rights Reserved**  
dengan tujuan menjaga agar alat penelitian tidak disalahgunakan oleh pihak tidak bertanggung jawab.

Anda **tidak diizinkan**:
- menyebarkan ulang,
- memodifikasi,
- menjual ulang alat ini
tanpa izin dari penulis.

---

## 💬 Kontak

Untuk kolaborasi penelitian, pelaporan bug, atau akses versi premium berkala:
**Telegram:** https://t.me/srwxrwxrwx

---

## 📝 Penutup

Repository ini dibuat sebagai dokumentasi kerentanan, analisis teknis, dan pengembangan alat pengujian.  
Gunakan secara etis dan profesional.  
