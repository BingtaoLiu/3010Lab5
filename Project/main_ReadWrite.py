import time
import http.client
import urllib
# import urllib.request
import requests
import main2


URL1 = 'https://api.thingspeak.com/channels/1161338/fields/1.json?api_key=' + 'IFI077MYY53P4HR4' + '&results='
key1 = "P74NDBTW9HDK0JDU"
URL2 = 'https://api.thingspeak.com/channels/1160909/fields/1.json?api_key='+'34BOVG6Y72Q6EEVB'+'&results='
key2 = "O67GXT65S5U67H2Q"
URL3 = 'https://api.thingspeak.com/channels/1161317/fields/1.json?api_key=' + 'X3Q55V33X9YKOIYG' + '&results='
key3 = "L4GUMEDFAO5XU6OZ"

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
    print(temp[0], temp[1], temp[2])
    connectionEstablished = False
    compIDs= main2.comp_values(temp[0], temp[1])
    print(compIDs)

    while connectionEstablished == False:
        time.sleep(10)
        if compIDs == True and temp[2] == "TRUE":
            print("Connection Established")
            #this actually means connection established but we are writing False here so that
            #when the pi reads it, it knows the value was recieved and changed to false meaning a connection
            #was established
            connectionEstablished = True
            write_data_thingspeakRpiTwo(temp[0], temp[1], "OFF")
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
    params = urllib.parse.urlencode({'field1': join_string1, 'key': key1})
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
    data1 = requests.get(URL1).json()
    # feeds->last entry ->field1
    result1 = data1['feeds'][len(data1['feeds']) - 1]['field1']
    entryID1 = data1['feeds'][len(data1['feeds']) - 1]['entry_id']
    return result1, entryID1


def write_data_thingspeakRpiTwo(userID, sensorID, ss):

    sStatus = ss
    print(sStatus)
    #params = urllib.parse.urlencode({'field1': sStatus, 'field2': userID, 'field3': sensorID, 'key': key2})
    rpi2_list = [userID, sensorID, sStatus]
    join_string2 = ",".join(rpi2_list)
    params = urllib.parse.urlencode({'field1': join_string2, 'key': key2})
    headers = {"Content-typZZe": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        conn.close()
    except:
        print("connection failed")


def read_data_thingspeakRpiTwo():
    data2 = requests.get(URL2).json()
    # feeds->last entry ->field1
    result2 = data2['feeds'][len(data2['feeds']) - 1]['field1']
    entryID2 = data2['feeds'][len(data2['feeds']) - 1]['entry_id']
    #print(str(data2['feeds'][len(data2['feeds']) - 1]))
    return result2, entryID2


def write_data_thingspeakRpiThree(userID, sensorID, ss):

    # send data as one string separeted by ","
    rpi3_list = [userID, sensorID, ss]
    join_string3 = ",".join(rpi3_list)
    params = urllib.parse.urlencode({'field1': join_string3, 'key': key3})
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
    data3 = requests.get(URL3).json()
    # feeds->last entry ->field1
    result3 = data3['feeds'][len(data3['feeds']) - 1]['field1']
    entryID3 = data3['feeds'][len(data3['feeds']) - 1]['entry_id']

    return result3, entryID3







