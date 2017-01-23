# -*- coding: utf-8 -*-
import cv2
from filters import filters
from filters import masks








def process_image(image):

    #Maskenaufruf erfolgt in detect_faces(image)
    image = detect_faces(image)

    #Filteraufruf hier
    #image = filters.filter_frame(image)
    return image


"""
Funktion zur Gesichtserkennung

Paramenter OPenCV Bild image: das Rohbild

Rückgabe OpenCV Bild mit angewendeten Masken

"""

def detect_faces(image):
    face_cascade = cv2.CascadeClassifier(
        'haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(
        'haarcascades/haarcascade_eye.xml')

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        #cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = image[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3)

        number = 0
        eyeCoordinates = []

        for (ex, ey, ew, eh) in eyes:
            number +=1
            if(number <3):
                eyeCoordinates.append((ex, ey, ew, eh))
            #cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        #Masken werden nur aufgerufen wenn zwei Augen detektiert wurden
        if(number >1):

            #linkes und rechtes Auge richtig anordnen
            e1x, e1y, e1w, e1h =  eyeCoordinates[0]
            e2x, e2y, e2w, e2h = eyeCoordinates[1]

            if e1x > e2x:
                temp = eyeCoordinates[0]
                eyeCoordinates[0] = eyeCoordinates[1]
                eyeCoordinates[1] = temp
                e1x, e1y, e1w, e1h = eyeCoordinates[0]
                e2x, e2y, e2w, e2h = eyeCoordinates[1]


            #Maskenaufruf hier
            image = masks.mask_censor_bar(image, x,y,w,h, eyeCoordinates[0], eyeCoordinates[1],'Brille2')

    return image
