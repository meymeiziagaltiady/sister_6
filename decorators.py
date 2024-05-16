import re
import datetime

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

        args[1].sendall('Input Kode Pesawat (Contoh: ID-01): '.encode('utf-8'))  # Kirim pesan ke klien
        kode_pesawat = args[1].recv(1204).decode('utf-8')  # Terima pesan dari klien

        # Validasi format kode pesawat (dua huruf dan angka)
        kode_pattern = re.compile(r'^[A-Z]{2}-\d{2}$')
        while not kode_pattern.match(kode_pesawat):
            args[1].sendall('Format kode penerbangan tidak valid. Silakan masukkan kode dalam format seperti ID-01.\n'
                            'Input Kode Pesawat (Contoh: ID-01): '.encode('utf-8'))  # Kirim pesan ke klien
            kode_pesawat = args[1].recv(1204).decode('utf-8')  # Terima pesan dari klien

        list_args[2] = kode_pesawat
        countries_message = ""
        for index, country in enumerate(asean_countries, start=1):
            countries_message += f"{index}. {country}\n"

        countries_message += "Input Negara Keberangkatan:"

        args[1].sendall(countries_message.encode('utf-8'))  # Kirim pesan ke klien
        choice_dep = int(args[1].recv(1204).decode('utf-8'))  # Terima pesan dari klien

        while True:
            if 1 <= choice_dep <= len(asean_countries):
                departure = asean_countries[choice_dep - 1]
                list_args[3] = departure
                break
            else:
                args[1].sendall('Pilihan keberangkatan tidak valid. Silakan pilih lagi.\n'.encode('utf-8'))  # Kirim pesan ke klien
                choice_dep = int(args[1].recv(1204).decode('utf-8'))  # Terima pesan dari klien
        
        args[1].sendall('Input Waktu Keberangkatan (HH:MM): '.encode('utf-8'))  # Kirim pesan ke klien
        waktu_keberangkatan = args[1].recv(1204).decode('utf-8')  # Terima pesan dari klien

        # Validasi format jam
        time_pattern = re.compile(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
        while not time_pattern.match(waktu_keberangkatan):
            args[1].sendall('Format waktu tidak valid. Harap masukkan waktu dalam format HH:MM.\n'
                            'Input Waktu Keberangkatan (HH:MM): '.encode('utf-8'))  # Kirim pesan ke klien
            waktu_keberangkatan = args[1].recv(1204).decode('utf-8')  # Terima pesan dari klien

        list_args[4] = waktu_keberangkatan

        destination_message = ""
        destination_options = [country for country in asean_countries if country != departure]
        for index, country in enumerate(destination_options, start=1):
            destination_message += f"{index}. {country}\n"
        destination_message += "Input Negara Destinasi:"

        args[1].sendall(destination_message.encode('utf-8'))  # Kirim pesan ke klien
        choice_dest = int(args[1].recv(1204).decode('utf-8'))  # Terima pesan dari klien

        while True:
            if 1 <= choice_dest <= len(destination_options):
                destination = destination_options[choice_dest - 1]
                list_args[5] = destination
                break
            else:
                args[1].sendall('Pilihan destinasi tidak valid. Silakan pilih lagi.\n'.encode('utf-8'))  # Kirim pesan ke klien
                choice_dest = int(args[1].recv(1204).decode('utf-8')) 


        args[1].sendall('Input Jadwal Penerbangan (YYYY-MM-DD): '.encode('utf-8'))  # Kirim pesan ke klien
        jadwal_penerbangan = args[1].recv(1204).decode('utf-8')  # Terima pesan dari klien

        # Validasi format tanggal ISO untuk jadwal penerbangan
        iso_date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        while not iso_date_pattern.match(jadwal_penerbangan):
            args[1].sendall('Format tanggal penerbangan tidak valid. Harap masukkan tanggal dalam format YYYY-MM-DD.\n'
                            'Input Jadwal Penerbangan (YYYY-MM-DD): '.encode('utf-8'))  # Kirim pesan ke klien
            jadwal_penerbangan = args[1].recv(1204).decode('utf-8')  # Terima pesan dari klien

        # Validasi tanggal penerbangan lebih besar dari tanggal sistem
        today_date = datetime.date.today()
        flight_date = datetime.datetime.strptime(jadwal_penerbangan, '%Y-%m-%d').date()
        while flight_date <= today_date:
            args[1].sendall('Tanggal penerbangan tidak valid. Tanggal penerbangan harus lebih besar dari tanggal hari ini.\n'
                            'Input Jadwal Penerbangan (YYYY-MM-DD): '.encode('utf-8'))  # Kirim pesan ke klien
            jadwal_penerbangan = args[1].recv(1204).decode('utf-8')  # Terima pesan dari klien
            flight_date = datetime.datetime.strptime(jadwal_penerbangan, '%Y-%m-%d').date()

        list_args[6] = jadwal_penerbangan

        t = tuple(list_args)
        result = func(*t)  # Panggil fungsi yang diberikan

        return result

    return inner
