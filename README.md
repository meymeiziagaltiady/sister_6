# Horanghae Air Group Flight Scheduling System

## Daftar Isi
- [Deskripsi](#deskripsi)
- [Prasyarat](#prasyarat)
- [Cara Menjalankan](#cara-menjalankan)
- [Struktur Folder Project](#struktur-folder-project)
- [Pengembang](#pengembang)
- [Alat dan Teknologi yang Digunakan](#alat-dan-teknologi-yang-digunakan)
- [URL Video Demo](#url-video-demo)

## Deskripsi
Proyek ini adalah sistem yang menangani penjadwalan penjadwalan penerbangan untuk maskapai Horanghae Air Group. Server akan menyimpan data jadwal penerbangan dalam file route.json. Klien dapat menambahkan, melihat, mengubah, mencari, dan menghapus data jadwal penerbangan. Interaksi klien dengan sistem dilakukan secara real-time sehingga pengelolaan informasi jadwal penerbangan menjadi lebih efektif dan efisien. Studi ini bertujuan untuk memahami implementasi sistem terdistribusi dalam konteks penjadwalan maskapai penerbangan yang memiliki kompleksitas tinggi.

## Prasyarat

1. Pastikan untuk mengklon repository ini ke dalam direktori lokal Anda dengan perintah:
    ```
    git clone https://github.com/meymeiziagaltiady/sister_6.git
    ```
   Ini akan mendownload salinan proyek ke komputer Anda.

2. Pastikan Anda menginstall Radmin VPN. Radmin VPN dapat diunduh dari situs resminya: [Radmin VPN Downloads](https://www.radmin-vpn.com/).

## Cara Menjalankan

1. Buat jaringan baru pada Radmin VPN dan minta anggota tim untuk bergabung menggunakan nama jaringan dan kata sandi yang telah dibuat. Lalu masukkan IP pada file 'client.py' dan 'server.py'.

2. Jalankan server dengan perintah: 
    ```
    python server.py
    ```

3. Jalankan client dengan perintah: 
    ```
    python client.py
    ```
   Ini akan menjalankan program kemudian Anda dapat menggunakan fungsionalitas yang terdapat pada sistem ini.

## Struktur Folder Project
Berikut struktur folder project setelah program dijalankan hingga step npm test:
```
├── client.py
├── decorators.py
├── README.md
├── route.json
├── route.py
└── server.py
    
```

## Pengembang
[<img src="https://github.com/deasalmaisnaini.png" width="50" style="border-radius:50%">](https://github.com/deasalmaisnaini)
[<img src="https://github.com/meymeiziagaltiady.png" width="50" style="border-radius:50%">](https://github.com/meymeiziagaltiady)
[<img src="https://github.com/erhaemael.png" width="50" style="border-radius:50%">](https://github.com/erhaemael)
[<img src="https://github.com/yasminazizahtuhfah.png" width="50" style="border-radius:50%">](https://github.com/yasminazizahtuhfah)


<b>Dea Salma Isnaini - 211524038 ([@deasalmaisnaini](https://github.com/deasalmaisnaini))
<br> Mey Meizia Galtiady - 211524047 ([@meymeiziagaltiady](https://github.com/meymeiziagaltiady))
<br> Rahma Alia Latifa - 211524047 ([@erhaemael](https://github.com/erhaemael))
<br> Yasmin Azizah Tuhfah - 211524064 ([@yasminazizahtuhfah](https://github.com/yasminazizahtuhfah))
<b>

# Alat dan Teknologi yang Digunakan

1. ![](https://img.shields.io/badge/Radmin_VPN-%23FFE57E)
   <br>Untuk mengkonfigurasi jaringan VPN.

2. ![](https://img.shields.io/badge/Python-%23FFE57E)
   <br>Untuk pengembangan aplikasi klien dan server.

3. ![](https://img.shields.io/badge/JSON-%23FFE57E)
   <br>Untuk penyimpanan data jadwal penerbangan dalam file route.json.