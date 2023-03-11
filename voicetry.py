import speech_recognition as sr
r = sr.Recognizer()
from tkinter import *
root = Tk()

# width x height (limiting the gui of the project)
root.geometry("900x700")
root.title("atharva Gui")
root.minsize(900, 700)
root.maxsize(1920, 1080)
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
                            print(text)
                            break
                            counter = 0
                except:
                    print("Please say again!!")

Button(root, text= "Speak", command=speak).pack()
root.mainloop()

