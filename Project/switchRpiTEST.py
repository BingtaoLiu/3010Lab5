import time
import http.client
import urllib
import requests
import json

URL2 = 'https://api.thingspeak.com/channels/1160909/fields/1.json?api_key='+'34BOVG6Y72Q6EEVB'+'&results='
key2 = "O67GXT65S5U67H2Q"
userID = "20"
sensorID = "2"
ss= ""
#TEST ID = 4
def establishConnectionSwitchPi():
    #Read initial value
    temp = read_data_thingspeakRpiTwo()
    connectionEstablished = False

    while connectionEstablished == False:
        time.sleep(10)
        if temp == userID + "," + sensorID + "," + "FALSE":
            print("Connection Established")
            #connection was established and now we write back "TRUE"
            connectionEstablished = True
            write_data_thingspeakRpiTwo(userID, sensorID,"TRUE")
        else:
            print("Connection Failed")
            connectionEstablished = False

#TEST ID = 8
def write_data_thingspeakRpiTwo(userID, sensorID, ss):
    sStatus = ss
    if (sStatus == "TRUE"):
        # send data as one string separeted by ","
        rpi2_list = [userID, sensorID, sStatus]
        join_string2 = ",".join(rpi2_list)
        ss= "FALSE"
    else:
        rpi2_list = [userID, sensorID, sStatus]
        join_string2 = ",".join(rpi2_list)


    params = urllib.parse.urlencode({'field1': join_string2, 'key': key2})
    headers = {"Content-typZZe": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
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
    establishConnectionSwitchPi()
    #periodically reads from thingSpeak and displays it
    while True:
        time.sleep(10)
        #now we write to ThingSpeak by changing switchStatus
        write_data_thingspeakRpiTwo(userID, sensorID, "ON")
        #now we read from ThingSpeak to show we are able to check if value is same or different
        time.sleep(10)
        readT = read_data_thingspeakRpiTwo().split(",")
        #If value is ON we change it to OFF to test we can
        if readT[2] == "ON":
            write_data_thingspeakRpiTwo(userID, sensorID, "OFF")




