#!/usr/bin/python
# -*- coding:utf-8 -*-

import datetime

# It creates a class called Measure.
class Measure:
    def __init__(self, temperature = None, humidity = None, pressure = None, fireRating = None, date = None):
        """
        This function is a constructor for the Measure class. It takes in 5 parameters, all of which are
        optional. The parameters are temperature, humidity, pressure, fireRating, and date. The function
        sets the name of the class to "Measure" and sets the class variables to the parameters.

        :param temperature: The temperature in degrees Celsius
        :param humidity: The relative humidity in percent
        :param pressure: The pressure in the room
        :param fireRating: 0 = no fire, 1 = fire
        :param date: The date and time of the measure
        """
        self.name = "Measure"
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.fireRating = fireRating
        self.date = date

    def __str__(self):
        """
        The __str__ function is a special function that is called when you use the print function on an
        object
        :return: The name of the attribute and its value.
        """
        return self.name + ": " + str(self.value)

    def __repr__(self):
        """
        The __repr__ function is a special function that returns a string representation of the object.

        The __repr__ function is called by the repr() built-in function and by string conversions
        (reverse quotes) and by the print statement
        :return: The name of the attribute and its value.
        """
        return self.name + ": " + str(self.value)