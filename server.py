import threading
import time
import datetime
import socket
import random
import json
import os
import pandas as pd
from route import Route
from decorators import decorator_create
import re

k1 = 'Apa yang ingin Anda lakukan?'
k2 = '1.Buat Route\n2.Lihat Semua Route\n3.Perbarui Route\n4.Hapus Route\n5.Cari Route\nx Keluar'
k3 = 'Rute tidak ada!!!'
k4 = 'Berikan nomor dari opsi!!!'

class Server(object):
    last_auto_code = 0

    @classmethod
    def generate_auto_code(cls):
        cls.last_auto_code += 1
        return cls.last_auto_code

    def __init__(self):
        self.ip = '26.97.66.68'
        self.port_number = 8999
        self.lock = threading.Lock()
        self.list = []
        self.load_existing_routes()

    def load_existing_routes(self):
        filename = 'route.json'
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            try:
                existing_data = pd.read_json(filename, orient='records')
                for _, row in existing_data.iterrows():
                    route = Route()
                    route.setcode(row['Kode Pesawat'])
                    route.setDeparture(row['Negara Keberangkatan'])
                    route.setTime(row['Waktu Penerbangan'])
                    route.setDestination(row['Negara Destinasi'])
                    route.setFlightDate(row['Tanggal Penerbangan'])
                    route.auto_code = int(row['Kode Penerbangan'][3:])  # Mengambil bagian numerik dari Kode Penerbangan
                    self.list.append(route)
                    Server.last_auto_code = max(Server.last_auto_code, route.auto_code)
            except Exception as e:
                print(f'Gagal memuat rute dari {filename}: {e}')

    def save_to_json(self, data, filename):
        try:
            # Membuat DataFrame dari data baru
            df = pd.DataFrame([data])

            # Memeriksa apakah file sudah ada atau belum
            if not os.path.exists(filename):
                # File belum ada, tulis DataFrame ke file JSON dengan indentasi
                df.to_json(filename, orient='records', indent=4)
            else:
                # File sudah ada, baca konten file dan gabungkan dengan data baru
                existing_data = pd.read_json(filename, orient='records') if os.path.getsize(filename) > 0 else pd.DataFrame([])
                new_data = pd.concat([existing_data, df], ignore_index=True)
                new_data.to_json(filename, orient='records', indent=4)

            print(f'Data berhasil disimpan ke {filename}!')
        except Exception as e:
            print(f'Gagal menyimpan data ke {filename}: {e}')

    def delete_from_json(self, code, filename):
        try:
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                existing_data = pd.read_json(filename, orient='records')
                new_data = existing_data[existing_data['Kode Penerbangan'] != code]
                new_data.to_json(filename, orient='records', indent=4)
                print(f'Data berhasil dihapus dari {filename}!')
            else:
                print(f'File {filename} tidak ditemukan atau kosong.')
        except Exception as e:
            print(f'Gagal menghapus data dari {filename}: {e}')

    @decorator_create
    def create(self, conn, *args):
        code = args[0]
        route = Route()
        route.setcode(args[0])
        route.setDeparture(args[1])
        route.setTime(args[2])
        route.setDestination(args[3])
        route.setFlightDate(args[4])
        
        # Mencari kode negara berdasarkan destinasi
        country_codes = {
            'Brunei Darussalam': 'BWN',
            'Kamboja': 'KHM',
            'Indonesia': 'IDN',
            'Lao PDR': 'LAO',
            'Malaysia': 'MYS',
            'Myanmar': 'MMR',
            'Filipina': 'PHL',
            'Singapura': 'SIN',
            'Thailand': 'THA',
            'Vietnam': 'VNM'
        }
        destination_country = args[3]
        if destination_country in country_codes:
            country_code = country_codes[destination_country]
        else:
            country_code = 'UNK'  # Jika negara tidak ditemukan, gunakan kode "UNK"

        # Menghasilkan kode auto-generate dengan basis kode negara dan kode terakhir
        new_code = f'{country_code}{Server.generate_auto_code():03d}'
        route.auto_code = new_code  # Set kode otomatis

        self.list.append(route)
        print(f"[{datetime.datetime.now()}] Client {args[5]} Membuat Rute Baru")

        try:
            data = {
                'timestamp': datetime.datetime.now().isoformat(),
                'client_id': args[5],
                'Kode Penerbangan': new_code,  # Menggunakan kode otomatis
                'Kode Pesawat': route.getCode(),
                'Negara Keberangkatan': route.getDeparture(),
                'Waktu Penerbangan': route.getTime(),
                'Negara Destinasi': route.getDestination(),
                'Tanggal Penerbangan': route.getFlightDate()
            }

            self.save_to_json(data, 'route.json')
            conn.sendall(f'Rute Berhasi dibuat dan data disimpan ke JSON file!\nKode Pesawat: {route.getCode()}\nKode Penerbangan: {new_code}\nNegara Keberangkatan: {route.getDeparture()}\nWaktu Penerbangan: {route.getTime()}\nNegara Destinasi: {route.getDestination()}\nTanggal Penerbangan: {route.getFlightDate()}\n\n{k1}\n{k2}'.encode('utf-8'))
        except Exception as e:
            conn.sendall(f'Gagal Menyimpan ke dalam File JSON! Tolong Coba Lagi.\n{k1}\n{k2}'.encode('utf-8'))
            print('Rute gagal tersimpan ke dalam file JSON:', e)

        self.lock.release()

    def search(self, conn, ip):
        try:
            conn.sendall('Masukkan kode penerbangan: '.encode('utf-8'))
            code = conn.recv(1024).decode('utf-8').strip()

            with self.lock:
                with open('route.json', 'r') as file:
                    routes = json.load(file)
                    found_route = None
                    for route in routes:
                        if route['Kode Penerbangan'] == code:
                            found_route = route
                            break

            random_number = random.randint(2, 4)
            print("[{}] Client {} Mencari Rute".format(datetime.datetime.now(), ip))

            if found_route:
                response = f"Found successfully:\n"
                response += f"Kode Penerbangan: {found_route['Kode Penerbangan']}\n"
                response += f"Kode Pesawat: {found_route['Kode Pesawat']}\n"
                response += f"Negara Keberangkatan: {found_route['Negara Keberangkatan']}\n"
                response += f"Waktu Penerbangan: {found_route['Waktu Penerbangan']}\n"
                response += f"Negara Destinasi: {found_route['Negara Destinasi']}\n"
                response += f"Tanggal Penerbangan: {found_route['Tanggal Penerbangan']}\n"
                response += f"\n{k1}\n{k2}"
                conn.sendall(response.encode('utf-8'))
            else:
                conn.sendall(f"{k3}\n{k1}\n{k2}".encode('utf-8'))

        except Exception as e:
            print(f'Gagal mencari data dari file JSON: {e}')
            conn.sendall(f'Gagal mencari data dari file JSON: {e}\n{k1}\n{k2}'.encode('utf-8'))

    def delete(self, conn, ip):
        try:
            conn.sendall('Masukkan kode penerbangan yang ingin dihapus: '.encode('utf-8'))
            code = conn.recv(1024).decode('utf-8').strip()

            with self.lock:
                # Baca rute dari file JSON
                with open('route.json', 'r') as file:
                    routes = json.load(file)
                    new_routes = [route for route in routes if route['Kode Penerbangan'] != code]

                # Periksa apakah ada perubahan pada daftar rute
                if len(new_routes) < len(routes):
                    # Tulis kembali rute yang tersisa ke file JSON
                    with open('route.json', 'w') as file:
                        json.dump(new_routes, file, indent=4)
                    conn.sendall(f'Rute dengan Kode Penerbangan {code} berhasil dihapus.\n{k1}\n{k2}'.encode('utf-8'))
                    print(f"[{datetime.datetime.now()}] Client {ip} Menghapus Rute dengan Kode Penerbangan {code}")
                else:
                    conn.sendall(f'Rute dengan Kode Penerbangan {code} tidak ditemukan.\n{k1}\n{k2}'.encode('utf-8'))
                    print(f"[{datetime.datetime.now()}] Client {ip} Gagal Menghapus Rute dengan Kode Penerbangan {code}")

        except Exception as e:
            print(f'Gagal menghapus data dari file JSON: {e}')
            conn.sendall(f'Gagal menghapus data dari file JSON: {e}\n{k1}\n{k2}'.encode('utf-8'))

    def update(self, conn, ip):
        asean_countries = [
            "Brunei Darussalam",
            "Kamboja",
            "Indonesia",
            "Lao PDR",
            "Malaysia",
            "Myanmar",
            "Filipina",
            "Singapura",
            "Thailand",
            "Vietnam",
        ]

        try:

            conn.sendall(
                "Masukkan kode penerbangan yang ingin diperbarui: ".encode("utf-8")
            )
            code = conn.recv(1024).decode("utf-8").strip()

            with self.lock:
                # Baca rute dari file JSON
                with open("route.json", "r") as file:
                    routes = json.load(file)
                    found_route = None
                    for route in routes:
                        if route["Kode Penerbangan"] == code:
                            found_route = route
                            break

            if not found_route:
                conn.sendall(f"{k3}\n{k1}\n{k2}".encode("utf-8"))
                return

            response = f"\nFound route:\n"
            response += f"Kode Penerbangan: {found_route['Kode Penerbangan']} (tidak bisa diubah)\n"
            response += f"Kode Pesawat: {found_route['Kode Pesawat']}\n"
            response += f"Negara Keberangkatan: {found_route['Negara Keberangkatan']}\n"
            response += f"Waktu Penerbangan: {found_route['Waktu Penerbangan']}\n"
            response += f"Negara Destinasi: {found_route['Negara Destinasi']} (tidak bisa diubah)\n"
            response += f"Tanggal Penerbangan: {found_route['Tanggal Penerbangan']}\n"
            response += f"\nApa yang ingin diperbarui?\n1. Kode Pesawat\n2. Negara Keberangkatan\n3. Waktu Penerbangan\n4. Tanggal Penerbangan"
            conn.sendall(response.encode("utf-8"))
            option = conn.recv(1024).decode("utf-8").strip()

            # update kode pesawat
            if option == "1":
                conn.sendall("Masukkan Kode Pesawat baru (Contoh: ID-01): ".encode("utf-8"))
                kode_pesawat = conn.recv(1024).decode("utf-8").strip()
                kode_pattern = re.compile(r"^[A-Z]{2}-\d{2}$")
                while not kode_pattern.match(kode_pesawat):
                    conn.sendall(                    "Format kode penerbangan tidak valid. Silakan masukkan kode dalam format seperti ID-01.\n"
                        "Masukkan Kode Pesawat baru (Contoh: ID-01): ".encode("utf-8"))  # Kirim pesan ke klien
                    kode_pesawat = conn.recv(1204).decode("utf-8")  # Terima pesan dari klien

                found_route["Kode Pesawat"] = kode_pesawat

            # update negara keberangkatan
            elif option == "2":
                destination = found_route["Negara Destinasi"]
                countries_message = "List negara SEA:\n"
                departure_option = [country for country in asean_countries if country != destination]
                for index, country in enumerate(departure_option, start=1):
                    countries_message += f"{index}. {country}\n"

                countries_message += "Masukkan Negara Keberangkatan baru:"

                conn.sendall(countries_message.encode("utf-8"))  # Kirim pesan ke klien
                choice_dep = int(conn.recv(1204).decode("utf-8"))  # Terima pesan dari klien

                while True:
                    if 1 <= choice_dep <= len(asean_countries):
                        departure = asean_countries[choice_dep - 1]
                        break
                    else:
                        conn.sendall("Pilihan keberangkatan tidak valid. Silakan pilih lagi.\n".encode("utf-8"))  # Kirim pesan ke klien
                        choice_dep = int(conn.recv(1204).decode("utf-8"))  # Terima pesan dari klien

                found_route["Negara Keberangkatan"] = departure

            # update waktu keberangkatan
            elif option == "3":
                conn.sendall("Masukkan Waktu Penerbangan baru (HH:MM): ".encode("utf-8"))
                waktu_keberangkatan = conn.recv(1024).decode("utf-8").strip()
                time_pattern = re.compile(r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
                # validasi format waktu
                while not time_pattern.match(waktu_keberangkatan):
                    conn.sendall("Format waktu tidak valid. Harap masukkan waktu dalam format HH:MM.\n"
                        "Masukkan Waktu Penerbangan baru (HH:MM): ".encode("utf-8"))  # Kirim pesan ke klien
                    waktu_keberangkatan = conn.recv(1204).decode("utf-8")  # Terima pesan dari klien

                found_route["Waktu Penerbangan"] = waktu_keberangkatan

            # update tanggal keberangkatan
            elif option == "4":
                conn.sendall("Masukkan Tanggal Penerbangan baru (YYYY-MM-DD): ".encode("utf-8"))
                jadwal_penerbangan = conn.recv(1024).decode("utf-8").strip()

                # Validasi format tanggal ISO untuk jadwal penerbangan
                iso_date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
                while not iso_date_pattern.match(jadwal_penerbangan):
                    conn.sendall("Format tanggal penerbangan tidak valid. Harap masukkan tanggal dalam format YYYY-MM-DD.\n"
                        "Masukkan Tanggal Penerbangan baru (YYYY-MM-DD): ".encode("utf-8"))  # Kirim pesan ke klien
                    jadwal_penerbangan = conn.recv(1204).decode("utf-8")  # Terima pesan dari klien

                # Validasi tanggal penerbangan lebih besar dari tanggal sistem
                today_date = datetime.date.today()
                flight_date = datetime.datetime.strptime(jadwal_penerbangan, "%Y-%m-%d").date()
                while flight_date <= today_date:
                    conn.sendall(
                        "Tanggal penerbangan tidak valid. Tanggal penerbangan harus lebih besar dari tanggal hari ini.\n"
                        "Masukkan Tanggal Penerbangan baru (YYYY-MM-DD): ".encode("utf-8")
                    )  # Kirim pesan ke klien
                    jadwal_penerbangan = conn.recv(1204).decode("utf-8")  # Terima pesan dari klien
                    flight_date = datetime.datetime.strptime(jadwal_penerbangan, "%Y-%m-%d").date()

                found_route["Tanggal Penerbangan"] = jadwal_penerbangan
            else:
                conn.sendall(f"{k4}\n{k1}\n{k2}".encode("utf-8"))
                return

            with self.lock:
                # Update file JSON
                for idx, route in enumerate(routes):
                    if route["Kode Penerbangan"] == code:
                        routes[idx] = found_route
                        break
                with open("route.json", "w") as file:
                    json.dump(routes, file, indent=4)

            conn.sendall(f"Rute dengan Kode Penerbangan {code} berhasil diperbarui!\n{k1}\n{k2}".encode("utf-8"))
            print(f"[{datetime.datetime.now()}] Client {ip} Memperbarui Rute dengan Kode Penerbangan {code}")

        except Exception as e:
            print(f"Gagal memperbarui data : {e}")
            conn.sendall(f"Gagal memperbarui data dalam file JSON: {e}\n{k1}\n{k2}".encode("utf-8"))

    def read_all(self, conn, ip):
        try:
            with open('route.json', 'r') as file:
                routes = json.load(file)
                if routes:
                    response = "Daftar Rute:\n"
                    for route in routes:
                        response += f"\nKode Penerbangan: {route['Kode Penerbangan']}\n"
                        response += f"Kode Pesawat: {route['Kode Pesawat']}\n"
                        response += f"Negara Keberangkatan: {route['Negara Keberangkatan']}\n"
                        response += f"Waktu Penerbangan: {route['Waktu Penerbangan']}\n"
                        response += f"Negara Destinasi: {route['Negara Destinasi']}\n"
                        response += f"Tanggal Penerbangan: {route['Tanggal Penerbangan']}\n"
                    response += f"\n{k1}\n{k2}"
                    conn.sendall(response.encode('utf-8'))
                else:
                    conn.sendall(f"{k3}\n{k1}\n{k2}".encode('utf-8'))
            print("[{}] Client {} Melihat Rute".format(datetime.datetime.now(), ip))
        except Exception as e:
            print(f'Gagal membaca data dari file JSON: {e}')

    def options(self, conn, ip):
        while True:       
            reply = conn.recv(1204).decode('utf-8')
            if reply == '2':
                self.read_all(conn, ip) 
            elif reply == '1':
                self.create(conn, None, None, None, None, None, ip)
            elif reply == '4':
                self.delete(conn, ip)
            elif reply == '3':
                self.update(conn, ip)
            elif reply == '5':
                self.search(conn, ip)
            else:
                conn.sendall('{}'.format(k4).encode('utf-8'))            
        conn.close()      

    def connect_to_client(self):
        conne_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conne_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        conne_socket.bind((self.ip, self.port_number))
        conne_socket.listen(5)

        print("Server is running...")

        while True:
            conn, ip = conne_socket.accept()
            print('[{}] client {} connect with your server'.format(datetime.datetime.now(), ip))
            threading.Thread(target=self.options, args=(conn, ip,)).start()
        conne_socket.close()

if __name__ == "__main__":
    server = Server()
    server.connect_to_client()
