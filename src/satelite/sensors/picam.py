#!/usr/bin/python3

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


class PiCamera:
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 10
        self.camera.rotation = 0
        self.camera.brightness = 50
        self.camera.contrast = 0
        self.camera.saturation = 0
        self.camera.exposure_compensation = 0
        self.camera.exposure_mode = 'auto'

    def capture(self):
        stream = io.BytesIO()
        self.camera.capture(stream, format='jpeg')
        data = stream.getvalue()
        stream.close()
        return data

    async def start_continuous_capture(self):
        for buffer in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
                stream.truncate()
                stream.seek(0)

    async def stop_continuous_capture(self):
        self.camera.stop_recording()

    def close(self):
        self.camera.close()