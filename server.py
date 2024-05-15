import threading
import time
import datetime
import socket
import random
import json
import os
import pandas as pd
from route import Route
from decorators import decorator_create, decorator_read

k1 = 'Apa yang ingin Anda lakukan?'
k2 = 'Buat: 1, Lihat: 2, Perbarui: 3, Hapus: 4, Keluar: x'
k3 = 'Rute tidak ada!!!'
k4 = 'Berikan nomor dari opsi!!!'

class Server(object):
    last_auto_code = 0

    @classmethod
    def generate_auto_code(cls):
        cls.last_auto_code += 1
        return cls.last_auto_code

    def __init__(self):
        self.ip = 'localhost'
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
        print(f'Client {args[5]} Membuat Rute Baru')

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
            conn.sendall(f'Rute Berhasi dibuat dan data disimpan tke JSON file!\nKode Pesawat: {route.getCode()}\nKode Penerbangan: {new_code}\nNegara Keberangkatan: {route.getDeparture()}\nWaktu Penerbangan: {route.getTime()}\nNegara Destinasi: {route.getDestination()}\nTanggal Penerbangan: {route.getFlightDate()}\n{k1}\n{k2}'.encode('utf-8'))
        except Exception as e:
            conn.sendall(f'Gagal Menyimpan ke dalam File JSON! Tolong Coba Lagi.\n{k1}\n{k2}'.encode('utf-8'))
            print('Rute gagal tersimpan ke dalam file JSON:', e)

        self.lock.release()


    #Anazhti ama uparxei ena sugekrimeno Route kai to emfanizei
    @decorator_read
    def search(self,code,conn,ip):
     
     fly = self.search_list(code,1)
     random_number = random.randint(2,4)
     time.sleep(random_number)
    #  print('client {} waited to read the route {} seconds'.format(ip,random_number))
     print("[{}] client {} waited to read the route {} seconds".format(datetime.datetime.now(), ip, random_number))
     if fly is not None:
       conn.sendall('Found succesfully: {} {} {}\n{}\n{}'.format(fly.getCode(),fly.getState(),fly.getTime(),k1,k2).encode('utf-8'))
     else:
       conn.sendall('{}\n{}\n{}'.format(k3,k1,k2).encode('utf-8'))

     self.lock.release()
     

    #Diagrafei ena Route ama uparxei
    def delete_fly(self,conn,ip):

      self.lock.acquire()

      conn.sendall('dwse code: '.encode('utf-8'))          
      code = conn.recv(1204).decode('utf-8')
      fly = self.search_list(code,2)
      random_number = random.randint(5,10)
      time.sleep(random_number)
      # print('client {} waited to delete the route {} seconds'.format(ip,random_number))
      print('[{}] client {} waited to delete the route {} seconds'.format(datetime.datetime.now(), ip, random_number))
      if fly:
        conn.sendall('Route deleted succesfully!!!\n{}\n{}'.format(k1,k2).encode('utf-8'))         
      else:
        conn.sendall('{}\n{}\n{}'.format(k3,k1,k2).encode('utf-8'))

      self.lock.release()              


    #kanei update sugekrimeno Route
    def update(self,conn,ip):
        self.lock.acquire()

        conn.sendall('Type the code of the Route you want to update!!!'.encode('utf-8'))
        code = conn.recv(1204).decode('utf-8')
        fly, index = self.search_list(code,3)
        if fly is None:
         conn.sendall('{}'.format(k3).encode('utf-8'))
        else:

          conn.sendall('What do you want to update??\nCode: 1, State: 2, Time: 3'.encode('utf-8'))
          while True: 

            reply = conn.recv(1204).decode('utf-8')
            if reply.__eq__('1'):
                self.update_field(conn,fly,index,'code',ip)
                break
            elif reply.__eq__('2'):
              self.update_field(conn,fly,index,'state',ip)
              break
            elif reply.__eq__('3'):
              self.update_field(conn,fly,index,'time',ip)
              break
            else:
              conn.sendall('{}'.format(k4).encode('utf-8'))

        self.lock.release()    

    #apothikeuei Route sthn list
    def update_field(self,conn,fly,index,i,ip):
             conn.sendall('Give the new {}:'.format(i).encode('utf-8'))
             update = conn.recv(1204).decode('utf-8')
             if i == 'code':
               fly.setcode(update)
             elif i == 'state':
               fly.setstate(update)
             else:
               fly.setTime(update)
             self.list[index] = fly
             random_number = random.randint(5,10)      
             time.sleep(random_number)
            #  print('client {} waited to update the route {} seconds'.format(ip,random_number))
             print('[{}] client {} waited to update the route {} seconds'.format(datetime.datetime.now(), ip, random_number))
             conn.sendall('Updated sucesfully!!!\n{}\n{}'.format(k1,k2).encode('utf-8'))


    #anazhtei ama uparxei sugekrimeno route sthn lista
    def search_list(self,code,i):

       if i == 1: 
        for route in self.list:
            if route.getCode() == code:
                return route
        else:
             return None
       elif i == 2:
         for route in self.list:
            if route.getCode() == code:
                self.list.remove(route)
                return True
         else:
             return False
       else:   
            for index,route in enumerate(self.list):
              if route.getCode() == code:
                return route, index
            return None,-1 
              


    #Analogos me to ti thelei na kanei o client ektelei thn katallhlh methodo
    def options(self,conn,ip):
      
     while True:       
     
       reply = conn.recv(1204).decode('utf-8')
       
              
       if reply == '2':
          self.search(None,conn,ip) 
       elif reply == '1':
           
           self.create(conn,None,None,None,None, None, ip)
       elif reply == '4':
            self.delete_fly(conn,ip)
       elif reply == '3':
            self.update(conn,ip)
       elif reply == '5':
            # print('client {} close the connection!!!'.format(ip))
            print('[{}] client {} close the connection!!!'.format(datetime.datetime.now(), ip))
            break     
       else:
           conn.sendall('{}'.format(k4).encode('utf-8'))            
     conn.close()      

    #Dimiourgei sundesei me ton client kai dimiourgei to thread
    def connect_to_client(self):
        conne_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conne_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        conne_socket.bind((self.ip, self.port_number))
        conne_socket.listen(5)

        print("Server is running...")

        while True:
          conn, ip = conne_socket.accept()
          print('[{}] client {} connect with your server'.format(datetime.datetime.now(), ip))
          threading.Thread(target=self.options,args=(conn,ip,)).start()
        conne_socket.close()

             
       
if __name__  == "__main__":
    server = Server()
    server.connect_to_client()