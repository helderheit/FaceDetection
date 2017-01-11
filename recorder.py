import cv2

import processor


class VideoCamera(object):


    def __init__(self):

        self.video = cv2.VideoCapture(0)


    def __del__(self):
        self.video.release()

    def get_frame(self, black):
        success, image = self.video.read()

        image = processor.process_image(image)

        ret, jpeg = cv2.imencode('.jpg', image, [0])
        return jpeg.tobytes()



