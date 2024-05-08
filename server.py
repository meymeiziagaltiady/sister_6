import threading
import time 
import datetime
import socket
import random 
from route import Route
from decorators import decorator_create,decorator_read 

k1 = 'Apa yang ingin Anda lakukan?'
k2 = 'Buat: 1, Lihat: 2, Perbarui: 3, Hapus: 4, Keluar: 5'
k3 = 'Rute tidak ada!!!'
k4 = 'Berikan nomor dari opsi!!!'

 

class Server(object):
    
    def __init__(self):
        self.ip = 'localhost'
        self.port_number = 8999
        self.lock = threading.Lock()
        self.list = []

    # Membuat rute baru dan menyimpannya 
    @decorator_create
    def create(self, conn, *args):
        code = args[0]
        if any(route.getCode() == code for route in self.list):
            conn.sendall('Already exists!\n{}\n{}'.format(k1, k2).encode('utf-8'))
        else:
            route = Route()
            route.setcode(args[0])
            route.setDeparture(args[1])
            route.setTime(args[2])
            route.setDestination(args[3])
            route.setFlightDate(args[4])
            route.auto_code = Route.generate_auto_code()  # Menghasilkan kode otomatis
            self.list.append(route)
            random_number = random.randint(5, 10)
            time.sleep(random_number)
            print('Client {} waited to create the route for {} seconds'.format(args[5], random_number))
            #     # Kirim informasi rute baru ke klien1
            conn.sendall('Route created successfully!\nKode Pesawat: {}\nKode Penerbangan: {}\nDeparture: {}\nTime: {}\nDestination: {}\nFlight Date: {}\n{}\n{}'.format(
            route.getCode(), route.auto_code, route.getDeparture(), route.getTime(), route.getDestination(), route.getFlightDate(), k1, k2).encode('utf-8'))

        with open('file.txt', 'a') as file:
            file.write('[{}] Rute berhasil dibuat oleh client {}:\nKode Pesawat: {}\nKode Penerbangan: {}\nKeberangkatan: {}\nWaktu: {}\nTujuan: {}\nTanggal Penerbangan: {}\n\n'.format(
                datetime.datetime.now(), args[5], route.getCode(), route.auto_code, route.getDeparture(), route.getTime(), route.getDestination(), route.getFlightDate(), k1, k2))


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


