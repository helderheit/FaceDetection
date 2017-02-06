# -*- coding: utf-8 -*-
import webbrowser

import cv2
import time

import sys
from flask import Flask, Response, jsonify, request

from filters import filters
import requests
import monitor
import processor
import stream
from filters import masks
from recorder import VideoCamera

app = Flask(__name__, static_folder='docs', static_url_path='')

"""Cameras zurückgeben"""


@app.route('/stream/<streamid>/cams')
def get_cameras(streamid):
    cams = {'WebCam 1': '0', 'WebCam 2': '1', 'WebCam 3': '2', 'WebCam 4': '3'}

    return jsonify(cams)


"""Verfügbare Filter als Json zurückgegeben"""


@app.route('/filters')
def get_filter():
    return jsonify(stream.filter_list)


"""Verfügbare Masken als Json zurückgegeben"""


@app.route('/masks')
def get_masks():
    return jsonify(stream.mask_list)


@app.route('/stream/<streamid>/filteractive')
def get_active_filter(streamid):
    strm = stream.find_stream(streamid)
    if strm.filter is not None:

        return strm.filter.__name__ + '-' + strm.filter_args
    else:
        return ''


@app.route('/stream/<streamid>/maskactive')
def get_active_mask(streamid):
    strm = stream.find_stream(streamid)
    if strm.mask is not None:

        return strm.mask.__name__ + '-' + strm.mask_args
    else:
        return ''


"""Kamera wechseln"""


@app.route('/stream/<streamid>/changecam', methods=['POST'])
def change_cam(streamid):
    command = request.form['id']


    stream.find_stream(streamid).camera.stop_stream()
    stream.find_stream(streamid).camera = VideoCamera(int(command))
    stream.find_stream(streamid).camera.start_stream()

    return "Success"


"""Filter anwenden"""


@app.route('/stream/<streamid>/filter', methods=['POST'])
def apply_filter(streamid):
    command = request.form['filter']
    stream.find_stream(streamid).set_filter(command)

    return "Success"


"""Masken anwenden"""
@app.route('/stream/<streamid>/mask', methods=['POST'])
def apply_mask(streamid):
    command = request.form['mask']

    stream.find_stream(streamid).set_mask(command)
    return "Success"




def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()



@app.route('/stream/<streamid>/quit', methods = ['POST'])
def quit_stream(streamid):
    stream.find_stream(streamid).camera.stop_stream()



"""Webseite Zurückgeben"""


@app.route('/')
def index():
    return Response(open('docs/index.html'))


def gen(streamid):
    stream.find_stream(streamid).camera.start_stream()
    while True:
        frame = stream.find_stream(streamid).get_frame()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


"""Videostream zurückgeben"""


@app.route('/stream/<streamid>/image')
def video_feed(streamid):
    strm = stream.find_stream(streamid)


    return Response(gen(streamid),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


"""Videostream zurückgeben"""


@app.route('/stream/<streamid>/download')
def image_download(streamid):
    strm = stream.find_stream(streamid)


    return Response(strm.get_frame(), mimetype='image/jpeg')


def open_browser():
    webbrowser.open('http://localhost:3000/', new=2, autoraise=True)


if __name__ == '__main__':
    # Maskenparameter initialisieren

    masks.initialise_masks()

    im = cv2.imread('docs/img/preview/preview.png')
    im = processor.process_image(im, getattr(filters, 'filter_lines'), '', None, 'Brille')
    cv2.imwrite('docs/img/preview/test2.png', im)

    # Webapp initialisieren
    stream.initialise_web_app()

    # Systemüberwachung starten
    # monitor.initialise_monitor(debug = True)



    stream.streams.append(stream.Stream('12345', '', VideoCamera(0)))

    open_browser()

    app.run(port=3000, host='localhost', threaded=True, debug=False)
