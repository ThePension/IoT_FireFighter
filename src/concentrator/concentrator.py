#!/usr/bin/python
# -*- coding:utf-8 -*-

import paho.mqtt.client as mqtt
import os
import json
import sys

sys.path.append("../common")

import measure

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Is the main class whom is running on the virtual machine


class Concentrator:
    def __init__(self):
        self.name = "Concentrator"
        self.isRunning = False
        self.measures = []

        self.influxdb_server = os.environ['INFLUXDB_SERVER']
        self.influxdb_token = os.environ['INFLUXDB_TOKEN']
        self.influxdb_org = os.environ['INFLUXDB_ORG']
        self.influxdb_bucket = os.environ['INFLUXDB_BUCKET']

        self.mqtt_client = os.environ['MQTT_CLIENT']
        self.mqtt_brocker = os.environ['MQTT_BROCKER']
        self.mqtt_port = os.environ['MQTT_PORT']
        self.mqtt_topic = os.environ['MQTT_TOPIC']

        self._run()

    def __str__(self):
        """
        The __str__ function is a special function that is called when you print an object
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
        It creates a MQTT client, connects to the MQTT broker, subscribes to the topic
        "FireFighter/Measure" and starts the loop that listens for messages
        """
        self.isRunning = True

        client = mqtt.Client(self.mqtt_client)
        client.on_message = self.on_message
        client.connect(self.mqtt_brocker, int(self.mqtt_port), 60)
        client.subscribe([(self.mqtt_topic, 0)])  # Default QoS=0
        client.loop_forever()

    def stop(self):
        """
        The function stops the loop that is running in the background
        """
        client.loop_stop()
        self.isRunning = False

    def on_message(self,client, userdata, message):
        """
        It takes the data from the MQTT message, converts it to a JSON object, and then writes it to the
        InfluxDB database

        :param client: the MQTT client
        :param userdata: The user data set in Client() or user_data_set()
        :param message: The message variable is a JSON string that contains the data from the MQTT
        message
        """
        data = str(message.payload.decode("utf-8"))
        mm = json.loads(data)

        try:
            with InfluxDBClient(url=self.influxdb_server, token=self.influxdb_token, org=self.influxdb_org) as clientDB:
                write_api = clientDB.write_api(write_options=SYNCHRONOUS)

                topic = message.topic.split("/")[-1]

                temp = "mem,host=host1 {}={}".format(topic+'/temperature', mm['temperature'])
                humy = "mem,host=host1 {}={}".format(topic+'/humidity', mm['humidity'])
                pres = "mem,host=host1 {}={}".format(topic+'/pressure', mm['pressure'])
                fire = "mem,host=host1 {}={}".format(topic+'/fireRating', mm['fireRating'])

                write_api.write(self.influxdb_bucket, self.influxdb_org, temp)
                write_api.write(self.influxdb_bucket, self.influxdb_org, humy)
                write_api.write(self.influxdb_bucket, self.influxdb_org, pres)
                write_api.write(self.influxdb_bucket, self.influxdb_org, fire)

                clientDB.close()

        except Exception as e:
        	print ("error")


if __name__ == "__main__":
    concentrator = Concentrator()