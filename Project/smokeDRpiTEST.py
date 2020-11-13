import random
import time
import httplib
import urllib
# import urllib.request
import requests
import json

URL3 = 'https://api.thingspeak.com/channels/1161317/fields/1.json?api_key=' + 'X3Q55V33X9YKOIYG' + '&results='
key3 = "L4GUMEDFAO5XU6OZ"
userID = "1"
sensorID = "2"
ss= " "

#TEST ID = 4
def establishConnection():
    #Read initial value
    temp = read_data_thingspeakRpiThree()
    connectionEstablished = "TRUE"

    while connectionEstablished == "TRUE":
        time.sleep(10)
        if temp == userID + "," + sensorID + "," + "TRUE":
            print("Connection Established")
            #this actually means connection established but we are writing False here so that
            #when the pi reads it, it knows the value was recieved and changed to false meaning a connection
            #was established
            connectionEstablished = "FALSE"
            write_data_thingspeakRpiThree(userID, sensorID, connectionEstablished)
        else:
            print("Connection Failed")
            connectionEstablished = "TRUE"


def write_data_thingspeakRpiThree(userID, sensorID, ss):

    # send data as one string separeted by ","
    rpi3_list = [userID, sensorID, ss]
    join_string3 = ",".join(rpi3_list)
    params = urllib.urlencode({'field1': join_string3, 'key': key3})
    headers = {"Content-typZZe": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print(join_string3)
        print(response.status, response.reason)
        data = response.read()
        conn.close()
    except:
        print("connection failed")

#TEST ID = 6
def read_data_thingspeakRpiThree():
    data3 = requests.get(URL3).json()
    # feeds->last entry ->field1
    result3 = data3['feeds'][len(data3['feeds']) - 1]['field1']
    return result3



if __name__ == '__main__':
    #establishes connection with ThingSpeak
    establishConnection()
    #periodically reads from thingSpeak and displays it
    while True:
        time.sleep(10)
        readT = read_data_thingspeakRpiThree().split(",")
        for i in readT:
            print(i)

