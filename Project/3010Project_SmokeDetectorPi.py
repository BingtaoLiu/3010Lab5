import random
import time
import httplib
import urllib
#import urllib.request
import requests
import json


# Emulated Object for MQ2 sensor

class MQ2:
    def __init__(self,readAPI,writeAPI):
        self.methane = 0
        self.CO2 = 0
        self.readAPI = readAPI
        self.writeAPI = writeAPI
        self.userID = '1'
        self.sensorID = '2'
    
    def establishConnection(self):
        self.writeTS(self.userID+','+self.sensorID+','+'TRUE')
        connectionEstablished = False
        while connectionEstablished == False:
            time.sleep(10)
            result = self.readTS()
            if result == self.userID+','+self.sensorID+','+'FALSE':
                print("Connection Established")
                connectionEstablished = True
            else:
                print("Connection Failed")
                connectionEstablished = False
    
    def readingString(self):
        self.CO2 = self.readCO2()
        self.methane = self.readMethane()
        return self.userID+","+self.sensorID+","+str(self.CO2)+","+str(self.methane)
    
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
    
    def readCO2(self):
        return random.random()*100
    
    def readMethane(self):
        return random.random()*100
    
if __name__ == '__main__':
    readAPI ='https://api.thingspeak.com/channels/1161317/fields/1.json?api_key=' + 'X3Q55V33X9YKOIYG' + '&results='
    writeAPI = "L4GUMEDFAO5XU6OZ"
    smokeDetectorPi = MQ2(readAPI,writeAPI)
    smokeDetectorPi.establishConnection()
    while True:
        time.sleep(10)
        smokeDetectorPi.writeTS(smokeDetectorPi.readingString())
        print(smokeDetectorPi.readTS())
        
