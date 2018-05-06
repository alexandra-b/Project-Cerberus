import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

GPIO.setmode(GPIO.BCM)

#         send address                    receive address
#         Pi to Nano                      Nano -> Pi
pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0,17) #PIN 0 and PIN 17

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS) #secure, slower => better range
radio.setPALevel(NRF24.PA_MIN) #close to Arduino Nano

radio.SetAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

#receiving data from Nano => reading pipe
radio.openReadingPipe(1, pipes[1])
radio.printDetails()
radio.startListening()

while True:
    #if nothing was received, go back to sleep to preserve power
    while not radio.available(0):
        time.sleep(1/100)

    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print("Received: {}".format(receivedMessage))

    #data send is byte (8 bits from 0 to 255) => decode message
    print("Decoding the message received...")
    string = ""

    #32 is SPACE, 126 is ~
    #48 is 0, 57 is 9, 65 is A, 90 is Z, 97 is a, 122 is z
    for n in receivedMessage:
        if(n >= 32 and n <= 126):
            string += chr(n)
    print("The message received is: {}".format(string))
