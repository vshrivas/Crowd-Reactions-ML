import cognitive_face as CF
import imageio
import asyncio
import functools
import argparse

class CrowdEmotion:
  

  def __init__(self):
    self.key = '51fae3a010d1498d95a008972adb3547'
    # set api key
    CF.Key.set(self.key) 
    
