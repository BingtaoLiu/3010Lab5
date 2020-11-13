import random
import time
import httplib
import urllib
# import urllib.request
import requests
import json

URL1 = 'https://api.thingspeak.com/channels/1161338/fields/1.json?api_key=' + 'IFI077MYY53P4HR4' + '&results='
key1 = "P74NDBTW9HDK0JDU"
userID = "3"
sensorID = "4"
ss= ""

#TEST ID = 4
def establishConnection():
    #Read initial value
    temp = read_data_thingspeakRpiOne()
    connectionEstablished = "TRUE"

    while connectionEstablished == "TRUE":
        time.sleep(10)
        if temp == userID + "," + sensorID + "," + "TRUE":
            print("Connection Established")
            #this actually means connection established but we are writing False here so that
            #when the pi reads it, it knows the value was recieved and changed to false meaning a connection
            #was established
            connectionEstablished = "FALSE"
            write_data_thingspeakRpiOne(userID, sensorID, connectionEstablished)
        else:
            print("Connection Failed")
            connectionEstablished = "TRUE"

def write_data_thingspeakRpiOne(userID, sensorID, ss):

    # send data as one string separeted by ","
    rpi1_list = [userID, sensorID, ss]
    join_string1 = ",".join(rpi1_list)
    params = urllib.urlencode({'field1': join_string1, 'key': key1})
    headers = {"Content-typZZe": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print(join_string1)
        print(response.status, response.reason)
        data = response.read()
        conn.close()
    except:
        print("connection failed")

##TEST ID =5
def read_data_thingspeakRpiOne():
    data1 = requests.get(URL1).json()
    # feeds->last entry ->field1
    result1 = data1['feeds'][len(data1['feeds']) - 1]['field1']
    return result1



if __name__ == '__main__':
    #establishes connection with ThingSpeak
    establishConnection()
    #periodically reads from thingSpeak and displays it
    while True:
        time.sleep(10)
        readT = read_data_thingspeakRpiOne().split(",")
        for i in readT:
            print(i)

