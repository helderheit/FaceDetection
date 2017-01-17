#Module fuer Filter
import cv2

def filter_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def filter_negative(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)