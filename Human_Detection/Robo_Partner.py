import cv2
import torch
import mediapipe as mp
import time
import serial

# ==== Inisialisasi YOLOv5 untuk deteksi orang ====
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.classes = [0]  # hanya deteksi class 'person'

# ==== Inisialisasi MediaPipe Hands ====
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

# ==== Inisialisasi Serial ke ESP32/Arduino ====
ser = serial.Serial('COM3', 115200, timeout=1)  # Ganti COM3 sesuai port kamu
time.sleep(2)  # Tunggu koneksi stabil

# Fungsi untuk mendeteksi status jari
def get_fingers_status(landmarks):
    tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
    fingers = []

    # Thumb
    if landmarks[tips[0]].x < landmarks[tips[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # 4 jari lainnya
    for tip in tips[1:]:
        if landmarks[tip].y < landmarks[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

# ==== Mulai Kamera ====
cap = cv2.VideoCapture(1)  # Ganti ke 0 jika webcam utama
prev_gesture = None
last_action_time = time.time()
current_gesture_text = ""
gesture_active_until = 0  # waktu sampai gesture masih aktif

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    direction = "Tidak Ada"
    detected_person = False

    # ==== DETEKSI ORANG (YOLO) ====
    results_yolo = model(frame)
    detections = results_yolo.pandas().xyxy[0]

    for _, row in detections.iterrows():
        xmin, ymin, xmax, ymax = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
        label = row['name']

        if label == 'person':
            detected_person = True
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            center_x = (xmin + xmax) // 2
            center_y = (ymin + ymax) // 2
            cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)

            frame_center = frame.shape[1] // 2

            # Jika gesture sedang aktif, abaikan kontrol dari deteksi orang
            if time.time() > gesture_active_until:
                if center_x < frame_center - 50:
                    direction = "← Kiri"
                    ser.write(b'0')  # arah tidak ditentukan, tetap kirim stop
                elif center_x > frame_center + 50:
                    direction = "→ Kanan"
                    ser.write(b'0')
                else:
                    direction = "↑ Maju"
                    ser.write(b'1')

    if not detected_person and time.time() > gesture_active_until:
        ser.write(b'0')  # Stop jika tidak ada orang & tidak dalam mode gesture

    # ==== DETEKSI TANGAN (MediaPipe) ====
    results_hand = hands.process(frame_rgb)
    if results_hand.multi_hand_landmarks:
        for hand_landmarks in results_hand.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmark_list = hand_landmarks.landmark
            fingers = get_fingers_status(landmark_list)
            gesture = tuple(fingers)

            if gesture != prev_gesture and time.time() - last_action_time > 1:
                prev_gesture = gesture
                last_action_time = time.time()

                # === Gesture Dikenali ===
                if gesture == (0, 1, 0, 0, 0):
                    current_gesture_text = "🖐️ Telunjuk → FOLLOW"
                    ser.write(b'1')  # Maju
                    gesture_active_until = time.time() + 2  # Aktif 2 detik
                elif gesture == (0, 0, 0, 0, 0):
                    current_gesture_text = "✊ Genggam → STOP"
                    ser.write(b'0')  # Stop
                    gesture_active_until = time.time() + 2
                elif gesture == (0, 1, 1, 1, 1):
                    current_gesture_text = "☝️ Index + lainnya → BEL0K KIRI"
                    ser.write(b'4')  # mundur
                    gesture_active_until = time.time() + 2
                elif gesture == (0, 1, 1, 1, 0):
                    current_gesture_text = "🖐️ Semua Jari → BEL0K KANAN"
                    ser.write(b'2')  # Belok kanan
                    gesture_active_until = time.time() + 2
                elif gesture == (0, 1, 1, 0, 0):
                    current_gesture_text = "☝️ Index + lainnya → BEL0K KIRI"
                    ser.write(b'3')  # Belok kiri
                    gesture_active_until = time.time() + 2
    else:
        current_gesture_text = ""  # Reset jika tidak ada tangan

    # ==== TAMPILKAN TEKS GESTURE & ARAH ====
    if current_gesture_text:
        cv2.putText(frame, current_gesture_text, (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(frame, f"Arah: {direction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # ==== TAMPILKAN FRAME ====
    cv2.imshow("Gabungan: Orang + Gesture", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
ser.close()
cv2.destroyAllWindows()
