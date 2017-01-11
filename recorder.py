import cv2



class VideoCamera(object):


    def __init__(self):

        self.video = cv2.VideoCapture(1)


    def __del__(self):
        self.video.release()

    def get_frame(self, black):
        success, image = self.video.read()

        mask = cv2.imread("mask.png")


        face_cascade = cv2.CascadeClassifier(
            'haarcascades/haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier(
            'haarcascades/haarcascade_eye.xml')


        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = image[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray,1.3)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        ret, jpeg = cv2.imencode('.jpg', image, [0])
        return jpeg.tobytes()
