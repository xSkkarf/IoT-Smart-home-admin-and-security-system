import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
token = "XhUT8G1_zz-5EwTfzeIy3QqzUbEwFqyF"


#this module is responsible for running the rfid sensor and check if the scanned rfid card is valid or not
blynkControl_doorLock = False
doorlock_PinValue = False

#time the leds indicating if the card is valid or not stay on for
doorlock_timeSeconds = 2

SS_PIN = 21
RST_PIN = 27
access_pin = 38
denied_pin = 40

doorlock_access_time = 0
#doorlock_denied_time = now

global startTimer
startTimer = False
doorlock_access_flag = False
doorlock_denied_flag = False
HIGH = True
LOW = False

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(access_pin,GPIO.OUT)
GPIO.setup(denied_pin,GPIO.OUT)


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



# control wither blynk or the rfid sensor control the leds
def blynk_control():
    global blynkControl_doorLock
    blynkControl_doorLock = (read(token, "v24"))
    if blynkControl_doorLock =='0':
        rfid_read()
    else:
        global doorlock_PinValue
        doorlock_PinValue = (read(token, "v27"))
        print(doorlock_PinValue)
        if doorlock_PinValue =='1':
            GPIO.output(access_pin, GPIO.HIGH)
        else:
            GPIO.output(access_pin, GPIO.LOW)


global now
global timeDiff
global true
global timea,timed,fa,fd
fa = 0
fd = 0
timea=0
timed=0
reader = SimpleMFRC522()

# rfid card reader function
# if there is no card it returns None
# if a valid card if read, a led indicating authorized access will light up,
# else another led indicating unaithorized access will light up
def rfid_read():
    global timea,timed,fa,fd,now
    # fa flag for detection of authorized card, fd flag for detection of unauthorized card
    if fa ==1 and now - timea >= doorlock_timeSeconds:
        GPIO.output(access_pin, GPIO.LOW)
        write(token,"v27","0")
        fa=0
    if fd ==1 and now - timed >= doorlock_timeSeconds:
        GPIO.output(denied_pin, GPIO.LOW)
        fd = 0
    id = reader.read_id_no_block()
    if id is None:
        return
    #check id of cards
    if id == 764197935610:
        timea = time.time()
        print("Test1\nAuthorized access")
        # send the name of the card holder and the time when the card the read to blynk
        write(token, "v28", "Emad-Sakr")
        t = time.localtime()
        # time is converted from GMT to GMT+2 by accessing the time.localtime by indexing
        time_sent = str((int(t[3])+2)%24) + ":" + str(t[4]) + ":" + str(t[5])
        print(time_sent)
        write(token, "v29", time_sent)
        fa=1
        #turn on led on access_pin to indicate authorized access
        GPIO.output(access_pin, GPIO.HIGH)
        write(token,"v27","1")
    elif id == 730404479544:
        timea = now
        print("Test2\nAuthorized access")
        write(token, "v28", "Ahmed-Hassouna")
        write(token,"v27","1")
        t = time.localtime()
        # time is converted from GMT to GMT+2 by accessing the time.localtime by indexing
        time_sent = str((int(t[3])+2)%24) + ":" + str(t[4]) + ":" + str(t[5])
        print(time_sent)
        write(token, "v29", time_sent)
        fa=1
        GPIO.output(access_pin, GPIO.HIGH)
    else:
        # turn on led on denied_pin to indicate unauthorized rfid card
        print("unknown")
        write(token, "v28", "Access Denied")
        t = time.localtime()
        # time is converted from GMT to GMT+2 by accessing the time.localtime by indexing
        time_sent = str((int(t[3])+2)%24) + ":" + str(t[4]) + ":" + str(t[5])
        print(time_sent)
        write(token, "v29", time_sent)
        timed= time.time()
        fd=1
        GPIO.output(denied_pin,GPIO.HIGH)
    time.sleep(0.5)


while True:
    global now
    now = time.time()
    blynk_control()

GPIO.cleanup()
