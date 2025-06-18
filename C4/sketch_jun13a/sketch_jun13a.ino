#include <LiquidCrystal_I2C.h>
#include <Keypad.h>
#include <HardwareSerial.h>
#include <DFRobotDFPlayerMini.h>

// LCD
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Keypad
const byte ROWS = 4;
const byte COLS = 3;
char keys[ROWS][COLS] = {
  {'1','2','3'},
  {'4','5','6'},
  {'7','8','9'},
  {'*','0','#'}
};
byte rowPins[ROWS] = {13, 12, 14, 27};    // Sesuaikan dengan koneksi fisik
byte colPins[COLS] = {26, 25, 33};        // Sesuaikan dengan koneksi fisik
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

// DFPlayer dengan UART2 (HardwareSerial)
HardwareSerial mp3Serial(2); // UART2
DFRobotDFPlayerMini mp3;

String inputCode = "";
String correctCode = "1234";
unsigned long countdownStart;
int duration = 20; // detik
bool triggered = false;
bool disarmed = false;

void setup() {
  lcd.init();
  lcd.backlight();
  keypad.setDebounceTime(100);

  mp3Serial.begin(9600, SERIAL_8N1, 16, 17); // RX = GPIO16, TX = GPIO17
  if (!mp3.begin(mp3Serial)) {
    lcd.setCursor(0, 0);
    lcd.print("DFPlayer Error");
    while (true); // berhenti di sini jika DFPlayer gagal
  }

  mp3.volume(30);

  lcd.setCursor(0, 0); lcd.print("READY TO PLANT");
  lcd.setCursor(0, 1); lcd.print("Press *");
}

void loop() {
  char key = keypad.getKey();
  if (!triggered && key) {
    triggered = true;
    countdownStart = millis();
    mp3.play(1); // sirine.mp3
    inputCode = "";
  }

  if (triggered && !disarmed) {
    int secondsLeft = duration - (millis() - countdownStart) / 1000;

    // Baris pertama: Countdown:<waktu>
    lcd.setCursor(0, 0);
    lcd.print("                "); // 16 spasi untuk clear satu baris
    lcd.setCursor(0, 0);
    lcd.print("Countdown:");
    lcd.setCursor(11, 0);
    lcd.print("  "); // bersihkan dua digit
    lcd.setCursor(11, 0);
    lcd.print(secondsLeft);

    lcd.setCursor(0, 1);  
    lcd.print("Code: ");
    lcd.print("        "); // bersihkan sisa karakter
    lcd.setCursor(6, 1);
    lcd.print(inputCode);


    if (key) {
      if (key == '#') {
        if (inputCode == correctCode) {
          disarmed = true;
          lcd.clear();
          lcd.print("DISARMED");
          mp3.play(3); // disarmed.mp3
        } else {
          lcd.clear();
          lcd.print("***WRONG CODE***");
          delay(1000);
          inputCode = "";
        }
      } else if (key == '*') {
        inputCode = "";
      } else {
        inputCode += key;
      }
    }

    if (secondsLeft <= 0 && !disarmed) {
      lcd.clear();
      lcd.print("BOOM!");
      mp3.play(2); // boom.mp3
      delay(5000);
      triggered = false;
      inputCode = "";
      disarmed = false;
      lcd.clear();
      lcd.setCursor(0, 0); lcd.print("READY TO PLANT");
      lcd.setCursor(0, 1); lcd.print("Press *");
    }
  }
}
