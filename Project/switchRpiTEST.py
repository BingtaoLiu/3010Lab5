import time
import httplib
import urllib
import requests
import json

URL2 = 'https://api.thingspeak.com/channels/1160909/fields/1.json?api_key='+'34BOVG6Y72Q6EEVB'+'&results='
key2 = "O67GXT65S5U67H2Q"
userID = "5"
sensorID = "6"
ss= ""
#TEST ID = 4
def establishConnection():
    #Read initial value
    temp = read_data_thingspeakRpiTwo()
    connectionEstablished = "TRUE"

    while connectionEstablished == "TRUE":
        time.sleep(10)
        if temp == userID + "," + sensorID + "," + "TRUE":
            print("Connection Established")
            #this actually means connection established but we are writing False here so that
            #when the pi reads it, it knows the value was recieved and changed to false meaning a connection
            #was established
            connectionEstablished = "TRUE"
            write_data_thingspeakRpiTwo(userID, sensorID, connectionEstablished)
        else:
            print("Connection Failed")
            connectionEstablished = "FALSE"

#TEST ID = 8
def write_data_thingspeakRpiTwo(userID, sensorID, ss):
    sStatus = ss
    if (sStatus == "FALSE"):
        # send data as one string separeted by ","
        rpi2_list = [userID, sensorID, sStatus]
        join_string2 = ",".join(rpi2_list)
        ss= "TRUE"
    else:
        rpi2_list = [userID, sensorID, sStatus]
        join_string2 = ",".join(rpi2_list)


    params = urllib.urlencode({'field1': join_string2, 'key': key2})
    headers = {"Content-typZZe": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print(join_string2)
        print(response.status, response.reason)
        data = response.read()
        conn.close()
    except:
        print("connection failed")

#TEST ID = 7
def read_data_thingspeakRpiTwo():
    data2 = requests.get(URL2).json()
    # feeds->last entry ->field1
    result2 = data2['feeds'][len(data2['feeds']) - 1]['field1']
    print(result2)
    return result2



if __name__ == '__main__':
    #establishes connection with ThingSpeak
    establishConnection()
    #periodically reads from thingSpeak and displays it
    while True:
        time.sleep(10)
        #now we write to ThingSpeak by changing switchStatus
        write_data_thingspeakRpiTwo(userID, sensorID, "ON")
        #now we read from ThingSpeak to show we are able to check if value is same or different
        time.sleep(3)
        readT = read_data_thingspeakRpiTwo().split(",")
        #If value is ON we change it to OFF to test we can
        if readT[2] == "ON":
            write_data_thingspeakRpiTwo(userID, sensorID, "OFF")




