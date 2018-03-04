import cognitive_face as CF
import imageio
import asyncio
import functools
import argparse

class CrowdEmotion:
  
  # returns the current emotional state of the crowd
  def getCurrentEmotion(self):
    return self.emotion

  # takes a filepath to an image, calls CF API on the
  # image, and then sets the emotional state 
  def processEmotion(self, filename):
    return

  def __init__(self):
    self.key = '51fae3a010d1498d95a008972adb3547'
    # set api key
    CF.Key.set(self.key) 
    # initialize the emotion object
    self.emotion = None
