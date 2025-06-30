# DOSER-WIFI by ALRSSYD_



DOSER-WIFI adalah skrip Python sederhana yang dirancang untuk melakukan serangan UDP Flood ke gateway (router) dalam jaringan lokal. Alat ini dibuat untuk tujuan edukasi, yaitu untuk memahami konsep serangan Denial-of-Service (DoS) pada level jaringan dan untuk menguji ketahanan router Anda terhadap serangan banjir paket.

---

### ⚠️ PERINGATAN KERAS (DISCLAIMER)

**PENGGUNAAN ALAT INI ADALAH TANGGUNG JAWAB ANDA SEPENUHNYA.**

-   **GUNAKAN HANYA PADA JARINGAN ANDA SENDIRI** atau jaringan di mana Anda memiliki izin eksplisit untuk melakukan pengujian.
-   Menyerang jaringan publik atau milik orang lain tanpa izin adalah **tindakan ilegal** dan dapat dikenai sanksi hukum di banyak negara.
-   Pengembang tidak bertanggung jawab atas penyalahgunaan atau kerusakan yang disebabkan oleh skrip ini. Gunakan dengan bijak dan etis.

---

### ✨ Fitur

-   **Tampilan Profesional:** Banner pembuka yang keren dan output berwarna untuk kemudahan pembacaan.
-   **Multi-threading:** Mampu melancarkan serangan dari ratusan "pekerja" (thread) secara bersamaan untuk intensitas maksimal.
-   **Serangan ke Port Acak:** Secara otomatis mengirimkan paket ke port acak (1-65535) untuk membuat router lebih sulit menangani lalu lintas.
-   **Statistik Real-time:** Menampilkan jumlah total paket terkirim dan kecepatan serangan (Paket Per Detik / PPS) secara langsung.
-   **User-Friendly:** Interaktif, meminta input target dan tingkat serangan dari pengguna.
-   **Ringan:** Tidak memerlukan dependensi atau library eksternal, cukup Python standar.

---

### 📲 Instalasi & Penggunaan di Termux

Berikut adalah langkah-langkah untuk menginstal dan menjalankan skrip ini di Termux.

**1. Siapkan Termux dan install paket yang dibutuhkan (`git` dan `python`).**
Buka Termux dan jalankan perintah ini:
```bash
pkg update && pkg upgrade -y && pkg install git python -y
