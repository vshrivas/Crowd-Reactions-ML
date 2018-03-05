import cognitive_face as CF
import imageio
import asyncio
import functools
import argparse
import constants
import numpy as np 
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class CrowdEmotion:
  
  def __init__(self, subplot, canvas):
    # set api key
    CF.Key.set(constants.CF_KEY) 
    # initialize the emotion objects
    self.emotion = None
    self.agg_emotions = None
    self.emotions_time = [[], [], [], [], [], [], [], []]
    self.subplot = subplot
    self.canvas = canvas

  # returns the current emotional state of the crowd
  def getCurrentEmotion(self):
    return self.emotion

  # takes a filepath to an image, calls CF API on the
  # image, and then sets the emotional state. Also returns
  # the emotions. Note that there could be several people in the 
  # crowd, so we want to average each emotion over the number of 
  # people
  def processEmotion(self, filename):
    
    # The emotion values of anger, contempt, disgust, fear, 
    # happiness, neutral, sadness, and surprise respectively 
    agg_emotions = [0, 0, 0, 0, 0, 0, 0, 0]
    num_faces = 0
    result = CF.face.detect(filename, attributes = 'emotion')
    try: 
      for face in result: 
        emotion = face['faceAttributes']['emotion']
        agg_emotions[0] += emotion['anger']
        agg_emotions[1] += emotion['contempt']
        agg_emotions[2] += emotion['disgust']
        agg_emotions[3] += emotion['fear']
        agg_emotions[4] += emotion['happiness']
        agg_emotions[5] += emotion['neutral']
        agg_emotions[6] += emotion['sadness']
        agg_emotions[7] += emotion['surprise']
        num_faces += 1
        self.emotion = emotion

      if num_faces == 0:
        return None
      for i in range(len(agg_emotions)):
        agg_emotions[i] /= num_faces

      self.agg_emotions = agg_emotions
      if self.agg_emotions != None:
        for i in range(len(self.agg_emotions)):
          self.emotions_time[i].append(self.agg_emotions[i])

      return agg_emotions

    except not result:
      return None

  def graphEmotion(self):
    print("[INFO] Updating graph.")
    for emotion in self.emotions_time:
      # TODO: instead of 100, use the time that the video ends
      if emotion != []:
        if(len(emotion) == 1):
          emotion.append(0.0)
        y_axis = np.linspace(0,100, num=len(emotion))
        self.subplot.plot(emotion, y_axis)
        # TODO: we need to scale the x and y axes to match this
        # data range, otherwise it won't graph 
        self.canvas.draw()
      else:
        print("[INFO] Emotion not detected in video.")

      self.canvas.show()
      self.canvas.get_tk_widget().grid(row = 0, column = 0)
