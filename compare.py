import face_recognition
import os
import shutil
known_image = face_recognition.load_image_file("known_image.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

folder = '.'
files = os.listdir(folder)
sorted_images = 'sorted_images'
if sorted_images not in files:
    os.mkdir(sorted_images)

for file in files:
    unknown_image = face_recognition.load_image_file(os.path.join(folder, file))
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    result = face_recognition.compare_faces([known_encoding], unknown_encoding)
    if result:
        shutil.move(os.path.join(folder, file), os.path.join(sorted_images, file))
