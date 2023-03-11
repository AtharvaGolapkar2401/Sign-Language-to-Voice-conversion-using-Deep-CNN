import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.geometry("900x700")
root.configure(bg="white")
Label(root, text="atharva trial cam").pack
f1 = LabelFrame(root, bg="red")
f1.pack()
L1 = Label(f1, bg="red")
L1.pack()

cap = cv2.VideoCapture(0)

while True:
    img = cap.read()[1]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(Image.fromarray(img))
    L1['image'] = img
    root.update()