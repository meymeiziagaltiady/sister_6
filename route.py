class Route(object):

    # Variabel kelas untuk menyimpan kode terakhir yang digunakan
    last_code = 0

    # Inisialisasi objek Route
    def _init__(self, code, departure, time, destination, flightDate):
        self.code = None
        self.departure = None
        self.time = None
        self.destination = None
        self.flightDate = None
        self.auto_code = None

    # Metode statis untuk menghasilkan kode otomatis
    @staticmethod
    def generate_auto_code():
        # Menambah last_code dan mengembalikannya sebagai kode penerbangan baru
        Route.last_code += 1
        return Route.last_code

    # Metode untuk mengatur kode penerbangan
    def setcode(self, code):
        self.code = code

    # Metode untuk mengatur tempat keberangkatan
    def setDeparture(self, departure):
        self.departure = departure

    # Metode untuk mengatur waktu keberangkatan
    def setTime(self, time):
        self.time = time 

    # Metode untuk mengatur tujuan penerbangan
    def setDestination(self, destination):
        self.destination = destination

    # Metode untuk mengatur tanggal penerbangan
    def setFlightDate(self, flightDate):
        self.flightDate = flightDate

    # Metode untuk mendapatkan kode penerbangan
    def getCode(self):
        return self.code

    # Metode untuk mendapatkan waktu keberangkatan
    def getTime(self):
        return self.time  

    # Metode untuk mendapatkan tujuan penerbangan
    def getDestination(self):
        return self.destination

    # Metode untuk mendapatkan tempat keberangkatan
    def getDeparture(self):
        return self.departure

    # Metode untuk mendapatkan tanggal penerbangan
    def getFlightDate(self):
        return self.flightDate

    # Metode untuk menampilkan informasi penerbangan
    def shaw(self):
        print(self.code + self.departure + self.time + self.destination + self.flightDate + self.auto_code)

if __name__ == "__main__":
    pass
