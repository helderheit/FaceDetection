# -*- coding: utf-8 -*-
import cv2
from flask import Flask, Response, jsonify, request

from filters import filters
import monitor
import processor
import stream
from filters import masks
from recorder import VideoCamera

app = Flask(__name__, static_folder='docs', static_url_path = '')





"""Verfügbare Filter als Json zurückgegeben"""
@app.route('/filters')
def get_filter():
    return jsonify(stream.filter_list)
"""Verfügbare Masken als Json zurückgegeben"""
@app.route('/masks')
def get_masks():
    return jsonify(stream.mask_list)

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

def gen(stream):
    stream.camera.start_stream()
    while True:
        frame = stream.get_frame()
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


"""Videostream zurückgeben"""
@app.route('/stream/<streamid>/image')
def video_feed(streamid):
    strm = stream.find_stream(streamid)
    print strm

    return Response(gen(strm),
                mimetype='multipart/x-mixed-replace; boundary=frame')






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


    stream.streams.append(stream.Stream('12345','',VideoCamera()))
    app.run(port = 3000,host = 'localhost', threaded=True, debug=True)




