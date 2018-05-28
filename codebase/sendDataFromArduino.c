#include <SPI.h>  //how the transceiver communicates
#include <RF24.h>

//Digital Pins: CE, CSN
RF24 radio(9, 10);


int sensor = 2;              // the pin that the sensor is atteched to
int state = LOW;             // by default, no motion detected
int val = 0;                 // variable to store the sensor status (value)

void setup() {
/*
  radio.begin()
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  radio.openWritingPipe(0xF0F0F0E1LL); //need to match the one from R-Pi
  radio.enableDynamicPayloads();
  radio.powerUp();
*/
  pinMode(sensor, INPUT);    // initialize sensor as an input
  digitalWrite(2, 1);
}

void loop(){
  val = digitalRead(sensor);   // read sensor value
  if (val == HIGH) {
    // check if the sensor is HIGH
    if(state == LOW){
      Serial.begin(9600);        // initialize serial
      //radio.write(&text, sizeof(text));
      Serial.println("1");
      Serial.end();
    }
  }
  state=val;
}
