import cv2

cam = cv2.VideoCapture(0)

cv2.namedWindow = "test"


def capture():
    count = 0
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print('error')
            break
        if count >= 60:
            return frame
        count += 1


if __name__ == "__main__":
    f = capture()
    cv2.imshow('test', f)
    cv2.waitKey(0)
