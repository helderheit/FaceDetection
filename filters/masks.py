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


Die Funktionen geben jeweils ein OpenCV Bild zurück das den angewendeten Filter
beeinhaltet.
"""


import cv2



"""
Rahmen um Gesicht und Augen

Augenmittelpunkte markiert

"""
def mask_debug(image,x,y,w,h,eye1,eye2):
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    e1x, e1y, e1w, e1h = eye1
    e2x, e2y, e2w, e2h = eye2

    cv2.rectangle(image, (x+e1x, y+e1y), (x+e1x + e1w, y+e1y + e1h), (0, 255, 0), 2)
    cv2.rectangle(image, (x+e2x, y+e2y), (x+e2x + e2w, y+e2y + e2h), (0, 255, 0), 2)

    e1centerx = x+e1x + e1w / 2
    e1centery = y+ e1y + e1h / 2


    e2centerx = x + e2x + e1w / 2
    e2centery = y + e2y + e1h / 2

    cv2.rectangle(image, (e1centerx-1, e1centery-1), (e1centerx + 2, e1centery + 2), (0, 255, 255), 2)
    cv2.rectangle(image, (e2centerx-1, e2centery-1), (e2centerx + 2, e2centery + 2), (0, 255, 255), 2)


    return image


"""
Schwarze Balken vor den Augen

"""
def mask_censor_bar(image,x,y,w,h,eye1,eye2):

    centerx = x+w/2
    centery = y + h/2

    e1x, e1y, e1w, e1h = eye1
    e2x, e2y, e2w, e2h = eye2

    e1centerx = x+e1x + e1w / 2
    e1centery = y+ e1y + e1h / 2


    e2centerx = x + e2x + e1w / 2
    e2centery = y + e2y + e1h / 2


    cv2.rectangle(image, (e1centerx-20, e1centery-20), (e2centerx+40, e2centery+40 ), (0, 0, 0),-1)
    #cv2.rectangle(image, (e2centerx, e2centery), (e2centerx + 2, e2centery + 2), (0, 255, 255), 2)


    return image
