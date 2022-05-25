#!/usr/bin/python
# -*- coding:utf-8 -*-

import common.measure as measure
import captors.shtc3 as SHTC3
import captors.lps22hb as LPS22HB
import captors.picam as PiCamera

import paho.mqtt.client as mqtt
import sys
import json
import datetime


# Is the main class whom is running on the raspberry pi
class firefighter:
    def __init__(self):
        self.name = "Firefighter"
        self.isRunning = False
        self.measures = []

        self.client = mqtt.Client()
        self.run()

    def __str__(self):
        """
        The function returns a string that is the name of the object, followed by a colon, followed by a
        string representation of the measures
        :return: The name of the object and the measures of the object.
        """
        return self.name + ": " + str(self.measures)

    def __repr__(self):
        """
        The __repr__ function is a special function that returns a string representation of an object
        :return: The name of the object and the measures of the object.
        """
        return self.name + ": " + str(self.measures)

    def _run(self):
        """
        It connects to the broker, retrieves the measures from the sensors, publishes them to the broker
        and then disconnects
        """
        self.isRunning = True
        self.client.connect(sys.argv[1], 1883, 60)

        while self.isRunning:
            measure = measure.Measure()
            measure.temperature = SHTC3.retrieveMeasure()
            measure.humidity = LPS22HB.retrieveMeasure()
            # measure.pressure = LPS22HB.retrieveMeasure()
            measure.fireRating = PiCamera.retrieveMeasure()
            measure.date = datetime.now()

            client.publish("FireFighter/Measure", json.dumps(measure.__dict__))
            time.sleep(5)

        self.client.disconnect()

    def _stop(self):
        """
        The function sets the isRunning variable to False and stop the firefighter
        """
        self.isRunning = False


if __name__ == "__main__":
    firefighter = firefighter()
