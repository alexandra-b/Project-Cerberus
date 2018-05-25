import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
from datetime import datetime
from datetime import timezone
from pytz import timezone
import serial
from firebase import firebase
#import pyrebase
FIREBASE_ROOT = 'https://guardian-dbd05.firebaseio.com/'
firebase = firebase.FirebaseApplication(FIREBASE_ROOT, None)

#Arduino Communication
serial_port = '/dev/ttyUSB0'
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate)
# Firebase database to hold data for this whole project


'''
# disable warnings sometimes printed when using SPI bus on Raspberry Pi
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#initialize the radio module
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
radio.setPayloadSize(1)
radio.setChannel(0x60) 										# must be the same for sensors and base station
radio.setDataRate(NRF24.BR_1MBPS)							# must be the same for sensors and base station
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(True)
radio.enableAckPayload()
radio.enableDynamicPayloads()
radio.openReadingPipe(1, [0xE0, 0xE0, 0xE0, 0xE0, 0xF2])	# set receiving address for this base station
'''
armed = None

def handle(msg):
	global armed
	armed = msg["armed"]
	if armed == "true":
		print("Listening from Arduino...")
	if armed == "false":
		print("STOPPED")


	'''
def handle(msg):
	global armed
	now = msg["data"]
	if now != armed:
		armed = now
		if now:
			print("Listening...")
			#radio.startListening()					# start listening if /armed is True in Firebase


		else:
			print("Stopped!")
			#radio.stopListening()					# stop listening if /armed is False in Firebase
'''
#stream = firebase.child("/armed").stream(handle) 	# create a stream to listen for changes for /armed in Firebase

sensorLocation = "kitchen"
try:
    while(1):
        result = firebase.get('/armed',None)
        #print(result)
        if result == 'true':
            hour = "%H:%M:%S"
            date = "%d-%m-%Y"
            now_time = datetime.now(timezone('UTC'))
            now_RO = now_time.astimezone(timezone('Europe/Athens'))
            print(now_RO.strftime(hour))
            print(now_RO.strftime(date))
            print("Add code of serial stream here")
            motion = 1
            dayEventPath = '/events/'+now_RO.strftime(date)+'/Alexa'
            dayJson = {"start": now_RO.strftime(hour)}
            firebase.patch(dayEventPath,dayJson)
            print("Add code of serial stream here")
            motion = 1
            if motion == 1:
                #hour = "%H:%M:%S"
                #date = "%d-%m-%Y"
                #now_time = datetime.now(timezone('UTC'))
                #now_RO = now_time.astimezone(timezone('Europe/Athens'))
                #print(now_RO.strftime(hour))
                #print(now_RO.strftime(date))
                eventJson = {"motion": "detected in {0}".format(sensorLocation)} #add sensor which detected motion
                #print(event)
                #print(new_event)
                eventpath = '/events/'+now_RO.strftime(date)+'/'+now_RO.strftime(hour)
                print(eventpath)
                firebase.patch(eventpath,eventJson)
                time.sleep(2)


except KeyboardInterrupt as e:			# catch KeyboardInterrupt
	stream.close()						# close the stream and exit program
	print()
