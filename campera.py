import time
import cv2
import numpy as np
from imutils.video.pivideostream import PiVideoStream


class VideoCamera(object):
    def __init__(self, flip = False):
        self.vs = PiVideoStream().start()
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

class NormalCamera(object):
    def __init__(self, flip=False):
        self.vs = cv2.VideoStream(0)
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def get_frame(self):
        frame = self.vs.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
