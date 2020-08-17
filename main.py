import os
import sys
import subprocess
import capture
import cv2 as cv
import face_recognition

CAM = cv.VideoCapture(0)
cv.namedWindow = 'test'
matches = []
face_loc = []
images = []

commands = sys.argv[1:]

for r, directory, file in os.walk('./images'):
    images = file

print(images)


def store_new_image():
    for root, directories, files in os.walk('.'):
        if "images" in directories:
            break
        else:
            subprocess.call("mkdir images", shell=True)
            break

    name = input("Enter your first name: ")
    frame = capture.capture()
    cv.imwrite(f"images/{name}.png", frame)


original_commands = {'str_n_img': store_new_image, 'sni': store_new_image}

for command in commands:
    if original_commands.get(command) is not None:
        original_commands[command]()

print(face_recognition.face_encodings(face_recognition.load_image_file(f"images/Binod.png")))

encodings = [face_recognition.face_encodings(face_recognition.load_image_file(f"images/{encoding}"))[0]
             for encoding in images]

names = [name.rstrip('.png') for name in images]


now = True

while True:
    ret, f = CAM.read()

    if not ret:
        break

    temp_frame = cv.resize(f, (0, 0), fx=0.25, fy=0.25)
    temp_frame = temp_frame[:, :, ::-1]

    if now:
        face_loc = face_recognition.face_locations(temp_frame)
        face_encodings = face_recognition.face_encodings(temp_frame, face_loc)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(encodings, face_encoding)
            name = 'N/A'
            face_distances = face_recognition.face_distance(encodings, face_encoding)

            print(matches)
        now = False
    else:
        now = True
    for location, match in zip(face_loc, matches):
        top, right, bottom, left = location
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        name = 'N/A'

        if match is not None and match:
            name = names[matches.index(match)]

        f = cv.rectangle(f, (left, top), (right, bottom), (255, 0, 0), 3)

        cv.rectangle(f, (left, bottom - 15), (right, bottom), (255, 0, 0), cv.FILLED)
        font = cv.FONT_HERSHEY_DUPLEX
        cv.putText(f, name, (left + 6, bottom), font, 0.65, (255, 255, 255), 1)

    cv.imshow('', f)
    k = cv.waitKey(1)

    if k % 256 == ord('s'):
        break

CAM.release()
cv.destroyAllWindows()
