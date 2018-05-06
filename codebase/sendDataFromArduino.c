#include <SPI.h>  //how the transceiver communicates
#include <RF24.h>

//Digital Pins: CE, CSN
RF24 radio(9, 10);
int PIR_output = 5; // Output of Passive Infra-Red

void setup(){
  radio.begin()
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  radio.openWritingPipe(0xF0F0F0E1LL); //need to match the one from R-Pi
  radio.enableDynamicPayloads();
  radio.powerUp();

  pinMode(PIR_output, INPUT);
  Serial.begin(9600);
}

void loop(){
  const char text[] = "Hello World";
  if(digitalRead(PIR_output) == HIGH){
    radio.write(&text, sizeof(text));
    delay(1000);
    Serial.println("Motion detected!");
  }
  else{
    Serial.println("Scanning...");
  }
}
