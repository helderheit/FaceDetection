# -*- coding: utf-8 -*-

from flask import Flask, render_template, Response, redirect, jsonify, request

import processor
from filters import masks
from filters import filters
from recorder import VideoCamera

import cv2

app = Flask(__name__, static_url_path = '')


filter_list = {}
mask_list =  {}


"""Verfügbare Filter als Json zurückgegeben"""
@app.route('/filters')
def get_filter():
    return jsonify(filter_list)
"""Verfügbare Masken als Json zurückgegeben"""
@app.route('/masks')
def get_masks():
    return jsonify(mask_list)

"""Filter anwenden"""
@app.route('/filter', methods=['POST'])
def apply_filter():
    print request.form['filter']
    return "Success"

"""Masken anwenden"""
@app.route('/mask', methods=['POST'])
def apply_mask():
    print request.form['mask']
    return "Success"


"""Webseite Zurückgeben"""
@app.route('/')
def index():
    return Response(open('static/index.html'))

def gen(camera):
    while True:
       frame = camera.get_frame()
       yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
"""Videostream zurückgeben"""
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

  im = cv2.imread('static/img/preview/preview2.png')
  im = processor.process_image(im)
  cv2.imwrite('static/img/preview/test.png', im)

  #Webapp initialisieren
  initialise_web_app()

  app.run(port = 3000, debug=True)



