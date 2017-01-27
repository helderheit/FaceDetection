# -*- coding: utf-8 -*-
import cv2

import processor


class VideoCamera(object):


    def __init__(self):
        self.video = None


    def start_stream(self):
        if self.video is None:
          self.video = cv2.VideoCapture(0)


    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        return image
