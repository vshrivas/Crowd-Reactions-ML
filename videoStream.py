import threading
import imageio
import tkinter as tk
from PIL import Image, ImageTk
import cv2

# plays a video in a tkinter Label object 
def videoStream(label, filename):
  # load the video from the file system
  video = imageio.get_reader(filename)

  print("[INFO] Loaded video successfully. Beginning stream.")  

  # loop through each frame in the video
  for frame in video.iter_data():
    # convert the frame into a tkinter compatible image
    frame_image = ImageTk.PhotoImage(Image.fromarray(frame))
    # load the frame into the provided label
    label.config(image = frame_image)
    label.image = frame_image

# start a thread that runs the video stream
def startVideoStream(label, filename):
  print("[INFO] Starting video stream.")
  thread = threading.Thread(target = videoStream, args = (label, filename))
  thread.daemon = 1;
  thread.start()
  return thread

# plays the camera feed in a tkinter Label object
def cameraStream(label):
  while True:
    # capture the camera frame
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    frame_image = ImageTk.PhotoImage(Image.fromarray(frame))
    # load the frame into the tkinter label
    label.config(image = frame_image)
    label.image = frame_image

# starts a thread that runs the camera stream
def startCameraStream(label):
  print("[INFO] Starting camera stream.")
  thread = threading.Thread(target = cameraStream, args = (label))
  thread.daemon = 1
  thread.start()
  return thread
