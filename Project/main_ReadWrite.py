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
            co
