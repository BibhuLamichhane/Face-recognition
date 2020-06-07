import os
import sys
import subprocess
import capture
import cv2
import face_recognition
import numpy as np

CAM = cv2.VideoCapture(0)
cv2.namedWindow = 'test'
face_loc = []


def store_new_image():
    name = input("Enter your name: ")
    frame = capture.capture()
    cv2.imwrite(f"images/{name}.png", frame)


original_commands = {'str_n_img': store_new_image, 'sni': store_new_image}
                    
commands = sys.argv[1:]

for root, directories, files in os.walk('.'):
    if "images" in directories:
        break
    elif "images" not in directories:
        subprocess.call("mkdir images", shell=True)
        break

for command in commands:
    if original_commands.get(command) is not None:
        original_commands[command]()

images = []
for r, directory, file in os.walk('./images'):
    images = file

encodings = [face_recognition.face_encodings(face_recognition.load_image_file(f"images/{encoding}"))[0]
             for encoding in images]

names = [name.rstrip('.png') for name in images]
now = True

while True:
    ret, f = CAM.read()

    if not ret:
        break

    temp_frame = cv2.resize(f, (0, 0), fx=0.25, fy=0.25)
    temp_frame = temp_frame[:, :, ::-1]

    if now:
        face_loc = face_recognition.face_locations(temp_frame)
        face_encodings = face_recognition.face_encodings(temp_frame, face_loc)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(encodings, face_encoding)
            name = 'N/A'
            face_distances = face_recognition.face_distance(encodings, face_encoding)
            name_index = np.argmin(face_distances)
            if matches[name_index]:
                name = names[name_index]

        now = False
    else:
        now = True
    for location, name in zip(face_loc, names):
        top, right, bottom, left = location
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        f = cv2.rectangle(f, (left, top), (right, bottom), (255, 0, 0), 3)

        cv2.rectangle(f, (left, bottom - 15), (right, bottom), (255, 0, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(f, name, (left + 6, bottom), font, 0.5, (255, 255, 255), 1)

    cv2.imshow('Video', f)
    k = cv2.waitKey(1)

    if k & 0xFF == ord('s'):
        break

CAM.release()
cv2.destroyAllWindows()
