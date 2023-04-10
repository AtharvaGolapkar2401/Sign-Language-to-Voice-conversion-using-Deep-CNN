import tkinter as tk
import tkinter
from tkinter.ttk import *

import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
from cvzone.ClassificationModule import Classifier
import pyttsx3
from playsound import playsound
from tkinter import *
from PIL import Image, ImageTk
import speech_recognition as sr
r = sr.Recognizer()

engine = pyttsx3.init()
voices = pyttsx3.init().getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)
# print(voices[1].id)

def station_name(fname):
    incoming_text = fname

root = Tk()
root.geometry("503x550")
root.configure(bg="white")
#button style
style = Style()

style.configure('TButton', font=
('calibri', 20, 'bold'),
                borderwidth='4')

# Changes will be reflected
# by the movement of mouse.
style.map('TButton', foreground=[('active', '!disabled', 'green')],
          background=[('active', 'black')])


# Label(root, text="atharva trial cam").grid()
f1 = LabelFrame(root, bg="red")
f1.grid(row=0, column=0)
f2 = LabelFrame(root, bg="yellow")
L1 = Label(f1, bg="red", height="300", width="500")
L1.grid(row=0, column=0, rowspan=1, columnspan=1)


incoming_text = tkinter.StringVar()
incoming_text.set("Predicted Text is displayed here")

def station(fname):
    incoming_text.set(fname)
L2 = Label(root, textvariable=incoming_text, bg="black", fg="white", font=("comicsansms", 15, "bold"))
L2.grid(row=1,column=0)


def getvals():
     amount = amountVal.get()
     engine.say("Rupees"+amount)
     engine.runAndWait()


def getvals1():
    amt = amountVal.get()
    if (amt == "thane"):
        playsound('thane.mp3')
    elif(amt == "bandra"):
        playsound('bandra.mp3')
    elif (amt == "ghatkopar" or amt == "dadar"):
        playsound('ghatkopar.mp3')
    engine.runAndWait()


def getvals2():
        am = amountVal.get()
        engine.say(am + "via")
        engine.runAndWait()

def speak():
    while True:
        counter = 1
        with sr.Microphone() as source:
                #clear the bg noise
                r.adjust_for_ambient_noise(source, duration=0.3)
                print("Speak now")
                # capture the audio
                audio = r.listen(source)
                try:
                    if (counter == 1):
                            text = r.recognize_google(audio)
                            station(text)
                            break
                            counter = 0
                except:
                    print("Please say again!!")


# Create style Object
style = Style()

style.configure('TButton', font=
('calibri', 20, 'bold'),
                borderwidth='4')

# Changes will be reflected
# by the movement of mouse.
style.map('TButton', foreground=[('active', '!disabled', 'green')],
          background=[('active', 'black')])



amountVal = StringVar()
amount_label=  tk.Label(root,text="Input").grid(row=3,column=0)

amountentry = Entry(root, text="submit!", fg = 'black',bg = 'yellow', textvariable=amountVal, width=30, borderwidth=3, relief="ridge")
amountentry.grid(row=3,column=0, padx=100, pady=10)
btn = Button(root,text="submit", command=getvals).grid(row=4,column=0, pady = 10, padx = 100)
btn = Button(text="Via which Station", command=getvals1).grid(row=5,column=0,pady = 10, padx = 100)

btn = Button(root, text= "Speak", command=speak).grid(row=6,column=0, pady =10,padx=100)
#----------------------------------------#
#project wala opencv



cap = cv2.VideoCapture(0)


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




class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Page 1")
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text="Go to Page 2", command=lambda: controller.show_frame(Page2))
        button1.pack()


class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Page 2")
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text="Go to Page 1", command=lambda: controller.show_frame(Page1))
        button1.pack()
        while True:
            success, img = cap.read()
            imgOutput = img.copy()
            hands, img = detector.findHands(img)
            image = cap.read()[1]
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = ImageTk.PhotoImage(Image.fromarray(image))
            L1['image'] = image
            root.update()

            if hands:
                hand = hands[0]
                x, y, w, h = hand['bbox']

                imgWhite = np.ones((imgsize, imgsize, 3), np.uint8) * 255
                imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

                imgCropShape = imgCrop.shape

                aspectRatio = h / w

                if aspectRatio > 1:
                    k = imgsize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgsize))
                    imgResizeShape = imgResize.shape
                    wGap = math.ceil((imgsize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
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
                # blank_image[:] = (0, 0, 0)
                # cv2.putText(blank_image,labels[index], (100,80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)
                # cv2.imshow('3 Channel Window', blank_image)
                # cv2.imshow("IMAGECROP", imgCrop)
                # cv2.imshow("IMAGEWHITE", imgWhite)
                # cv2.imshow("Output", imgOutput)

                if labels[index] == "single":
                    hii_counter += 1
                    if (hii_counter >= 5):
                        playsound('single.mp3')
                        hii_counter = 0

                elif labels[index] == "return":
                    hii_counter += 1
                    if (hii_counter >= 5):
                        playsound('return.mp3')
                        hii_counter = 0

                elif labels[index] == "repeat":
                    hii_counter += 1
                    if (hii_counter >= 5):
                        playsound('repeat.mp3')
                        hii_counter = 0

            # cv2.imshow("IMAGE", imgOutput)
            # key = cv2.waitKey(1)

            # if key & 0xFF == 27: # esc key
            #     break

            # with sr.Microphone() as source:
            #     # clear the bg noise
            #     r.adjust_for_ambient_noise(source, duration=0.3)
            #     print("Speak now")
            #     # capture the audio
            #     audio = r.listen(source)
            #     try:
            #         text = r.recognize_google(audio)
            #         print(text)
            #     except:
            #         print("Please say again!!")


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Page1, Page2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Page1)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


app = MainApplication()
app.mainloop()

cap.release()
cv2.destroyAllWindows()