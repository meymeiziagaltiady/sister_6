import socket
import sys
import time

# Mendefinisikan kelas Client
class Klien(object):
    
    def __init__(self):
        # Inisialisasi klien dengan alamat dan nomor port default
        self.alamat = 'localhost'
        self.nomor_port = 8999
        # Membuat soket untuk koneksi TCP
        self.soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        

    # Metode untuk membuat koneksi dengan server, bertukar pesan, dan memutuskan koneksi
    def connect(self):
        # Terhubung ke server dengan alamat IP dan nomor port yang ditentukan
        self.soket.connect(('26.22.96.30', 8999))
        while True:
            # Membaca input pengguna dari konsol
            pilihan = input()
            # Mengirim input pengguna ke server
            self.soket.sendall(pilihan.encode('utf-8'))
            # Jika input adalah 'x', keluar dari program
            if pilihan == 'x':
                sys.exit()
            # Menerima balasan dari server
            balasan = self.soket.recv(1024).decode('utf-8')
            # Mencetak balasan dari server
            print(balasan)
        
        # Menutup koneksi soket (baris ini tidak akan tercapai dalam loop saat ini)
        self.soket.close()

# Fungsi untuk menampilkan pesan selamat datang dan opsi kepada pengguna
def pesan():
    print('Hello Horanghae Air Group!!!')
    print('Apa yang ingin Anda lakukan?')
    print('Buat: 1, Lihat: 2, Perbarui: 3, Hapus: 4, Cari: 5, Keluar: x')

# Fungsi utama
if __name__ == "__main__":
    # Menampilkan pesan awal dan opsi
    pesan()
    # Membuat objek Klien
    klien = Klien()
    # Menghubungkan klien ke server dan menangani komunikasi
    klien.connect()
