import cv2
import os
import numpy as np

current_label = 0
for person_name in os.listdir(data_path):
    person_folder = os.path.join(data_path, person_name)
    if not os.path.isdir(person_folder):
        continue
    
    label_map[current_label] = person_name
    for img_name in os.listdir(person_folder):
        img_path = os.path.join(person_folder, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        faces.append(img)
        labels.append(current_label)
    current_label += 1

faces = np.array(faces)
labels = np.array(labels)

# Train recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, labels)

# Save model
recognizer.save("trained_faces.yml")
np.save("labels.npy", label_map)
print("Training complete, model saved.")
