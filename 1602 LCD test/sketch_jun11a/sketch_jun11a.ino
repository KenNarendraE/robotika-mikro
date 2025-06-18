#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2); // Ganti alamat sesuai hasil I2C Scanner

String teks = " Halo, ini adalah teks berjalan di LCD 1602! ";
int posisi = 0;

void setup() {
  Wire.begin(21, 22);  // Pin default ESP32 I2C
  lcd.init();
  lcd.backlight();
}

void loop() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(teks.substring(posisi, posisi + 16));

  posisi++;
  if (posisi > teks.length() - 16) {
    posisi = 0;
  }

  delay(300); // Kecepatan scroll, bisa diatur
}
