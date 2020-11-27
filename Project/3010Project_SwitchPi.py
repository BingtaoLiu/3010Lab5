import RPi.GPIO as GPIO
import time

#from switchTEST import testStatus

switchS = "OFF"
userID = '20'
sensorID = '2'

try:
    def testStatus(status):
        stateTest = status
        return stateTest
            
    state = testStatus(switchS)
    print("State of Device before connection: " + state + "\n")
except:
    print("State of Device before connection: NULL\n")
    state = None

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

def switchOn():
    input('Hit return to Turn ON')
    print("Turning Switch ON")
    # Set socket encoder pins to 0111
    GPIO.output(11, False)
    GPIO.output(15, True)
    GPIO.output(16, True)
    GPIO.output(13, True)
    time.sleep(0.1)
    GPIO.output(22, True) # Enable Modulator
    time.sleep(0.25)
    GPIO.output(22, False) # Disable Modulator

def switchOff():
    input('Hit return to Turn OFF')
    print("Turning Switch OFF")
    # Set socket encoder pins to 0110
    GPIO.output(11, False)
    GPIO.output(15, True)
    GPIO.output(16, True)
    GPIO.output(13, False)
    time.sleep(0.1)
    GPIO.output(22, True) # Enable Modulator
    time.sleep(0.25)
    GPIO.output(22, False) # Disable Modulator

try:
    while True:
        if state == "OFF":
            switchOn()
            state = "ON"
            print("Current State of Device: " + state + "\n")
           # print(exit)
        elif state == "ON":
            switchOff()
            state = "OFF"
          #  print(exit)
            print("Current State of Device: " + state + "\n")
        else:
            print("CONNECTION ERROR")
            state = None
            print("Current State of Device: " + state + "\n")

    time.sleep(1)
    
except:
    print("Current State of Device: NULL\n")
    
finally:
# cleanup the GPIO before finishing
    GPIO.cleanup()
    
