#!/usr/bin/python
# -*- coding:utf-8 -*-

import datetime import datetime

class Measure:
    def __init__(self, temperature = None, humidity = None, pressure = None, fireRating = None, date = None):
        self.name = "Measure"
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.fireRating = fireRating
        self.date = date

    def __str__(self):
        return self.name + ": " + str(self.value)

    def __repr__(self):
        return self.name + ": " + str(self.value)