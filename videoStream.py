import threading
import imageio
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import time

# a class that maintains a video streaming thread
class VideoStreamThread: 

  # sets the video source
  def setSource(self, source):
    if(source != 0 and not isinstance(source, str)):
      print("[WARN] You tried to select an invalid video source.")
      return
    self.source = source
    self.sourceChanged = True    
    print("[INFO] Video source changed successfully.") 

  def stopStream(self):
    self.stopStreaming = True

  def streamVideo(self, label):
    if self.video == None:
      print("[WARN] No video found to stream. Doing nothing.")
      return
    print("[INFO] Beginning video stream.");
    for frame in self.video.iter_data(): 
      # stop the stream if the stopStream variable is set
      if(self.stopStreaming or self.sourceChanged):
        print("[INFO] Stopping stream from " + self.source)
        break
      # convert the frame into a tkinter compatible image
      frame_image = ImageTk.PhotoImage(Image.fromarray(frame))
      # load the frame into the provided label
      label.config(image = frame_image)
      label.image = frame_image
    
    # if we exited the loop because the source changed, just  
    # start another stream with the correct source
    if self.sourceChanged: 
      print("[INFO] Video source is now changing.")
      self.startStream(label)
 
  def streamCamera(self, label):
    print("[INFO] Beginning camera stream.")
    while True:
      # I do this in an if statement just to enable logging.
      if self.stopStreaming or self.sourceChanged: 
        print("[INFO] Stopping camera stream.")
        break
      # capture the camera frame
      cap = cv2.VideoCapture(0)
      ret, frame = cap.read()
      frame_image = ImageTk.PhotoImage(Image.fromarray(frame))
      # load the frame into the tkinter label
      label.config(image = frame_image)
      label.image = frame_image

    cap.release()
    cv2.destroyAllWindows()
    # change sources if that's why we exited the loop
    if self.sourceChanged:
      print("[INFO] Video source is now changing.")
      self.startStream(label)

  def startStream(self, label):
    # if this thread has no source, it just sleeps
    while(not self.sourceChanged):
      time.sleep(1)
    # if the source is a filename, load the video and start a 
    # video stream
    self.sourceChanged = False
    if isinstance(self.source, str):
      self.video = imageio.get_reader(self.source)
      print("[INFO] Loaded video successfully.")
      self.streamVideo(label)
    elif self.source == 0:
      self.streamCamera(label)
    else:
      print("[WARN] You selected an invalid video source. Crashing.")
      return

  # creates a video stream thread that streams to a label
  def __init__(self, label):
    # set the source of the video stream
    self.source = None
    # signal variable to indicate source change
    self.sourceChanged = False
    # state variable: true if video stream should stop entirely
    self.stopStreaming = False
    print("[INFO] Starting video stream thread.")
    self.thread = threading.Thread(target = self.startStream, args = (label,))
    self.thread.daemon = True
    self.thread.start()
