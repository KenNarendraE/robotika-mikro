#define MOISTURE_SENSOR_PIN 34
#define BUZZER_PIN 15

const int DRY_THRESHOLD = 2000;  // Sesuaikan dengan kondisi sensor kamu

void setup() {
  Serial.begin(115200);
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  int moisture = analogRead(MOISTURE_SENSOR_PIN);
  Serial.print("Moisture: ");
  Serial.println(moisture);

  if (moisture > DRY_THRESHOLD) {
    // Tanah kering: tanaman "berteriak"
    digitalWrite(BUZZER_PIN, HIGH);
    delay(3000);
    digitalWrite(BUZZER_PIN, LOW);
    delay(100);
  } else {
    digitalWrite(BUZZER_PIN, LOW);
  }

  delay(500);
}