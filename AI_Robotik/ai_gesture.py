import cv2
import mediapipe as mp
import keyboard
import time

# Inisialisasi Mediapipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

# Fungsi untuk mengecek status jari (1 = terbuka, 0 = tertutup)
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

# Mulai webcam
cap = cv2.VideoCapture(1)

prev_gesture = None
last_action_time = time.time()

while True:
    success, img = cap.read()
    if not success:
        break

    # Flip gambar dan konversi ke RGB
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Deteksi tangan
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmark_list = hand_landmarks.landmark
            fingers = get_fingers_status(landmark_list)
            gesture = tuple(fingers)

            # Hindari aksi yang terus-menerus (beri delay 1 detik)
            if gesture != prev_gesture and time.time() - last_action_time > 1:
                prev_gesture = gesture
                last_action_time = time.time()

                # Mapping gestur ke aksi
                if gesture == (0, 1, 0, 0, 0):
                    print("Telunjuk → Next Slide")
                    keyboard.send('l')

                elif gesture == (0, 1, 1, 0, 0):
                    print("2 Jari → Pause / Play")
                    keyboard.send('space')

                elif gesture == (0, 1, 1, 1, 0):
                    print("3 Jari → Previous Slide")
                    keyboard.send('j')

                elif gesture == (0, 1, 1, 1, 1):
                    print("4 Jari → Previous Slide")
                    keyboard.send('up')

                elif gesture == (1, 1, 1, 1, 1):
                    print("5 Jari → Previous Slide")
                    keyboard.send('down')

                elif gesture == (0, 0, 0, 0, 0):
                    print("Genggam → Stop")
                    keyboard.send('m')

    # Tampilkan hasil
    cv2.imshow("Hand Gesture Control", img)

    if cv2.waitKey(1) & 0xFF == 27:  # Tekan ESC untuk keluar
        break

cap.release()
cv2.destroyAllWindows()
