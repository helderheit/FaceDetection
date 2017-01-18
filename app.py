from flask import Flask, render_template, Response, redirect, jsonify

from filters import masks
from filters import filters
from recorder import VideoCamera

app = Flask(__name__)


filter_list = {}
mask_list =  {}



@app.route('/filters')
def get_filter():
    return jsonify(filter_list)

@app.route('/masks')
def get_masks():
    return jsonify(mask_list)


@app.route('/')
def index():
    return Response(open('static/index.html'))

def gen(camera):
    while True:
       frame = camera.get_frame()
       yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/image')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



def initialise_web_app():

    #Filter und Maskenfunktionen auflisten
    for function in dir(filters):
        if 'filter_' in function:

            docstring = getattr(filters, function).__doc__
            if docstring is not None:
                lines = docstring.split('\n')

                for line in lines:
                    line = line.replace('\t', '').replace(' ', '')
                    if line != '':
                        parameter = line.split(',')[0].replace(' ', '')
                        name = line.split(',')[1].replace(' ', '')
                        filename = line.split(',')[2].replace(' ', '')
                        filter_list[function + ':' + parameter] = [function, parameter, name, filename]

    for function in dir(masks):
        if 'mask_' in function:

            docstring = getattr(masks, function).__doc__
            if docstring is not None:
                lines = docstring.split('\n')


                for line in lines:
                    line = line.replace('\t','').replace(' ', '')
                    if line != '':

                        parameter = line.split(',')[0].replace(' ', '')
                        name = line.split(',')[1].replace(' ', '')
                        filename = line.split(',')[2].replace(' ', '')
                        mask_list[function+':'+parameter] = [function, parameter, name, filename]










if __name__ == '__main__':
  #Maskenparameter initialisieren
  masks.initialise_masks()
  #Webapp initialisieren
  initialise_web_app()
  app.run(port = 3000, debug=True)
