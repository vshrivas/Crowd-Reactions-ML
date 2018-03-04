import cognitive_face as CF
import imageio
import asyncio
import functools
import argparse
import constants

class CrowdEmotion:
  
  # returns the current emotional state of the crowd
  def getCurrentEmotion(self):
    return self.emotion

  # takes a filepath to an image, calls CF API on the
  # image, and then sets the emotional state 
  def processEmotion(self, filename):
    result = CF.face.detect(filename, attributes = 'emotion')
    try: 
      for face in result: 
        emotion = face['faceAttributes']['emotion']
        # TODO: Figure out how exactly we want to aggregate this
        # emotion data
        self.emotion = emotion
    except not result:
      pass

  def __init__(self):
    # set api key
    CF.Key.set(constants.CF_KEY) 
    # initialize the emotion object
    self.emotion = None
