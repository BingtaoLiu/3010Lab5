import random
import time
import httplib
import urllib
# import urllib.request
import requests
import json

URL1 = 'https://api.thingspeak.com/channels/1161338/fields/1.json?api_key=' + 'IFI077MYY53P4HR4' + '&results='
key1 = "P74NDBTW9HDK0JDU"
userID = "10"
sensorID = "1"
ss= ""


def establishConnectionFridgePi():
    #Read initial value
    temp = read_data_thingspeakRpiOne()
    connectionEstablished = False

    while connectionEstablished == False:
        time.sleep(10)
        if temp == userID + "," + sensorID + "," + "FALSE":
            print("Connection Established")
            #connection established and now we write back "TRUE"
            connectionEstablished = True
            write_data_thingspeakRpiOne(userID, sensorID, "TRUE")
        else:
            print("Connection Failed")
            connectionEstablished = False

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

def read_data_thingspeakRpiOne():
    data1 = requests.get(URL1).json()
    # feeds->last entry ->field1
    result1 = data1['feeds'][len(data1['feeds']) - 1]['field1']
    return result1

