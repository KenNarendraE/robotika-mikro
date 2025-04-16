#define FLAME_SENSOR_PIN 27
#define BUZZER_PIN 15

void setup() {
  Serial.begin(115200);
  pinMode(FLAME_SENSOR_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  int flameDetected = digitalRead(FLAME_SENSOR_PIN);
  Serial.println(flameDetected == LOW ? "🔥 API TERDETEKSI" : "✅ AMAN");

  if (flameDetected == LOW) {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(3000);
    digitalWrite(BUZZER_PIN, LOW);
  } else {
    digitalWrite(BUZZER_PIN, LOW);
  }

  delay(500);
}
