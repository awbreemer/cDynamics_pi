#include <SPI.h>

int count = 0;
uint16_t angle = 0x3ffe;
SPISettings settingsA;

void setup() {
settingsA = SPISettings(10000000, MSBFIRST, SPI_MODE1);
pinMode(D4,OUTPUT);
SPI.begin();
}



void loop() {
  // put your main code here, to run repeatedly:
  SPI.beginTransaction(settingsA);
  digitalWrite(D4, LOW);
  stat = SPI.transfer(angle);
  val1 = SPI.transfer(angle);
  val2 = SPI.transfer(angle);
  digitalWrite(D4, HIGH);
  SPI.endTransaction();
  Serial.println(val1);
  Serial.println(val2);
  delay(500);
  count++;
  if(count > 60){
    exit(0);
  }
}
