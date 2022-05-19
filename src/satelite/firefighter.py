#!/usr/bin/python
# -*- coding:utf-8 -*-

import ../common/measure as Measure
import ./captors/shtc3 as SHTC3
import ./captors/lps22hb as LPS22HB
import ./captors/picam as PiCamera

import paho.mqtt.client as mqtt
import sys
import json

class firefighter:
    def __init__(self):
        self.name = "Firefighter"
        self.isRunning = False
        self.measures = []

        self.client = mqtt.Client()
        self.run()

    def __str__(self):
        return self.name + ": " + str(self.measures)

    def __repr__(self):
        return self.name + ": " + str(self.measures)

    def _run(self):
        self.isRunning = True
        self.client.connect(sys.argv[1], 1883, 60)

        while self.isRunning:
            measure = Measure.Measure()
            measure.temperature = SHTC3.retrieveMeasure()
            measure.humidity = LPS22HB.retrieveMeasure()
            # measure.pressure = LPS22HB.retrieveMeasure()
            measure.fireRating = PiCamera.retrieveMeasure()

            client.publish("Measure", json.dumps(measure.__dict__))
            time.sleep(5)

        self.client.disconnect()


    def _stop(self):
        self.isRunning = False

