🔥 Deteksi Api dengan ESP32 – Proyek Sensor Api + Buzzer
Proyek ini menggunakan ESP32, sensor api (flame sensor), dan buzzer untuk mendeteksi keberadaan api. Ketika sensor mendeteksi nyala api, buzzer akan menyala sebagai alarm peringatan.

🧠 Cara Kerja
Sensor api mendeteksi nyala api melalui sinyal digital di pin GPIO 27

Jika api terdeteksi (sensor mengirim sinyal LOW), buzzer akan menyala selama 3 detik

Jika tidak ada api, buzzer akan mati dan sistem akan terus memantau

🧰 Komponen yang Digunakan
| Komponen             | Keterangan                    |
|----------------------|-------------------------------|
| ESP32                | Board mikrokontroler utama    |
| Sensor Api           | Sensor Digital                |
| Buzzer (aktif)       | Speaker kecil / modul buzzer  |
| Kabel Jumper         | Untuk koneksi antar komponen  |
| Breadboard (opsional)| Untuk merapikan rangkaian     |

## 🔌 Skema Koneksi

| Pin Sensor          | Pin ESP32 |
|---------------------|-----------|
| VCC                 | 3V3       |
| GND                 | GND       |
| AOUT / Analog Out   | GPIO 27   |


| Pin Buzzer          | Pin ESP32 |
|---------------------|-----------|
| VCC / +             | GPIO 15   |
| GND / -             | GND       |
