#include <Servo.h>

// Definisi pin sensor buka tutup
#define TRIG_PIN 14     // D5 - Sensor tangan (buka tutup)
#define ECHO_PIN 12     // D6

// Definisi pin sensor isi sampah
#define TRIG_PIN2 5     // D1 - Sensor isi sampah
#define ECHO_PIN2 4     // D2

#define SERVO_PIN 2     // D4
#define LED_PIN 16      // D0 - LED indikator sampah penuh

Servo tutupSampah;

void setup() {
  Serial.begin(9600);

  tutupSampah.attach(SERVO_PIN);
  tutupSampah.writeMicroseconds(2200);  // Tutup awal

  // Setup pin sensor tangan
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Setup pin sensor isi sampah
  pinMode(TRIG_PIN2, OUTPUT);
  pinMode(ECHO_PIN2, INPUT);

  // Setup LED indikator
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
}

void loop() {
  bacaSensorTangan();       // Sensor untuk buka tutup otomatis
  bacaSensorIsiSampah();    // Sensor untuk deteksi penuh
  delay(200);               // Delay siklus baca
}

// Fungsi untuk mendeteksi tangan (sensor 1)
void bacaSensorTangan() {
  long durasi;
  float jarak;

  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  durasi = pulseIn(ECHO_PIN, HIGH, 30000);
  jarak = durasi * 0.034 / 2;

  Serial.print("Jarak tangan: ");
  Serial.print(jarak);
  Serial.println(" cm");

  if (jarak > 0 && jarak < 45) {
    tutupSampah.writeMicroseconds(600);  // Buka
    delay(3000);                         // Tunggu
    tutupSampah.writeMicroseconds(2200); // Tutup
    delay(500);                          // Stabilisasi
  }
}

// Fungsi untuk mendeteksi penuh (sensor 2)
void bacaSensorIsiSampah() {
  long durasi;
  float jarak;

  digitalWrite(TRIG_PIN2, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN2, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN2, LOW);

  durasi = pulseIn(ECHO_PIN2, HIGH, 30000);
  jarak = durasi * 0.034 / 2;

  Serial.print("Jarak isi sampah: ");
  Serial.print(jarak);
  Serial.println(" cm");

  if (jarak <= 10) {
    digitalWrite(LED_PIN, HIGH);  // Sampah penuh
  } else {
    digitalWrite(LED_PIN, LOW);   // Masih kosong
  }
}
