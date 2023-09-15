import time
import RPi.GPIO as GPIO
import requests

token = "XhUT8G1_zz-5EwTfzeIy3QqzUbEwFqyF"

#This module is responsible for running the buzzer and ultrasonic sensor


blynkControl_doorBell = False
doorbell_PinValue = False

# time in seconds which the buzzer will stay on for
BUZ_timeSeconds = 5

motionSensor = 13
trigPin = 3
echoPin = 5
buz = 11


duration = 0
distance = 0
value = 100


lastTrigger = 0
buz_time = 0


global startTimer
startTimer = False
buz_flag = False
HIGH = True
LOW = False

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(echoPin,GPIO.IN)
GPIO.setup(trigPin,GPIO.OUT)
GPIO.setup(buz, GPIO.OUT,initial=GPIO.LOW)
GPIO.output(trigPin, False)


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


# activate the ultrasonice sensor and detect if the distance read is less then or equal to 100
# if the distance is less than or equal 100 and less than or equal 25 turn the buzzer on for 5 seconds
def doorBell():
    global pulse_start, pulse_stop, value, buz_flag, buz_time, now
    GPIO.output(trigPin, True)
    time.sleep(0.00001)
    GPIO.output(trigPin, False)

    while GPIO.input(echoPin) == 0:
        pulse_start = time.time()

    while GPIO.input(echoPin) == 1:
        pulse_stop = time.time()

    pulse_time = pulse_stop - pulse_start
    distance = pulse_time * 17150
    rounded_distance = round(distance, 2)
    if buz_flag == 0 and value >= rounded_distance:
        value = distance
        if value <= 25:
            print("Distance = ", rounded_distance)
            print("the doorbell is ON. ")
            GPIO.output(buz, True)
            buz_time = time.time()
            buz_flag = True
            GPIO.output(buz, True)
            write(token,"v26","1")
    if buz_flag == True and (now - buz_time > (BUZ_timeSeconds)):
        print("the doorbell is OFF. ")
        GPIO.output(buz, False)
        buz_flag = False
        write(token, "v26", "0")
    value = 100
    global f
    f = 1

# control wither blynk or the ultrasonic sensor control the buzzer
def blynk_control():
    global pulse_start, pulse_stop, value, buz_flag, buz_time, now, f
    global blynkControl_doorBell
    blynkControl_doorBell = (read(token, "v23"))
    print(blynkControl_doorBell)
    if blynkControl_doorBell =='0':
        doorBell()
    else:
        if buz_flag == True and f==1:
            print("the doorbell is OFF. ")
            GPIO.output(buz, False)
            buz_flag = False
            write(token, "v26", "0")

        global doorbell_PinValue
        doorbell_PinValue = (read(token, "v26"))
        print(doorbell_PinValue)
        if doorbell_PinValue =='1':
            GPIO.output(buz,GPIO.HIGH)
            buz_flag=1
            f=0
            buz_time=time.time()
        else:
            GPIO.output(buz,GPIO.LOW)
            f = 1


while True:
    global now
    now = time.time()
    blynk_control()
    print('-------------------------')

GPIO.cleanup()
