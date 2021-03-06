import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from videoStream import VideoStreamThread
from crowdEmotion import CrowdEmotion
import time
import matplotlib
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style
import numpy as np

# establish backend and settings for matplotlib
matplotlib.use("TkAgg")
style.use('ggplot')

class Application: 

  def __init__(self,master, width, height): 

      # the parent window
      self.master = master;
    
      # the thread running the video stream; initially set to None
      self.videoThread = None;
      
      # create all of the main containers

      # the control panel
      self.control_panel = tk.Frame(master, bg = 'white', width = width, height = 100)
      self.control_panel.grid(row = 0, columnspan = 6)
      self.control_panel.grid_propagate(0)

      # the video display
      self.video_display = tk.Frame(master, width = width/2, height = height - 100)
      self.video_display.grid(row = 1, columnspan = 3)
      self.video_display.grid_propagate(0)
      
      # the graph display 
      self.graph = tk.Frame(master, bg = 'red', width = width/2, height = height - 100)
      self.graph.grid(row = 1, column = 3, columnspan = 3)
      self.graph.grid_propagate(0)

      # create the widgets on the control panel
      self.buildControlPanel(self.control_panel)

      # create the crowdEmotion object
      self.crowdEmotion = CrowdEmotion()
 
      # set up the graph display frame so that it shows us a graph
      self.buildGraphDisplay(self.graph)
      
      # set up the video display frame so that it can actually play video
      self.buildVideoDisplay(self.video_display)
      self.videoStream = VideoStreamThread(self.video_label, self.crowdEmotion)
      self.videoPlaying = False

      # variables to store the graph 
      self.graph_canvas = None
      self.a = None

      # enable live udpates of the graph
      self.graphAnimation = animation.FuncAnimation(self.figure, self.animateGraph, \
          interval = 1000)

  # quits the application 
  def quit(self):

    # stop the video stream if there is one
    if(self.videoStream != None):
      self.videoStream.stopStream() 

    # stop the GUI
    self.master.destroy()
    print("[INFO] Successfully exited application.")


  # stops an existing video stream if one exists
  def stopVideoStream(self):

    # is a no-op if the current video thread doesn't exist
    if(self.videoStream == None):
      return
    print("[INFO] Signalling to existing video stream to stop.")
    self.videoStream.stopStream()
    self.videoStream = None


  # starts the live camera feed
  def start_cam(self): 
    print("[INFO] Starting camera feed. You will need a webcam.")
    self.videoStream.setSource(0)
    self.videoPlaying = True


  # open a video file 
  def open_video(self):
    print("[INFO] Opening file.")
    filename = askopenfilename()

    # do nothing if a filename isn't selected
    if (filename == '' or not isinstance(filename, str)):
      print("[WARN] No file selected.")
      return
    print("[INFO] Filename being opened: " + filename)
    self.videoStream.setSource(filename)
    self.videoPlaying = True


  # create the control panel widgets  
  def buildControlPanel(self, master):

    # configure the rows and columns of this panel to have weight
    for x in range(5):
      master.columnconfigure(x, weight = 1)
 
    # the close button
    self.close_button = ttk.Button(master, text = "Close")
    self.close_button.configure(command = lambda: self.quit())
    self.close_button.grid(row = 0, column = 5)

    # the camera source button
    self.camera_button = ttk.Button(master, text = "Activate Camera")
    self.camera_button.configure(command = lambda: self.start_cam())
    self.camera_button.grid(row = 0, column = 2) 

    # button to select a file
    self.file_path_button = ttk.Button(master, text = "Select a Video")
    self.file_path_button.configure(command = lambda: self.open_video())
    self.file_path_button.grid(row = 0, column = 0)


  # initialize a label object inside the video display to allow video 
  # streaming capability
  def buildVideoDisplay(self, master):

    # give weight to the rows and columns of this display 
    for x in range(5): 
      master.columnconfigure(x, weight = 1)
    master.rowconfigure(0, weight = 1)
    self.video_label = tk.Label(master)
    self.video_label.grid(row = 0, columnspan = 6, sticky = "nesw")


  # initialize a basic graph in the graph display
  def buildGraphDisplay(self, master):

    # give weight to the rows and columns of this display
    master.rowconfigure(0, weight = 1)
    master.columnconfigure(0, weight = 1)
    f = Figure(figsize = (6,6), dpi = 100)
    a = f.add_axes([0.1,0.2, 0.8, 0.7])
    self.subplot = a
    self.figure = f
    canvas = FigureCanvasTkAgg(f, master)
    self.graph_canvas = canvas
    canvas.show()
    canvas.get_tk_widget().grid(row = 0, column = 0)

  def animateGraph(self, i):
    emotionList = ['anger', 'contempt', 'disgust', 'fear', \
     'happiness', 'neutral', 'sadness', 'surprise']

    # clear the old graph lines
    self.subplot.clear()

    # plot the new emotion values
    for i in range(len(self.crowdEmotion.emotions_time)):
      emotion = self.crowdEmotion.emotions_time[i]
      if emotion != []:
        if (len (emotion) == 1):
          emotion.append(0.0)
        x_axis = np.linspace(1, len(emotion), num = len(emotion))
        self.subplot.set_title("Crowd Emotion Over Time")
        self.subplot.plot(x_axis, emotion, label = emotionList[i])
        self.subplot.legend(bbox_to_anchor=(0, -0.1), loc=2, ncol = int(len(emotionList)/2), borderaxespad=0.)
      elif self.videoPlaying:
        print("[WARN] Emotion not detected in video.")
