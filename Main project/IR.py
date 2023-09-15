import time
import RPi.GPIO as GPIO
import requests

token = "XhUT8G1_zz-5EwTfzeIy3QqzUbEwFqyF"

blynkControl_roomLamp = False
blynk_relay_pin = False

#time in seconds after which the lamp will turn off after
PIR_timeSeconds = 10

relay_pin = 26
motionSensor = 13

#This module is responsible for running the IR motion sensor

# timers to monitor when when the sensor starts reading and time of the last read
global startTimer
global lastTrigger
lastTrigger =0
startTimer = False
HIGH = True
LOW = False

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(relay_pin,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(motionSensor,GPIO.IN)


# read data from blynk using GET request
def read(token,pin):
    api_url = "https://blynk.cloud/external/api/get?token="+token+"&"+pin
    response = requests.get(api_url)
    return response.content.decode()
# write data to blynk using GET request
def write(token, pin, value):
    api_url = "https://blynk.cloud/external/api/update?token="+token+"&"+pin+"="+value
    response = requests.get(api_url)
    if "200" in str(response):
        print("Value successfully updated")
    else:
        print("Could not find the device token or wrong pin format")

# control wither the lamp will be controlled by blynk mobile application or the readings from the sensor
def blynk_control():
    global blynkControl_roomLamp
    blynkControl_roomLamp = (read(token, "v22"))
    print(blynkControl_roomLamp) #debugging in terminal
    if blynkControl_roomLamp == '0':
        MOTION_SENSOR()
    else:
        global blynk_relay_pin
        blynk_relay_pin = (read(token, "v25"))
        print(blynk_relay_pin) # debugging in terminal
        if blynk_relay_pin =='1':
            GPIO.output(relay_pin, GPIO.HIGH)
        else:
            GPIO.output(relay_pin, GPIO.LOW)


#interrupt function so that it runs whenever the sensor detects movement and it sets the lastTrigger to the time of the last detected motion
def detectMovement(motionSensor):
    global startTimer
    if blynkControl_roomLamp == '0':
        print("MOTION DETECTED!!!")
        time.sleep(0.1)
        GPIO.output(relay_pin, GPIO.HIGH)
        write(token,"v25","1")
        startTimer = True
        global lastTrigger
        lastTrigger = time.time()

# now is the time that gets continuously updated in the while loop
# lastTrigger is subtracted from now to to get the time the lamp has been on for
def MOTION_SENSOR():
    global startTimer,timeDiff
    timeDiff = now - lastTrigger
    print("here")
    if startTimer and timeDiff > (PIR_timeSeconds):
        print("Motion stopped...")
        GPIO.output(relay_pin, GPIO.LOW)
        write(token,"v25","0")
        startTimer = False

#when the sensor detects motion, it goes from high to low, so interrupt is set to falling edge
GPIO.add_event_detect(motionSensor,GPIO.FALLING,callback=detectMovement)

while True:
    global now
    now = time.time()
    blynk_control()
    print('-------------------------')

GPIO.cleanup()
