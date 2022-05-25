#!/usr/bin/python
# -*- coding:utf-8 -*-

import common.measure as measure
import captors.shtc3 as SHTC3
import captors.lps22hb as LPS22HB
import captors.picam as PiCamera

import paho.mqtt.client as mqtt
import sys
import json
import os
import datetime
from fire_detection_cnn.firenet import detect_fire


# Is the main class whom is running on the raspberry pi
class firefighter:
    def __init__(self):
        self.name = "Firefighter"
        self.isRunning = False

        self.mqtt_client = os.environment['MQTT_CLIENT']
        self.mqtt_brocker = os.environment['MQTT_BROCKER']
        self.mqtt_port = os.environment['MQTT_PORT']
        self.mqtt_topic = os.environment['MQTT_TOPIC']

        self.client = mqtt.Client()
        self.run()

    def __str__(self):
        """
        The function returns a string that is the name of the object, followed by a colon, followed by a
        string representation of the measures
        :return: The name of the object and the measures of the object.
        """
        return self.name

    def __repr__(self):
        """
        The __repr__ function is a special function that returns a string representation of an object
        :return: The name of the object and the measures of the object.
        """
        return self.name

    def _run(self):
        """
        It connects to the broker, retrieves the measures from the sensors, publishes them to the broker
        and then disconnects
        """
        self.isRunning = True
        self.client.connect(self.mqtt_brocker, self.mqtt_port, 60)

        while self.isRunning:

            shtc3 = SHTC3.retrieveMeasure()
            lps22hb = LPS22HB.retrieveMeasure()
            picam = PiCamera.retrieveMeasure()

            measure = measure.Measure()
            measure.temperature = shtc3['temperature']
            measure.humidity = shtc3['humidity']
            measure.pressure = lps22hb['pressure']

            fireDetected = detect_fire(picam['frame'])

            measure.fireRating = evaluateRating(measure, fireDetected)
            measure.date = datetime.now()

            client.publish(self.mqtt_topic, json.dumps(measure.__dict__))
            time.sleep(5)

        self.client.disconnect()

    def _stop(self):
        """
        The function sets the isRunning variable to False and stop the firefighter
        """
        self.isRunning = False

    def evaluateRating(self, measure, fireDetected):
        rate = 0
        if fireDetected:
            return 3
        
        if measure.temperature > 100:
            rate += 1

        if measure.humidity < 40:
            rate += 1

        if measure.pressure < 60: # Maybe 60k, based on : https://pdf.sciencedirectassets.com/278653/1-s2.0-S1877705813X00141/1-s2.0-S1877705813012411/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJ%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIFzix5f4ORQRF1trkNAR4fVyr%2FwnLutLmUwA%2FjVTVfZZAiEAzwX5zhTXvIsXfhfhzd0Dd6a1LS%2FUgskNGUMeXQ5TwUQq2wQIiP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAEGgwwNTkwMDM1NDY4NjUiDLBoxF1sXUw8BBlQwCqvBGFEwGIuNU6LbCKixOjWnJn6R1n81dzkGES2xNUXCM4SaoJaWdmpzf5rNVCDA16g14NmQwaSSmTEHw0Pc6Qa3WNqygk7aIk5T9quPQpDfckTmZFyWyvuEA3R0sq0lk2UNYMOhmwMCvRYEkH4e8EtfC4cZFJt8plGBXu0FvScTEzNDZz4MJd6c7zmKBukHD9U52eRrFSBY%2BY1obAkKfPrVy0AvuvTP1oPaqqyaygCShRDlJnjAarwDYEz1tcZlA2ONMWG14GwXLiRCEJqlPQvW3YSz5D6scTdbYJGK2rHlmcP4dop3148qw%2FslwTbnVLpTSZ%2B6BRt3J%2FaNISVNlxfZ7f8BZaIzrOAd7HH2%2BGr2921mBeKbgHXErLDwrSer0hTA6ORCQZnb1lsUgGW5LCHxd6ygnJ93SMh6HCzL1J83V7Rlybtamj7mxBQAcHh18a3t%2FsLll8aSExagdnxNZxLG%2F46vxVrDOkoTyNvYYd7Jad14j7aKV0WzvNu7bh8joQOVA3T42cCoNb%2FOgzUe6e%2FNFGZRX2ldTpgvnqpsfth8oklHFVVmaN0z62NMTc7z9Prdu8CRKwrxufugxegSKSgyjAR8EiOm7d3JkC85vQzwzg7j1%2B32x4%2FaRIzQWzOH3WGzbqTUe%2Fsxc4uSXMgQPmMqgRva1V2Fq7PoK8yequRuDR8IKSn2MchUYhi3pwQR%2BirjgD1YN4KtwRkMySbgRnTWACyeSlLJPoArT%2FGo8kCNzUw0Ze3lAY6qQF7utuseIpwqk7Vyc6d%2B2MGjHKpIhbcfdupgI0MU3urmE1E1lI8gNb%2B70kviUhlJ%2BKyTECxi8BGr3yzBfnAYKNLLZIMYygBLIL%2F83q%2BvrJoDWQP274GQQHJUtnSwiZ%2BK3Y%2BVDy8ewdKewuYlcZKl%2BxegvyHeSHJuCJMeUta7YPcPPhXo48vOwkC%2FFTYceNO3RFObrmhAdIGnsxQPdFJzPl32gXPMgKEthvt&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220525T074059Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTYUFMRZZVP%2F20220525%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=72177f1a448c6d9ac50fd179a0c1434c9ed0742d802dce234b535b2b14809970&hash=204b7eac59364545bc05e39caa224e6785417b73f2eacace6d7f5fcc29ca0ab7&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S1877705813012411&tid=spdf-63060fa0-2959-43b8-a57a-c0fbaa31661d&sid=326ef94927f5964b28484a24a6cbdf5e64aagxrqb&type=client&ua=4d515106005754560902&rr=710ca045fddf3b58
            rate += 1

        return rate


if __name__ == "__main__":
    firefighter = firefighter()
