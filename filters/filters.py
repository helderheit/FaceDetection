# -*- coding: utf-8 -*-
"""
Modul filters

Dieses Modul beeinhaltet alle Filter, die die Gesichts- und Augenposition NICHT
benötigen.

Die Filter liegen als Funktionen vor. Diese erhalten ein OpenCV-Bild image als  Paramenter.
*args: Weitere filterspezifische Parameter

Die Funktionen geben jeweils ein OpenCV Bild zurück das den angewendeten Filter
beeinhaltet.

+++WICHTIG+++
Im Docstring finden sich zeileweise jeweils ein möglicher Parameter, der im User-Interface angezeigte Name der Funktion sowie der Dateiname(mit Endung) des
Vorschaubildes, durch Komma getrennt. Filter ohne Docstring werden nicht dargestellt.



"""
import cv2
import numpy as np


#Images die von Anfang an geladen werden

frame_image = cv2.imread('filters/filters/rahmen.png')


def filter_gray(image, * args):
    """, Black&White, black-white.png"""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def filter_negative(image, *args):
    """, Thermo, negative.png"""
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

def filter_split(image, *args):
    """, Quadro, split.png"""
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

def filter_sepia(image):
    """, Sepia, sepia.png"""
    kernel = np.asmatrix([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]) #Kernel-Werte von http://amin-ahmadi.com/2016/03/24/sepia-filter-opencv/
    image = cv2.transform(image, kernel)
    return image

def filter_country(image, *args):
    """ger, Germany, germany.png
    fra, France, france.png"""

    if args[0] == "ger":
        height, width = image.shape[:2]
        height_3 = height/3
        height_2 = height_3*2
        blank_image = np.zeros((height, width, 3), np.uint8)
        cv2.rectangle(blank_image, (0, 0), (width, height_3), (0, 0, 0), -1, 8, 0)
        cv2.rectangle(blank_image, (0, height_3), (width, height_2), (0, 0, 255), -1, 8, 0)
        cv2.rectangle(blank_image, (0, height_2), (width, height), (0, 255, 255), -1, 8, 0)
        result = cv2.addWeighted(image, 0.5, blank_image, 0.5, 0)
        return result
    else:
        height, width = image.shape[:2]
        width_3 = width / 3
        width_2 = width_3 * 2
        blank_image = np.zeros((height, width, 3), np.uint8)
        cv2.rectangle(blank_image, (0, 0), (width_3, height), (255, 0, 0), -1, 8, 0)
        cv2.rectangle(blank_image, (width_3, 0), (width_2, height), (255, 255, 255), -1, 8, 0)
        cv2.rectangle(blank_image, (width_2, 0), (width, height), (0, 0, 255), -1, 8, 0)
        result = cv2.addWeighted(image, 0.5, blank_image, 0.5, 0)
        return result

def filter_frame(image, *args):
    """, Frame, frame.png"""
    height, width = image.shape[:2]
    h10 = height/10
    w10 = width/10
    newImage = image.copy()
    img1 = frame_image
    res1 = cv2.resize(img1,(width, height), interpolation = cv2.INTER_CUBIC)
    res2 = cv2.resize(newImage, (width-(2*w10), height-(2*h10)-(h10/3)), interpolation = cv2.INTER_CUBIC)
    blank_image = np.zeros((height, width, 3), np.uint8)
    blank_image[0:width, 0:height+160] = res1
    blank_image[(h10+h10/3):height-h10, w10:width-w10] = res2
    return blank_image

"""
Fügt ein Univerität Regensburg Wasserzeichen hinzu
"""

def filter_watermark(image, *args):
    """, Wasserzeichen, watermark.png"""
    watermark = cv2.imread('filters/masks/watermark.jpeg')

    watermark = cv2.resize(watermark, (image.shape[1], image.shape[0]))

    return cv2.addWeighted(image, 0.85, watermark, 0.15, cv2.INTER_AREA)



def filter_lut(image, *args):

    image = image*(image*0.1)

    return image
