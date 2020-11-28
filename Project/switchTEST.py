import random
import time
import http.client
import urllib
import urllib.request
import requests
import json

# Switch pi

class SStatus:
    def __init__(self, readAPI, writeAPI):
        self.switchS = "OFF"
        self.readAPI = readAPI
        self.writeAPI = writeAPI
        self.userID = '20'
        self.sensorID = '2'

    def establishConnection(self):
        self.writeTS(self.userID + ',' + self.sensorID + ',' + 'TRUE')
        connectionEstablished = False
        while connectionEstablished == False:
            time.sleep(10)
            result = self.readTS()
            if result == self.userID + ',' + self.sensorID + ',' + 'TRUE':
                print("Connection Established")
                connectionEstablished = True
            else:
                print("Connection Failed")
                connectionEstablished = False


    def writeTS(self, fieldString):
        params = urllib.parse.urlencode({'field1': fieldString, 'key': self.writeAPI})
        headers = {"Content-typZZe": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = http.client.HTTPConnection("api.thingspeak.com:80")
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
        # feeds->last entry ->field1
        result = data['feeds'][len(data['feeds']) - 1]['field1']
        return result


if __name__ == '__main__':
    readAPI = 'https://api.thingspeak.com/channels/1160909/fields/1.json?api_key=' + '34BOVG6Y72Q6EEVB' + '&results='
    writeAPI = "O67GXT65S5U67H2Q"
    switchPi = SStatus(readAPI, writeAPI)
    switchPi.establishConnection()
    print(result)
    while True:
        time.sleep(10)
        print(switchPi.readTS())

