import time

import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

offset = 20
imgsize = 300
counter = 0
folder1 = 'data2/single'
folder2 = 'data2/return'
folder3 = 'data2/repeat'

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgsize, imgsize, 3), np.uint8)*255
        imgCrop = img[y-offset:y+h+offset, x-offset:x+w+offset]

        imgCropShape = imgCrop.shape

        aspectRatio = h/w

        if aspectRatio > 1:
            k = imgsize/h
            wCal = math.ceil(k*w)
            imgResize = cv2.resize(imgCrop, (wCal, imgsize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgsize-wCal)/2)
            imgWhite[:, wGap:wCal+wGap] = imgResize

        else:
            k = imgsize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgsize, hCal), interpolation = cv2.INTER_AREA)
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgsize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize

        cv2.imshow("IMAGECROP", imgCrop)
        cv2.imshow("IMAGEWHITE", imgWhite)

    cv2.imshow("IMAGE", img)
    key = cv2.waitKey(1)
    if key == ord("1"):
        counter += 1
        cv2.imwrite(f'{folder1}/Image_{time.time()}.jpg', imgWhite)
        print(counter)

    elif key == ord("2"):
        counter += 1
        cv2.imwrite(f'{folder2}/Image_{time.time()}.jpg', imgWhite)
        print(counter)

    elif key == ord("3"):
        counter += 1
        cv2.imwrite(f'{folder3}/Image_{time.time()}.jpg', imgWhite)
        print(counter)

    elif key & 0xFF == 27: # esc key
        break

cap.release()
cv2.destroyAllWindows()