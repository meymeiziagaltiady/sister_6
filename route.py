class Route(object):

  last_code = 0

  def _init__(self,code,departure,time, destination, flightDate):
      self.code = None
      self.departure = None
      self.time = None
      self.destination = None
      self.flightDate = None
      self.auto_code = None

  @staticmethod
  def generate_auto_code():
      # Increment the last_code and return it as the new flight code
      Route.last_code += 1
      return Route.last_code

  def setcode(self,code):
    self.code = code

  def setDeparture(self,departure):
    self.departure = departure

  def setTime(self,time):
    self.time = time 
  
  def setDestination(self,destination):
    self.destination = destination

  def setFlightDate(self,flightDate):
    self.flightDate = flightDate

  def getCode(self):
    return self.code   


  def getTime(self):
    return self.time  
  
  def getDestination(self):
    return self.destination
  
  def getDeparture(self):
    return self.departure
  
  def getFlightDate(self):
    return self.flightDate

  def shaw(self):
    print(self.code + self.departure + self.time + self.destination + self.flightDate + self.auto_code)

  
if __name__ == "__main__":
    pass


