#Module fuer Filter
import cv2

def filter_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def filter_negative(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#http://stackoverflow.com/questions/4195453/how-to-resize-an-image-with-opencv2-0-and-python2-6
#http://stackoverflow.com/questions/19098104/python-opencv2-cv2-wrapper-get-image-size
def filter_split(image):
	height, width = image.shape[:2]
	height_2 = height/2
	width_2 = width/2
	small = cv2.resize(image, (height_2, width_2))
	image[0:height_2, 0:width_2] = small
	image[0:height_2, width_2:width] = small