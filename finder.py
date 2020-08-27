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
now = True

while True:
    ret, f = CAM.read()

    if not ret:
        break

    temp_frame = cv.resize(f, (0, 0), fx=0.25, fy=0.25)
    temp_frame = temp_frame[:, :, ::-1]

    if now:
        face_loc = face_recognition.face_locations(temp_frame)
        now = False
    else:
        now = True
    for location in face_loc:
        top, right, bottom, left = location
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4


        f = cv.rectangle(f, (left, top), (right, bottom), (255, 0, 0), 3)

    cv.imshow('', f)
    k = cv.waitKey(1)

    if k % 256 == ord('s'):
        break

CAM.release()
cv.destroyAllWindows()
