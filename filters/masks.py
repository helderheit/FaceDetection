# -*- coding: utf-8 -*-
"""
Modul masks

Dieses Modul beeinhaltet alle Filter, die die Gesichts- und Augenposition
benötigen.

Die Filter liegen als Funktionen vor. Diese erhalten folgenden Paramenter in der
vorgegebenen Reihenfolge.

OpenCV Bild image: das Rohbild
int x:  x-Position linke obere Ecke des Rahmens um das Gesicht
int y:  y-Position linke obere Ecke des Gesichts um das Gesicht
int w:  Breite des Rahmens um das Gesicht
int h:  Höhe des Rahmens um das Gesicht
tupel (x,y,w,h) eye1: Das linke Auge, x,y,w,h equivalent zum Gesicht
tupel (x,y,w,h) eye2: Das rechte Auge, x,y,w,h equivalent zum Gesicht

*args: Weitere filterspezifische Parameter


Die Funktionen geben jeweils ein OpenCV Bild zurück das den angewendeten Filter
beeinhaltet.


+++WICHTIG+++
Im Docstring finden sich zeileweise jeweils ein möglicher Parameter, der im User-Interface angezeigte Name der Funktion sowie der Dateiname(mit Endung) des
Vorschaubildes, durch Komma getrennt. Filter ohne Docstring werden nicht dargestellt.



"""
import math

import cv2
import numpy as np

"""
    Parameters
"""

param_glasses = {}

"""
    Parameter initialisieren
"""


def initialise_masks():
    glasses_conf_file = open('filters/masks/config/glasses.conf', 'r')
    for line in glasses_conf_file:
        params = line.split(',')
        params[1] = params[1].replace(' ', '')
        for i in range(2, 6):
            params[i] = int(params[i])

        param_glasses[params[0]] = params[1:]


"""
Rahmen um Gesicht und Augen

Augenmittelpunkte markiert

"""


def mask_debug(image, x, y, w, h, eye1, eye2, *args):
    """, Debug, debug.png"""
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    e1x, e1y, e1w, e1h = eye1
    e2x, e2y, e2w, e2h = eye2

    cv2.rectangle(image, (x + e1x, y + e1y), (x + e1x + e1w, y + e1y + e1h), (0, 255, 0), 2)
    cv2.rectangle(image, (x + e2x, y + e2y), (x + e2x + e2w, y + e2y + e2h), (0, 255, 0), 2)

    e1centerx = x + e1x + e1w / 2
    e1centery = y + e1y + e1h / 2

    e2centerx = x + e2x + e1w / 2
    e2centery = y + e2y + e1h / 2

    cv2.rectangle(image, (e1centerx - 1, e1centery - 1), (e1centerx + 2, e1centery + 2), (0, 255, 255), 2)
    cv2.rectangle(image, (e2centerx - 1, e2centery - 1), (e2centerx + 2, e2centery + 2), (0, 255, 255), 2)

    return image

"""
Blurs the face
"""

def mask_blur(image, x, y, w, h, eye1, eye2, *args):
    face = image[y:y+h, x:x+w]
    face = cv2.GaussianBlur(face,(51, 51), 30)
    image[y:y+face.shape[0], x:x+face.shape[1]] = face
    return image

"""
Fügt ein Univerität Regensburg Wasserzeichen hinzu
"""

def mask_watermark(image, x, y, w, h, eye1, eye2, *args):
    watermark = cv2.imread('filters/masks/watermark.jpeg')

    watermark = cv2.resize(watermark, (image.shape[1], image.shape[0]))

    return cv2.addWeighted(image, 0.9, watermark, 0.1, cv2.INTER_AREA)


"""
Schwarze Balken vor den Augen

"""


def mask_censor_bar(image, x, y, w, h, eye1, eye2, *args):
    """, Balken, censorbar.png"""
    centerx = x + w / 2
    centery = y + h / 2

    e1x, e1y, e1w, e1h = eye1
    e2x, e2y, e2w, e2h = eye2

    e1centerx = x + e1x + e1w / 2
    e1centery = y + e1y + e1h / 2

    e2centerx = x + e2x + e1w / 2
    e2centery = y + e2y + e1h / 2

    cv2.rectangle(image, (e1centerx - w / 5, e1centery - h / 5), (e2centerx + w / 5, e2centery + h / 5), (0, 0, 0), -1)
    # cv2.rectangle(image, (e2centerx, e2centery), (e2centerx + 2, e2centery + 2), (0, 255, 255), 2)


    return image


"""
Brillen

"""


def mask_glasses(image, x, y, w, h, eye1, eye2, *args):
    """Brille, Brille, glasses1.png
    Brille2, Sonnenbrille, glasses2.png
    """
    centerx = x + w / 2
    centery = y + h / 2

    e1x, e1y, e1w, e1h = eye1
    e2x, e2y, e2w, e2h = eye2

    e1centerx = x + e1x + e1w / 2
    e1centery = y + e1y + e1h / 2

    e2centerx = x + e2x + e1w / 2
    e2centery = y + e2y + e1h / 2

    # Bildparameter laden
    params = param_glasses[args[0]]

    filename = 'filters/masks/glasses/'+params[0]
    glasses_eye_left_x = params[1]
    glasses_eye_left_y = params[2]
    glasses_eye_right_x = params[3]
    glasses_eye_right_y = params[4]


    #Overlay-Bild laden
    s_img = cv2.imread(filename, -1)

    #Overlay-Bild skalieren, rotieren undpositionieren
    eye_distance = math.sqrt(math.pow(e2centerx -e1centerx, 2) + math.pow(e2centery - e1centery,2))
    glasses_distance = glasses_eye_right_x - glasses_eye_left_x
    scale_factor =  eye_distance/(1.0*glasses_distance)

    # Skalieren http://stackoverflow.com/questions/4195453/how-to-resize-an-image-with-opencv2-0-and-python2-6
    s_img = cv2.resize(s_img,  (0,0), fx=scale_factor, fy=scale_factor)



    angle = -math.atan((e2centery -e1centery)/(e2centerx - e1centerx*1.0) )*(180/math.pi)


    # Rotation http://docs.opencv.org/trunk/da/d6e/tutorial_py_geometric_transformations.html

    rows, cols, ch = s_img.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    s_img = cv2.warpAffine(s_img, M, (cols, rows))

    center_eyes_x = int(e1centerx + (e2centerx-e1centerx)/2.0)
    center_eyes_y = int(e1centery + (e2centery - e1centery)/ 2.0)

    glasses_center_x = int(glasses_eye_left_x + (glasses_eye_right_x-glasses_eye_left_x)/2.0)*scale_factor
    glasses_center_y = int(glasses_eye_left_y + (glasses_eye_right_y - glasses_eye_left_y) / 2.0)*scale_factor

    x_offset = int(center_eyes_x- glasses_center_x)
    y_offset = int(center_eyes_y - glasses_center_y)

    # Code for Alpha-Overlay: http://stackoverflow.com/questions/14063070/overlay-a-smaller-image-on-a-larger-image-python-opencv

    for c in range(0, 3):
        image[y_offset:y_offset + s_img.shape[0], x_offset:x_offset + s_img.shape[1], c] \
            = s_img[:, :, c] * (s_img[:, :, 3] / 255.0) + image[y_offset:y_offset + s_img.shape[0],
                                                          x_offset:x_offset + s_img.shape[1], c] * (
                                                              1.0 - s_img[:, :, 3] / 255.0)


    return image
