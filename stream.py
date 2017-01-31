# -*- coding: utf-8 -*-
"""
Modul stream

Diese Modul verwaltet verschiedene Streams

"""
import cv2

import processor
import recorder
from filters import masks, filters


streams = []


filter_list = {}
mask_list =  {}



class Stream:

    def  __init__(self, id, redirect, camera):
        self.id = id
        self.redirect = redirect
        self.camera = camera
        self.filter = None
        self.mask = None
        self.filter_args = None
        self.mask_args = None
        self.loading_image = cv2.imread('loading.png')


    def get_frame(self):
        image = None
        if self.redirect == '':
            image = self.camera.get_frame()




        image = processor.process_image(image, self.filter,self.filter_args, self.mask, self.mask_args)

        if image is None:
            image = self.loading_image
        ret, jpeg = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
        return jpeg.tobytes()

    def set_filter(self, filter_id):
        filtername = filter_id.split(':')[0]
        filterargs = filter_id.split(':')[1]
        if self.filter == getattr(filters, filtername):
            self.filter = None
            self.filter_args = None
        else:
            self.filter = getattr(filters, filtername)
            self.filter_args = filterargs


    def set_mask(self, mask_id):
        maskname = mask_id.split(':')[0]
        maskargs = mask_id.split(':')[1]
        if self.mask == getattr(masks, maskname):
            self.mask = None
            self.mask_args = None
        else:
            self.mask = getattr(masks, maskname)
            self.mask_args = maskargs


def find_stream(id):
    for stream in streams:
        if id == stream.id:
            return stream
    return None

def find_stream_index(id):
    index = 0
    for stream in streams:
        if id == stream.id:
            return index
        index += index
    return None

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











