# -*- coding: utf-8 -*-
import cv2

import processor


class VideoCamera(object):



    def __init__(self, camId):
        self.video = None
        self.cam_id = camId





    def start_stream(self):

        print 'start'
        if self.video is None:
            self.video = cv2.VideoCapture(self.cam_id)


    def __del__(self):
        if self.video is not None:
            self.video.release()

    def stop_stream(self):
        if self.video is not None:
            self.video.release()
            self.video = None

    def get_frame(self):

        if self.video is not None:
            success, image = self.video.read()
        else:
            image = None
        return image
