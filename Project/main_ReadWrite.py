import time
import http.client
import urllib
# import urllib.request
import requests
import main


URL = "https://api.thingspeak.com/channels/1214109/fields/1.json?api_key=" + "UN1NYDUT4E1QODWF" + "&results="
key = "K628RF2FUJY95ZRE"

ss = ""

def establishConnectionFridgePi():
    #Read initial value
    readData = []
    readData = read_data_thingspeakRpiOne()
    temp= readData[0].split(",")
    connectionEstablished = False
    compIDs= main2.comp_values(temp[0], temp[1])
    while connectionEstablished == False:
        time.sleep(10)
        if compIDs == True and temp[2] == "FALSE":
            print("Connection Established")
            #this actually means connection established but we are writing False here so that
            #when the pi reads it, it knows the value was recieved and changed to false meaning a connection
            #was established
            connectionEstablished = True
            write_data_thingspeakRpiOne(temp[0], temp[1], "TRUE")
        else:
            print("Connection Failed")
            connectionEstablished = False

def establishConnectionSwitchPi():
    #Read initial value
    readData =[]
    readData = read_data_thingspeakRpiTwo()
    temp = readData[0].split(",")
    connectionEstablished = False
    compIDs= main2.comp_values(temp[0], temp[1])

    while connectionEstablished == False:
        time.sleep(10)
        if compIDs == True and temp[2] == "FALSE":
            print("Connection Established")
            #this actually means connection established but we are writing False here so that
            #when the pi reads it, it knows the value was recieved and changed to false meaning a connection
            #was established
            connectionEstablished = True
            write_data_thingspeakRpiTwo(temp[0], temp[1], "TRUE")
        else:
            print("Connection Failed")
            connectionEstablished = False

def establishConnectionSmokePi():
    #Read initial value
    readData =[]
    readData = read_data_thingspeakRpiThree()
    temp = readData[0].split(",")
    connectionEstablished = False
    compIDs= main2.comp_values(temp[0], temp[1])

    while connectionEstablished == False:
        time.sleep(10)
        if compIDs == True and temp[2] ==  "FALSE":
            print("Connection Established")
            #this actually means connection established but we are writing False here so that
            #when the pi reads it, it knows the value was recieved and changed to false meaning a connection
            #was established
            connectionEstablished = True
            write_data_thingspeakRpiThree(temp[0], temp[1], "TRUE")
        else:
            print("Connection Failed")
            connectionEstablished = False



def write_data_thingspeakRpiOne(userID, sensorID, ss):

    # send data as one string separeted by ","
    rpi1_list = [userID, sensorID, ss]
    join_string1 = ",".join(rpi1_list)
    params = urllib.parse.urlencode({'field1': join_string1, 'key': key})
    headers = {"Content-typZZe": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
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
    data1 = requests.get(URL).json()
    # feeds->last entry ->field1
    result1 = data1['feeds'][len(data1['feeds']) - 1]['field1']
    entryID1 = data1['feeds'][len(data1['feeds']) - 1]['entry_id']
    return result1, entryID1


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

    params = urllib.parse.urlencode({'field2': join_string2, 'key': key})
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


def read_data_thingspeakRpiTwo():
    data2 = requests.get(URL).json()
    # feeds->last entry ->field1
    result2 = data2['feeds'][len(data2['feeds']) - 1]['field2']
    entryID2 = data2['feeds'][len(data2['feeds']) - 1]['entry_ID']
    return result2, entryID2


def write_data_thingspeakRpiThree(userID, sensorID, ss):

    # send data as one string separeted by ","
    rpi3_list = [userID, sensorID, ss]
    join_string3 = ",".join(rpi3_list)
    params = urllib.parse.urlencode({'field3': join_string3, 'key': key})
    headers = {"Content-typZZe": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print(join_string3)
        print(response.status, response.reason)
        data = response.read()
        conn.close()
    except:
        print("connection failed")


def read_data_thingspeakRpiThree():
    data3 = requests.get(URL).json()
    # feeds->last entry ->field1
    result3 = data3['feeds'][len(data3['feeds']) - 1]['field3']
    entryID3 = data3['feeds'][len(data3['feeds']) - 1]['entry_ID']

    return result3, entryID3





