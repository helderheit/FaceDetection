from flask import Flask, render_template, Response, redirect
from recorder import VideoCamera
import cv2
app = Flask(__name__)

black = False
@app.route('/')
def index():
    return Response(open('static/index.html'))

def gen(camera):
    while True:
       frame = camera.get_frame(black)
       yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/image')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')





if __name__ == '__main__':
  app.run(port = 3000, debug=True)
