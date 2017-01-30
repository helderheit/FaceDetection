# -*- coding: utf-8 -*-
import cv2
from flask import Flask, Response, jsonify, request

from filters import filters
import requests
import monitor
import processor
import stream
from filters import masks
from recorder import VideoCamera

app = Flask(__name__, static_folder='docs', static_url_path = '')


"""Cameras zurückgeben"""
@app.route('/<streamid>/cams')
def get_cameras(streamid):
    cams = {'cam1': '0', 'cam2': '1', 'cam3': '2', 'cam4': '4'}

    return jsonify(cams)





"""Verfügbare Filter als Json zurückgegeben"""
@app.route('/filters')
def get_filter():
    return jsonify(stream.filter_list)
"""Verfügbare Masken als Json zurückgegeben"""
@app.route('/masks')
def get_masks():
    return jsonify(stream.mask_list)


"""Kamera wechseln"""
@app.route('/<streamid>/changecam', methods=['POST'])
def change_cam(streamid):
    command =  request.form['id']
    print command



    stream.find_stream(streamid).camera.stop_stream()
    stream.find_stream(streamid).camera = VideoCamera(int(command))
    stream.find_stream(streamid).camera.start_stream()





    return "Success"

"""Filter anwenden"""
@app.route('/<streamid>/filter', methods=['POST'])
def apply_filter(streamid):
    command =  request.form['filter']
    stream.find_stream(streamid).set_filter(command)

    return "Success"

"""Masken anwenden"""
@app.route('/<streamid>/mask', methods=['POST'])
def apply_mask(streamid):
    command = request.form['mask']

    stream.find_stream(streamid).set_mask(command)
    return "Success"


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
    print strm

    return Response(gen(streamid),
                mimetype='multipart/x-mixed-replace; boundary=frame')

"""Videostream zurückgeben"""
@app.route('/stream/<streamid>/download')
def image_download(streamid):
    strm = stream.find_stream(streamid)
    print strm

    return Response(strm.get_frame(),  mimetype='image/jpeg')


if __name__ == '__main__':

    #Maskenparameter initialisieren

    masks.initialise_masks()

    #im = cv2.imread('docs/img/preview/preview2.png')
    #im = processor.process_image(im, None, 'france', getattr(masks, 'mask_glasses'), 'Brille')
    #cv2.imwrite('docs/img/preview/test2.png', im)

    #Webapp initialisieren
    stream.initialise_web_app()

    #Systemüberwachung starten
    monitor.initialise_monitor(debug = True)


    stream.streams.append(stream.Stream('12345','',VideoCamera(1)))
    app.run(port = 3000,host = 'localhost', threaded=True, debug=True)




