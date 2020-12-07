from sense_hat import SenseHat 
import random
import time
import httplib
import urllib
import requests
import json
import sys

sense = SenseHat()

class FridgePi:
    def __init__(self,readAPI,writeAPI):
        self.temp = 0
        self.humidity = 0
        self.readAPI = readAPI
        self.writeAPI = writeAPI
        self.userID = '10'
        self.sensorID = '1'
    
    def establishConnection(self):
        self.writeTS(self.userID+','+self.sensorID+','+'FALSE')
        connectionEstablished = False
        while connectionEstablished == False:
            time.sleep(10)
            result = self.readTS()
            if result == self.userID+','+self.sensorID+','+'TRUE':
                print("Connection Established")
                connectionEstablished = True
            else:
                print("Connection Failed")
                connectionEstablished = False
    
    def readingString(self):
        self.temp = self.readtemp()
        self.humidity = self.readhumidity()
        return self.userID+","+self.sensorID+","+str(self.temp)+","+str(self.humidity)
    
    def writeTS(self,fieldString):
        params = urllib.urlencode({'field1': fieldString, 'key':self.writeAPI }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print(fieldString)
            print(response.status, response.reason)
            data = response.read()
            conn.close()
        except:
            print("connection failed")
        
    def readTS(self):
        data = requests.get(self.readAPI).json()
        #feeds->last entry ->field1
        result = data['feeds'][len(data['feeds'])-1]['field1']
        return result
    
    def readtemp(self):
	temp_c = sense.get_temperature() # Read the sensors
	temp_f = temp_c * 9.0 / 5.0 + 32.0
  	temp_f = float("{0:.2f}".format(temp_f)) # Format the data
        return str(temp_f)
    
    def readhumidity(self):
	# Read the sensors
        humidity = sense.get_humidity() 
	# Format the data
	humidity = float("{0:.2f}".format(humidity)) 
	return str(humidity)
    
if __name__ == '__main__':
    readAPI ='https://api.thingspeak.com/channels/1161317/fields/1.json?api_key=' + 'IFI077MYY53P4HR4' + '&results='
    writeAPI = "P74NDBTW9HDK0JDU"
    SenseHatPi = FridgePi(readAPI,writeAPI)
    SenseHatPi.establishConnection()
    while True:
        time.sleep(10)
        SenseHatPi.writeTS(SenseHatPi.readingString())
        print(SenseHatPi.readTS())
        
