import socket
import sys
import time

class Client(object):
    
    def __init__(self):
        self.address = 'localhost'
        self.port_number = 8999
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        

    #Dhmiourgei sundesei me ton server, antalasei mhnumata kai telos aposundeaite
    def connect(self):
      self.socket.connect(('26.97.66.68',8999))
      while True:
        
         option = input()
         self.socket.sendall(option.encode('utf-8'))
         if option == 'x':
             sys.exit()
         reply = self.socket.recv(1204).decode('utf-8')
         print(reply)
        
        
      self.socket.close()



def message():
    print('Hello Horanghae Air Group!!!')
    print('Apa yang ingin Anda lakukan?')
    print('1.Buat Route\n2.Lihat Semua Route\n3.Perbarui Route\n4.Hapus Route\n5.Cari Route\nx Keluar')

if __name__ == "__main__":
    message()
    client = Client()
    client.connect()
