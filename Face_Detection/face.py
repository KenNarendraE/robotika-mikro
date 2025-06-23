import cv2
import face_recognition

# Muat gambar wajah yang dikenali
known_image = face_recognition.load_image_file("ken.jpeg")
known_encoding = face_recognition.face_encodings(known_image)[0]
known_names = ["Ken"]  # Ganti sesuai nama

# Mulai webcam
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Ubah ke RGB
    rgb_frame = frame[:, :, ::-1]

    # Temukan semua wajah & encoding di frame ini
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Bandingkan dengan wajah yang dikenal
        matches = face_recognition.compare_faces([known_encoding], face_encoding)
        name = "Tidak Dikenal"

        if True in matches:
            name = known_names[0]

        # Gambar kotak dan nama
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Tampilkan
    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
