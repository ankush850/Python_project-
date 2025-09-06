import cv2
import os
import datetime

# ===============================
# Setup paths
# ===============================
output_dir = "captured_faces"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# ===============================
# Haar cascades for detection
# ===============================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
body_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_fullbody.xml"
)

# ===============================
# Start webcam
# ===============================
cap = cv2.VideoCapture(0)
cap.set(3, 640)   # Set width
cap.set(4, 480)   # Set height

print("[INFO] Press 's' to save a detected face")
print("[INFO] Press 'q' to quit")

# ===============================
# Main loop
# ===============================
while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Failed to grab frame.")
        break

    # Convert to grayscale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces and bodies
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = body_cascade.detectMultiScale(gray, 1.1, 3)

    # Draw face boxes
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(frame, "Face", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Draw body boxes
    for (x, y, w, h) in bodies:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
        cv2.putText(frame, "Body", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Add timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, timestamp, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Show video feed
    cv2.imshow("Face & Body Detection", frame)

    # Key controls
    key = cv2.waitKey(1) & 0xFF

    # Press 's' to save a snapshot of faces
    if key == ord('s') and len(faces) > 0:
        for i, (x, y, w, h) in enumerate(faces):
            face_roi = frame[y:y+h, x:x+w]
            filename = os.path.join(
                output_dir, f"face_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.jpg"
            )
            cv2.imwrite(filename, face_roi)
            print(f"[INFO] Saved face -> {filename}")

    # Press 'q' to quit
    if key == ord('q'):
        break

# ===============================
# Cleanup
# ===============================
cap.release()
cv2.destroyAllWindows()
print("[INFO] Program ended successfully.")
