# Daftar negara ASEAN
asean_countries = [
    'Brunei Darussalam',
    'Kamboja',
    'Indonesia',
    'Lao PDR',
    'Malaysia',
    'Myanmar',
    'Filipina',
    'Singapura',
    'Thailand',
    'Vietnam'
]

# Decorator untuk membaca input dari klien
def decorator_read(func):
    def inner(*args):
        args[0].lock.acquire()  # Kunci server
        args[2].sendall('Ketik kode: '.encode('utf-8'))  # Kirim pesan ke klien
        list_args  = list(args)
        list_args[1] = args[2].recv(1204).decode('utf-8')  # Terima pesan dari klien
        t = tuple(list_args)
        return func(*t)  # Panggil fungsi yang diberikan dan kembalikan hasilnya
    return inner

# Decorator untuk membuat rute baru
def decorator_create(func):
    def inner(*args):
        list_args = list(args)
        args[0].lock.acquire()  # Kunci server
        
        args[1].sendall('Input Kode Pesawat: '.encode('utf-8'))  # Kirim pesan ke klien
        kode_pesawat = args[1].recv(1204).decode('utf-8')  # Terima pesan dari klien
        list_args[2] = kode_pesawat

        # Tampilkan daftar negara ASEAN untuk pilihan keberangkatan
        args[1].sendall('Input Negara Keberangkatan:\n'.encode('utf-8'))  # Kirim pesan ke klien
        for index, country in enumerate(asean_countries, start=1):
            args[1].sendall(f"{index}. {country}\n".encode('utf-8'))  # Kirim pesan ke klien
        choice_dep = int(args[1].recv(1204).decode('utf-8'))  # Terima pesan dari klien

        if 1 <= choice_dep <= len(asean_countries):
            departure = asean_countries[choice_dep - 1]
            list_args[3] = departure
        else:
            list_args[3] = 'Keberangkatan Tidak Diketahui'
            args[1].sendall('Pilihan keberangkatan tidak valid. Silakan pilih lagi.\n'.encode('utf-8'))  # Kirim pesan ke klien
            return None

        args[1].sendall('Input Waktu Keberangkatan: '.encode('utf-8'))  # Kirim pesan ke klien
        waktu_keberangkatan = args[1].recv(1204).decode('utf-8')  # Terima pesan dari klien
        list_args[4] = waktu_keberangkatan

        # Tampilkan daftar negara ASEAN untuk pilihan destinasi (tidak termasuk keberangkatan)
        args[1].sendall('Input Negara Destinasi:\n'.encode('utf-8'))  # Kirim pesan ke klien
        destination_options = [country for country in asean_countries if country != departure]
        for index, country in enumerate(destination_options, start=1):
            args[1].sendall(f"{index}. {country}\n".encode('utf-8'))  # Kirim pesan ke klien

        while True:
            choice_dest = int(args[1].recv(1204).decode('utf-8'))  # Terima pesan dari klien
            if 1 <= choice_dest <= len(destination_options):
                destination = destination_options[choice_dest - 1]
                list_args[5] = destination
                break
            else:
                args[1].sendall('Pilihan destinasi tidak valid. Silakan pilih lagi.\n'.encode('utf-8'))  # Kirim pesan ke klien

        args[1].sendall('Input Jadwal Penerbangan: '.encode('utf-8'))  # Kirim pesan ke klien
        jadwal_penerbangan = args[1].recv(1204).decode('utf-8')  # Terima pesan dari klien
        list_args[6] = jadwal_penerbangan

        t = tuple(list_args)
        result = func(*t)  # Panggil fungsi yang diberikan

        return result

    return inner