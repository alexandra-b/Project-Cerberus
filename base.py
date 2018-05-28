import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
from datetime import datetime
from datetime import timezone
from pytz import timezone
import serial
from firebase import firebase
import subprocess
import json
import smtplib
import uuid
import os
import glob
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

cmd = 'python /home/pi/Desktop/alexaHomeSecurity/Website/simpleWeb.py'
FIREBASE_ROOT = 'https://guardian-dbd05.firebaseio.com/'
firebase = firebase.FirebaseApplication(FIREBASE_ROOT, None)

#start server that livestreams
p=subprocess.Popen(cmd,shell=True)

#communication to Arduino
serial_port = '/dev/ttyUSB1'
baud_rate = 9600
ser = serial.Serial(serial_port,baud_rate,timeout = 3)
s = [0]

def send_email():
    fromaddr = "pitestpi11@gmail.com"
    toaddr = "alexandra.bocereg@yahoo.com"
    text = 'Motion has been detected! Check this link to see a livestream '
    text += ' 172.20.10.5:5000'
    subject = 'Security ALERT!'
    message = 'Suject: {}\n\n{}'.format(subject,text)
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    username = "pitestpi11@gmail.com"
    password = "pitestpi1"
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()

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

was_on         = False  #Guardian pre-state for   activating
was_stopped    = False  #Guardian pre-state for deactivating
sensorLocation = "kitchen"
try:
    ok = 0
    while(1):
        result = firebase.get('/armed',None)
        #print(result)
        time.sleep(1)

        #check if motion detected
        #read_serial = ser.readline()
        #s[0] = int (ser.readline(),10)
        #print(result)
        ok = 0;
        if result == "true":

            # Add Guardian event to the firebase
            hour = "%H:%M:%S"
            date = "%d-%m-%Y"
            now_time = datetime.now(timezone('UTC'))
            now_RO = now_time.astimezone(timezone('Europe/Athens'))
            #print(now_RO.strftime(hour))
            #print(now_RO.strftime(date))

            if (was_on == False):
                dayEventPath = '/events/'+now_RO.strftime(date)+'/Guardian'
                dayJson = {"start": now_RO.strftime(hour)}
                firebase.patch(dayEventPath,dayJson)
                print("was_n True")
                was_on = True #Only update the 'start' once for this entry

            read_serial = ser.readline()
            #s[0]        = str(int (read_serial,10)) #str(int (ser.readline(),10))
            #if(s[0] == '1'):
            read_byte = read_serial+b'0'
            transformed_read_byte = (str (read_byte))
            getLen = len(transformed_read_byte)
            #print(transformed_read_byte + " " )
            #print(len(transformed_read_byte))
            #print(" ")
            #if(s[0] == '0'):
             #   prev = 0
            #HERE CHECK IF MOTION DETECTED SO U CAN ALERT THE USER
            if(getLen > 5):#s[0] == '1'):# and prev == 0): #also change here ok s.t mail is sent each time
                #print("Add code of serial stream here")
                motion = 1
                prev   = 1

                # Add trigger event into the database at the day created by Alexa init
                eventJson = {"motion": "detected in {0}".format(sensorLocation)} #add sensor which detected motion
                eventpath = '/events/'+now_RO.strftime(date)+'/'+now_RO.strftime(hour)
                print(eventpath)
                firebase.patch(eventpath,eventJson)

                time.sleep(2)
                if ok == 0:
                    send_email()
                    ok = 1
            was_on = True

        if (result == "false" and was_on == True and was_stopped == False):
            hour = "%H:%M:%S"
            date = "%d-%m-%Y"
            now_time = datetime.now(timezone('UTC'))
            now_RO = now_time.astimezone(timezone('Europe/Athens'))
            print(now_RO.strftime(hour))
            print(now_RO.strftime(date))
            dayEventPath = '/events/'+now_RO.strftime(date)+'/Guardian'
            dayJson = {"stop": now_RO.strftime(hour)}
            firebase.patch(dayEventPath,dayJson)
            print("was_stopped True")
            was_on      = False
            was_stopped = True   #Only update the 'stop' once for this entry

except KeyboardInterrupt as e:			# catch KeyboardInterrupt
	stream.close()		         # close the stream and exit program
	elseprint()
