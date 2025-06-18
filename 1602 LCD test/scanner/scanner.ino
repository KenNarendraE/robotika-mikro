#include <Wire.h>

void setup() {
  Wire.begin(); // SDA = GPIO21, SCL = GPIO22 (default ESP32)
  Serial.begin(115200);
  Serial.println("I2C Scanner - ESP32");
}

void loop() {
  byte error, address;
  int nDevices = 0;

  Serial.println("Scanning I2C bus...");

  for (address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("I2C device found at address 0x");
      if (address < 16) Serial.print("0");
      Serial.print(address, HEX);
      Serial.println("  ✓");
      nDevices++;
    } else if (error == 4) {
      Serial.print("Unknown error at address 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
    }
  }

  if (nDevices == 0)
    Serial.println("No I2C devices found.");
  else
    Serial.println("Done.\n");

  delay(5000); // tunggu 5 detik sebelum scan ulang
}
