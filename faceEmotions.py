import argparse
from scipy.misc import imsave
import cognitive_face as CF
import cv2
import imageio
from sys import platform

def recognize(key):

  CF.Key.set(key) # set API key

  while True:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if platform.startswith('win'): # for windows we don't display video due to camera issues
      cap.release()
    imageio.imwrite('tmp.png', frame)

    result = CF.face.detect('tmp.png', attributes='emotion')
    try:
      for face in result:
        emotion = face['faceAttributes']['emotion']
        print(emotion)
        if platform == 'darwin': # for mac we display the video, face bounding box, age & gender
          rect = face['faceRectangle']
          width = rect['width']
          top = rect['top']
          height = rect['height']
          left = rect['left']
          cv2.rectangle(frame, (left, top), (left + width, top + height),
                        (0, 255, 0), 2)
          cv2.imshow('Demo', frame)

    except not result:
      continue

    except KeyboardInterrupt:
      cap.release()
      cv2.destroyAllWindows()


if __name__ == '__main__':

  recognize("51fae3a010d1498d95a008972adb3547")
