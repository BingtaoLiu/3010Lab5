import RPi.GPIO as GPIO
import urllib, urllib.request, json, http.client, time
# import requests
import switchTEST
from switchTEST import *
from switchTEST import SStatus

def init_pins():
    # set the pins numbering mode
    GPIO.setmode(GPIO.BOARD)

    # Select the GPIO pins used for the encoder K0-K3 data inputs
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)

    # Select the signal to select ASK/FSK
    GPIO.setup(18, GPIO.OUT)

    # Select the signal used to enable/disable the modulator
    GPIO.setup(22, GPIO.OUT)

    # Disable the modulator by setting CE pin lo
    GPIO.output (22, False)

    # Set the modulator to ASK for On Off Keying 
    # by setting MODSEL pin lo
    GPIO.output (18, False)

    # Initialise K0-K3 inputs of the encoder to 0000
    GPIO.output (11, False)
    GPIO.output (15, False)
    GPIO.output (16, False)
    GPIO.output (13, False)

def switch1_On():
    input('Hit return to Turn Switch1 ON')
    print("Turning Switch1 ON" + "\n") 
    # Set socket encoder pins to 0111
    GPIO.output(11, False)
    GPIO.output(15, True)
    GPIO.output(16, True)
    GPIO.output(13, True)
    time.sleep(0.1)
    GPIO.output(22, True) # Enable Modulator
    time.sleep(0.25)
    GPIO.output(22, False) # Disable Modulator
    
def switch2_On():
    input('Hit return to Turn Switch2 ON')
    print("Turning Switch2 ON" + "\n")
    # Set socket encoder pins to 1111
    GPIO.output(11, True)
    GPIO.output(15, True)
    GPIO.output(16, True)
    GPIO.output(13, True)
    time.sleep(0.1)
    GPIO.output(22, True) # Enable Modulator
    time.sleep(0.25)
    GPIO.output(22, False) # Disable Modulator

def switch1_Off():
    input('Hit return to Turn Switch1 OFF')
    print("Turning Switch OFF" + "\n")
    # Set socket encoder pins to 0110
    GPIO.output(11, False)
    GPIO.output(15, True)
    GPIO.output(16, True)
    GPIO.output(13, False)
    time.sleep(0.1)
    GPIO.output(22, True) # Enable Modulator
    time.sleep(0.25)
    GPIO.output(22, False) # Disable Modulator
    
def switch2_Off():
    input('Hit return to Turn Switch2 OFF')
    print("Turning Switch2 OFF" + "\n")
    # Set socket encoder pins to 1110
    GPIO.output(11, True)
    GPIO.output(15, True)
    GPIO.output(16, True)
    GPIO.output(13, False)
    time.sleep(0.1)
    GPIO.output(22, True) # Enable Modulator
    time.sleep(0.25)
    GPIO.output(22, False) # Disable Modulator
    
def all_on():
    switch1_on()
    switch2_on()
    
def all_off():
    switch1_off()
    switch2_off()
    
def write_TS(userID, sensorID, switchStatus):
    # send data as one string separeted by ","
    rpi2_list = [userID, sensorID, switchStatus]
    join_string2 = ",".join(rpi2_list)
    
    params = urllib.parse.urlencode({'field1': switchStatus, 'field2': userID, 'field3': sensorID, 'key': writeAPI})
    headers = {"Content-typZZe": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print(join_string2)
        print(response.status, response.reason + "\n")
        data = response.read()
        conn.close()
    except:
        print("Write Connection to TS Failed" + "\n")
    
def read_TS():
    data = requests.get(readAPI).json()
    result = data['feeds'][len(data['feeds']) - 1]['field1']
    # feeds->last entry ->field1
    #f = urllib.request.urlopen(readAPI)
    #value = json.load(f)
    #f.close()
    #print(value)
    #return value
    print("Field 1 Result: " + result + "\n")
    return result


if __name__ == '__main__':
    readAPI = 'https://api.thingspeak.com/channels/1160909/fields/1.json?api_key=' + '34BOVG6Y72Q6EEVB' + '&results='
    writeAPI = "O67GXT65S5U67H2Q"
    
    switch = SStatus(readAPI, writeAPI)
    switch.establishConnection()
    
    init_pins()
    
    try:
        write_TS(switch.userID, switch.sensorID, "OFF")
        state = read_TS()
        print("State of Device at Initial Connection: " + state + "\n")
    except:
        print("STATE INIT CONNECTION ERROR")
        print("State of Device After Initialization: NULL\n")
        state = None

    try:
        while True:
            state = read_TS()
            if state == "OFF":
                switch1_On()
                state = "ON"
                write_TS(switch.userID, switch.sensorID, state)
                print("Current State of Device1: " + state + "\n")
               # print(exit)
            elif state == "ON":
                switch1_Off()
                state = "OFF"
                write_TS(switch.userID, switch.sensorID, state)
              #  print(exit)
                print("Current State of Device1: " + state + "\n")
            else:
                print("STATE CONNECTION ERROR")
                state = None
                write_TS(switch.userID, switch.sensorID, state)
                print("Current State of Device1: " + state + "\n")

        time.sleep(1)
        
    except:
        print("\nCurrent State of Device: NULL\n")
        
    finally:
    # cleanup the GPIO before finishing
        GPIO.cleanup()
        
