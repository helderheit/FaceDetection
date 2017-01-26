# -*- coding: utf-8 -*-
import cv2
from filters import filters
from filters import masks








def process_image(image, filter_function, filter_args, mask_function, mask_args):

    #Maskenaufruf erfolgt in detect_faces(image, mask_function, mask_args)
    if mask_function is not None:
        image = detect_faces(image, mask_function, mask_args)

    #Filteraufruf hier
    if filter_function is not None:

        image = filter_function(image, mask_args)
    return image


"""
Funktion zur Gesichtserkennung

Paramenter OPenCV Bild image: das Rohbild

Rückgabe OpenCV Bild mit angewendeten Masken

"""




def detect_faces(image, mask_function, mask_args):
    face_cascade = cv2.CascadeClassifier(
        'haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(
        'haarcascades/haarcascade_eye.xml')


    scale_factor = 0.5
    processimage = cv2.resize(image, (0, 0), fx=scale_factor, fy=scale_factor)
    gray = cv2.cvtColor(processimage, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        #cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]

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

            x = int(x*(1/scale_factor))
            y = int(y * (1 / scale_factor))
            w = int(w * (1 / scale_factor))
            h = int(h * (1 / scale_factor))

            #linkes und rechtes Auge richtig anordnen


            e1x, e1y, e1w, e1h =  eyeCoordinates[0]
            e2x, e2y, e2w, e2h = eyeCoordinates[1]

            e1x = int(e1x*(1/scale_factor))
            e1y = int(e1y * (1 / scale_factor))
            e1w = int(e1w * (1 / scale_factor))
            e1h = int(e1h * (1 / scale_factor))

            e2x = int(e2x * (1 / scale_factor))
            e2y= int(e2y * (1 / scale_factor))
            e2w = int(e2w * (1 / scale_factor))
            e2h = int(e2h * (1 / scale_factor))

            eyeCoordinates[0] = (e1x, e1y, e1w, e1h)
            eyeCoordinates[1] = (e2x, e2y, e2w, e2h)


            if e1x > e2x:
                temp = eyeCoordinates[0]
                eyeCoordinates[0] = eyeCoordinates[1]
                eyeCoordinates[1] = temp



            #Maskenaufruf hier
            image = mask_function(image, x,y,w,h, eyeCoordinates[0], eyeCoordinates[1],mask_args)

    return image
