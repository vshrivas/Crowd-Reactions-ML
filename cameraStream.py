import threading
import imageio
import tkinter as tk
from PIL import Image, ImageTk
import cv2

# a class that maintains a camera streaming thread
class CameraStreamThread: 
  
  def stopStream(self):
    self.stopStreaming = True

  def streamCameraFeed(self, label):
    print("[INFO] Beginning camera stream.")
    while True:
      # I do this in an if statement just to enable logging.
      if self.stopStreaming:
        print("[INFO] Stopping camera stream.")
        break
      # capture the camera frame
      cap = cv2.VideoCapture(0)
      ret, frame = cap.read()
      frame_image = ImageTk.PhotoImage(Image.fromarray(frame))
      # load the frame into the tkinter label
      label.config(image = frame_image)
      label.image = frame_image

  def startStream(self, label, video):
    print("[INFO] Starting camera stream thread.")
    self.thread = threading.Thread(target = streamCameraFeed, args = (label))
    self.thread.daemon = 1
    self.thread.start()

  # creates a camera stream thread from a file to a Label
  def __init__(self, label):
    self.stopStreaming = False
    self.startStream(label)
