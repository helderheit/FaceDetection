# -*- coding: utf-8 -*-
"""
Modul filters

Dieses Modul beeinhaltet alle Filter, die die Gesichts- und Augenposition NICHT
benötigen.

Die Filter liegen als Funktionen vor. Diese erhalten ein OpenCV-Bild image als  Paramenter.

Die Funktionen geben jeweils ein OpenCV Bild zurück das den angewendeten Filter
beeinhaltet.

+++WICHTIG+++
Im Docstring finden sich der im User-Interface angezeigte Name der Funktion sowie der Dateiname(mit Endung) des
Vorschaubildes, durch Komma getrennt. Filter ohne Docstring werden nicht dargestellt.

"""
import cv2
import numpy as np

def filter_gray(image):
    """Black&White, black-white.png"""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def filter_negative(image):
    """Thermo, negative.png"""
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

def filter_split(image):
    """Quadro, split.png"""
    height, width = image.shape[:2]
    height_2 = height/2
    width_2 = width/2
    #blank_image: "http://stackoverflow.com/questions/12881926/create-a-new-rgb-opencv-image-using-python"
    blank_image = np.zeros((height, width, 3), np.uint8)
    #resize: "http://docs.opencv.org/trunk/da/d6e/tutorial_py_geometric_transformations.html"
    small = cv2.resize(image, (width_2, height_2), interpolation = cv2.INTER_CUBIC)
    blank_image[0:height_2, 0:width_2] = small
    blank_image[height_2:height, 0:width_2] = small
    blank_image[0:height_2, width_2:width] = small
    blank_image[height_2:height, width_2:width] = small
    return blank_image