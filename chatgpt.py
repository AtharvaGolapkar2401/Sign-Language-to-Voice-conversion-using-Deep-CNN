import tkinter as tk
import cv2
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry('640x480')

# Create a label for displaying the video feed
label = tk.Label(root)
label.pack()

# Open the default camera
cap = cv2.VideoCapture(0)

# Define a function to capture frames from the camera and display them in the label
def show_frame():
    # Capture a frame from the camera
    ret, frame = cap.read()
    # Convert the frame from BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Convert the frame to a PIL Image object
    image = Image.fromarray(frame)
    # Convert the PIL Image object to a Tkinter PhotoImage object
    photo = ImageTk.PhotoImage(image)
    # Set the photo to the label
    label.config(image=photo)
    label.image = photo
    # Call the show_frame() function again after 10 milliseconds
    root.after(10, show_frame)

# Call the show_frame() function to start the video feed
show_frame()

root.mainloop()

# Release the camera and close the window when the window is closed
cap.release()
cv2.destroyAllWindows()
