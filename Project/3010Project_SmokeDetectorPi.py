import random
import time
import httplib
import urllib
#import urllib.request
import requests
import json
import serial

class MQ2:
    def __init__(self,readAPI,writeAPI):
        self.established = False
        self.methane = 0
        self.CO2 = 0
        self.readAPI = readAPI
        self.writeAPI = writeAPI
        self.userID = '30'
        self.sensorID = '3'
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.ser.flush()
    
    def establishConnection(self):
        self.writeTS(self.userID+','+self.sensorID+','+'FALSE')
        time.sleep(5)
        while self.established == False:
            result = self.readTS()
            if result == self.userID+','+self.sensorID+','+'TRUE':
                print("Connection Established")
                self.established = True
            else:
                print("Connection Failed")
            time.sleep(2)
    
    def writeTS(self,fieldString):
        params = urllib.urlencode({'field1': fieldString, 'key':self.writeAPI }) 
        #print(params)
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
    
    def readSensor(self):
        while True:
            if self.ser.in_waiting > 0:
                reading = self.ser.readline().decode('utf-8').rstrip()
                return self.userID+","+self.sensorID+","+reading

    
if __name__ == '__main__':
    readAPI ='https://api.thingspeak.com/channels/1161317/fields/1.json?api_key=' + 'X3Q55V33X9YKOIYG' + '&results='
    writeAPI = "L4GUMEDFAO5XU6OZ"
    smokeDetectorPi = MQ2(readAPI,writeAPI)
    smokeDetectorPi.establishConnection()
    while True:
        smokeDetectorPi.writeTS(smokeDetectorPi.readSensor())
        time.sleep(5)

        