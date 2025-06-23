import cv2
import torch

# Muat model YOLOv5s dari PyTorch Hub
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.classes = [0]  # Kelas 0 = 'person'

# Buka webcam
cap = cv2.VideoCapture(0)  # Ganti 0 jika kamu pakai kamera USB eksternal

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Deteksi objek
    results = model(frame)

    # Konversi hasil ke pandas DataFrame
    detections = results.pandas().xyxy[0]

    # Gambar bounding box hanya untuk class 'person'
    for i, row in detections.iterrows():
        xmin, ymin, xmax, ymax = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
        confidence = float(row['confidence'])
        label = row['name']

        # Gambar kotak dan label
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        cv2.putText(frame, f"{label} {confidence:.2f}", (xmin, ymin - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Koordinat tengah orang (untuk pengembangan robot mengikuti)
        center_x = (xmin + xmax) // 2
        center_y = (ymin + ymax) // 2
        cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)

        # Di sini kamu bisa kontrol arah motor berdasarkan posisi center_x

    cv2.imshow("Deteksi Orang", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
