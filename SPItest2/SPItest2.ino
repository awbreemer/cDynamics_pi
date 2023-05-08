  #include <SPI.h>
  const int SSPin = D4;
  const long desiredFrequency = 10000000;
  uint16_t data = 0x3FFE;

  uint16_t modifyBit(uint16_t value, uint8_t bitPosition, bool bitValue) {
  if (bitValue) {
    // Set the bit at the specified position
    value |= (1 << bitPosition);
  } else {
    // Clear the bit at the specified position
    value &= ~(1 << bitPosition);
  }
  return value;
}

uint16_t get14bits(uint16_t value){
  uint16_t newValue = modifyBit(value, 15, false);
  newValue = modifyBit(newValue, 14, false);
  return(newValue);
}



void setup() {
  // put your setup code here, to run once:
  data = modifyBit(data, 14, true);
  SPI.begin();
  SPISettings spiSettings(desiredFrequency, MSBFIRST, SPI_MODE1);
  //SPI.setDataMode(SPI_MODE1);
  //SPI.setClockDivider(clockDivider);

  pinMode(SSPin, OUTPUT);
  digitalWrite(SSPin, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(SSPin, LOW);
  uint16_t receivedData = SPI.transfer16(data);
  digitalWrite(SSPin, HIGH);
  receivedData = get14bits(receivedData);
  int decodedData = ((int)receivedData << 8) | (receivedData >> 8);
  Serial.println(decodedData);
  delay(500);
}
