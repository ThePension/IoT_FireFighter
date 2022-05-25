#!/usr/bin/python
# -*- coding:utf-8 -*-

import captor
import ctypes


# It's a captor that reads the temperature and humidity from a SHTC3 sensor
class SHTC3(captor.Captor):
    def __init__(self):
        """
        The function is called init, it returns an integer, and it takes a void pointer as an argument
        """
        self.dll = ctypes.CDLL("./SHTC3.so")
        init = self.dll.init
        init.restype = ctypes.c_int
        init.argtypes = [ctypes.c_void_p]
        init(None)

    def retrieveMeasure(self):
        """
        It returns a tuple of two floats, the first one being the temperature and the second one being
        the humidity
        :return: The return value is a tuple of two floats.
        """
        temperature = self.dll.SHTC3_Read_TH
        temperature.restype = ctypes.c_float
        temperature.argtypes = [ctypes.c_void_p]

        humidity = self.dll.SHTC3_Read_RH
        humidity.restype = ctypes.c_float
        humidity.argtypes = [ctypes.c_void_p]
        return (temperature(None), humidity(None))

# it test if the SHTC3 class is working
if __name__ == "__main__":
    shtc3 = SHTC3()
    while True:
        print('Temperature = %6.2f°C , Humidity = %6.2f%%' %
              (shtc3.read_temperature(), shtc3.read_humidity()))
