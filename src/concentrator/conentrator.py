#!/usr/bin/python
# -*- coding:utf-8 -*-

import ../common/measure as measure

import paho.mqtt.client as mqtt
import os
import json
import datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

class Concentrator:
    def __init__(self):
        self.name = "Concentrator"
        self.isRunning = False
        self.measures = []

        self.influxdb_server = os.environment['INFLUXDB_SERVER']
        self.influxdb_token = os.environment['INFLUXDB_TOKEN']
        self.influxdb_org = os.environment['INFLUXDB_ORG']
        self.influxdb_bucket = os.environment['INFLUXDB_BUCKET']


        self.run()

    def __str__(self):
        return self.name + ": " + str(self.measures)

    def __repr__(self):
        return self.name + ": " + str(self.measures)

    def _run(self):
        self.isRunning = True

        client = paho.Client(os.environment['MQTT_CLIENT'])
        client.on_message=on_message
        client.connect(os.environment['MQTT_BROCKER'], os.environment['MQTT_PORT'], 60)
        client.subscribe([("FireFighter/Measure", 0)]) # Default QoS=0
        client.loop_forever()

    def stop(self):
        client.loop_stop()
        self.isRunning = False

    def on_message(client, userdata, message):
        data = str(message.payload.decode("utf-8"))
        measure = json.loads(data, object_hook=measure.Measure)

        with InfluxDBClient(url=self.influxdb_server, token=self.influxdb_token, org=self.influxdb_org) as clientDB:
        write_api = clientDB.write_api(write_options=SYNCHRONOUS)

        topic=message.topic.split("/")[-1]
        data = "mem,host=host1 {}={}".format(topic, measure)

        write_api.write(self.influxdb_bucket, self.influxdb_org, data)

        clientDB.close()
