#include <DFRobotDFPlayerMini.h>

#define MOISTURE_SENSOR_PIN 34
const int DRY_THRESHOLD = 2000;

HardwareSerial dfSerial(2); // UART2 (Serial2)
DFRobotDFPlayerMini myDFPlayer;

bool isDry = false;  // Status sebelumnya

void setup() {
  Serial.begin(115200);
  dfSerial.begin(9600, SERIAL_8N1, 16, 17); // RX=16, TX=17

  Serial.println("Initializing DFPlayer...");
  if (!myDFPlayer.begin(dfSerial)) {
    Serial.println("DFPlayer tidak terdeteksi.");
    while (true); // berhenti kalau gagal
  }

  myDFPlayer.volume(25);  // atur volume 0-30
  Serial.println("DFPlayer siap!");
}

void loop() {
  int moisture = analogRead(MOISTURE_SENSOR_PIN);
  Serial.print("Moisture: ");
  Serial.println(moisture);

  if (moisture > DRY_THRESHOLD) {
    if (!isDry) {
      // Baru saja jadi kering
      Serial.println("Tanah kering! Mainkan suara.");
      myDFPlayer.play(1);
      isDry = true;
    }
  } else {
    if (isDry) {
      // Baru saja jadi basah
      Serial.println("Tanah sudah cukup lembap. Hentikan suara.");
      myDFPlayer.stop();
      isDry = false;
    }
  }
//ini delay 0,5 detik
  delay(500);
}
