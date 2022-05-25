#!/usr/bin/python3
# -*- coding:utf-8 -*-

import captor
import asyncio
import sys
import time
import os
import io

if len(sys.argv) > 1:
    import cv2
else:
    import picamera
    import picamera.array


# It's a class that inherits from the Captor class and is used to capture images from the Raspberry Pi
# camera
class PiCamera(captor.Captor):
    def __init__(self):
        """
        The function sets the camera resolution to 640x480, the framerate to 10, the rotation to 0, the
        brightness to 50, the contrast to 0, the saturation to 0, the exposure compensation to 0, and
        the exposure mode to 'auto'
        """
        self.camera = picamera.PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 10
        self.camera.rotation = 0
        self.camera.brightness = 50
        self.camera.contrast = 0
        self.camera.saturation = 0
        self.camera.exposure_compensation = 0
        self.camera.exposure_mode = 'auto'

    def retrieveMeasure(self):
        """
        It takes a picture and returns the data
        :return: The data is being returned.
        """
        stream = io.BytesIO()
        self.camera.capture(stream, format='jpeg')
        data = stream.getvalue()
        stream.close()
        return {'fireRating':data}

    async def start_continuous_capture(self):
        """
        It continuously captures images from the camera and stores them in a buffer
        """
        for buffer in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
                stream.truncate()
                stream.seek(0)

    async def stop_continuous_capture(self):
        """
        This function stops the camera from recording
        """
        self.camera.stop_recording()

    def close(self):
        """
        The function closes the camera
        """
        self.camera.close()
