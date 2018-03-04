import threading
import imageio
import tkinter as tk
from PIL import Image, ImageTk
import cv2

# a class that maintains a video streaming thread
class VideoStreamThread: 

  def stopStream(self):
    self.stopStreaming = True

  def streamVideo(self, label, video):
    print("[INFO] Beginning video stream.");
    for frame in video.iter_data(): 
      # stop the stream if the stopStream variable is set
      if(self.stopStreaming):
        print("[INFO] Stopping stream from " + self.filename)
        break
      # convert the frame into a tkinter compatible image
      frame_image = ImageTk.PhotoImage(Image.fromarray(frame))
      # load the frame into the provided label
      label.config(image = frame_image)
      label.image = frame_image
  
  def startStream(self, label, video):
    print("[INFO] Starting video stream thread.")
    self.thread = threading.Thread(target = self.streamVideo, args = (label, video))
    self.thread.daemon = 1
    self.thread.start()
  
  # creates a video stream thread from a file to a Label
  def __init__(self, filename, label):
    self.filename = filename
    # load the video from the file system
    self.video = imageio.get_reader(filename)
    print("[INFO] Loaded video successfully.")  
    # state variable: true if video stream should stop
    self.stopStreaming = False
    # start the video stream
    self.startStream(label, self.video)
