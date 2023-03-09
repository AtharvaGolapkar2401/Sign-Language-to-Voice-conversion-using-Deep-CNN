import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
from cvzone.ClassificationModule import Classifier
import pyttsx3
from playsound import playsound

engine = pyttsx3.init()
voices = pyttsx3.init().getProperty('voices')
engine.setProperty('voice', voices[0].id)
# print(voices[1].id)


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras2_model.h5", "Model/labels.txt")
labels = ["repeat", "return", "single"]
offset = 20
imgsize = 300
counter = 0
folder1 = 'data2/single'
folder2 = 'data2/return'
folder3 = 'data2/repeat'
height = 100
width = 300
blank_image = np.zeros((height, width, 3), np.uint8)
hii_counter = 0

while True:
    success, img = cap.read()
    imgOutput = img.copy()
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
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
            print(prediction, index)

        else:
            k = imgsize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgsize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgsize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
        # cv2.rectangle(imgOutput, (x - offset, y - offset - 50), (x - offset + 250, y - offset - 50 + 50), (255,0,255), cv2.FILLED)
        # cv2.putText(imgOutput, labels[index], (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)
        # cv2.rectangle(imgOutput, (x - offset, y - 10 ), (x + w + offset, y + h + offset), (255,0,255), 4)
        blank_image[:] = (0, 0, 0)
        cv2.putText(blank_image,labels[index], (100,80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)
        cv2.imshow('3 Channel Window', blank_image)
        cv2.imshow("IMAGECROP", imgCrop)
        cv2.imshow("IMAGEWHITE", imgWhite)
        # cv2.imshow("Output", imgOutput)

        if labels[index] == "single":
            hii_counter += 1
            if(hii_counter >= 5):
                playsound('single.mp3')
                hii_counter = -5

        elif labels[index] == "return":
            hii_counter += 1
            if(hii_counter >= 5):
                playsound('return.mp3')
                hii_counter = -5

        elif labels[index] == "repeat":
            hii_counter += 1
            if(hii_counter >= 5):
                playsound('repeat.mp3')
                hii_counter = -5

    cv2.imshow("IMAGE", imgOutput)
    key = cv2.waitKey(1)

    if key & 0xFF == 27: # esc key
        break

cap.release()
cv2.destroyAllWindows()
