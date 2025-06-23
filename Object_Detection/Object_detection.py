import torch
import cv2
import numpy as np

# Muat model YOLOv5 (gunakan model ringan yolov5s)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', trust_repo=True)

# Buka kamera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kamera tidak ditemukan")
    exit()

# Daftar objek yang ingin dideteksi
target_objects = ['bottle', 'book', 'paper']

# Fungsi bantu: rotasi gambar
def rotate_image(image, angle):
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, matrix, (w, h))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detected = False

    # Coba deteksi dengan rotasi 0, 90, dan -90 derajat
    for angle in [0, 90, -90]:
        rotated = rotate_image(frame, angle) if angle != 0 else frame
        results = model(rotated)
        df = results.pandas().xyxy[0]

        for _, row in df.iterrows():
            label = row['name']
            conf = row['confidence']
            x1, y1, x2, y2 = map(int, [row['xmin'], row['ymin'], row['xmax'], row['ymax']])

            if label in target_objects and conf > 0.5:
                # Kembalikan koordinat ke frame asli jika rotasi digunakan
                if angle != 0:
                    # Balik bounding box sesuai rotasi
                    box = rotated[y1:y2, x1:x2]
                    box = rotate_image(box, -angle)  # balikan kotak jika perlu
                    frame[y1:y2, x1:x2] = box
                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    detected = True

        if detected:
            break  # Tidak perlu cek rotasi lain jika sudah terdeteksi

    # Tampilkan hasil
    cv2.imshow("Deteksi Objek", frame)

    # ESC untuk keluar
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
