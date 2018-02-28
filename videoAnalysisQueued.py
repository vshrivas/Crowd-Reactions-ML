import argparse
from scipy.misc import imsave
import cognitive_face as CF
import cv2
from sys import platform
import asyncio
import imageio
import functools

async def produce(queue):
  loop = asyncio.get_event_loop()
  while True:
    try:
      # capture a frame from the camera
      cap = cv2.VideoCapture(0)
      ret, frame = cap.read()
      if platform.startswith('win'): # for windows we don't display video due to camera issues
        cap.release()
      imageio.imwrite('tmp.png', frame)

      # await for CF api call
      result = await loop.run_in_executor(None, functools.partial(CF.face.detect, image='tmp.png', attributes='emotion'))

      # put result in queue
      await queue.put(result)

    except KeyboardInterrupt:
      cap.release()
      cv2.destroyAllWindows()

  # if queue is full, await to put in item until empty spot opens up
  await queue.put(None)


async def consume(queue):
  while True:
    # if queue is empty, waits until item is available
    item = await queue.get()
    if item is None:
      break

    # process the item
    try:
      for face in item:
        emotion = face['faceAttributes']['emotion']
        print(emotion)
        '''if platform == 'darwin': # for mac we display the video, face bounding box, age & gender
          rect = face['faceRectangle']
          width = rect['width']
          top = rect['top']
          height = rect['height']
          left = rect['left']
          cv2.rectangle(item, (left, top), (left + width, top + height), 
            (0, 255, 0), 2)
          cv2.imshow('Demo', item)'''

    except KeyboardInterrupt:
      cap.release()
      cv2.destroyAllWindows() 

def recognize(key):
  CF.Key.set(key) # set API key

  loop = asyncio.get_event_loop()
  queue = asyncio.Queue(loop=loop)
  producer = produce(queue)
  consumer = consume(queue)
  loop.run_until_complete(asyncio.gather(producer, consumer))
  loop.close()

if __name__ == '__main__':
  recognize("51fae3a010d1498d95a008972adb3547")
