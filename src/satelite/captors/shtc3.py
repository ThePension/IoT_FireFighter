#!/usr/bin/python
# -*- coding:utf-8 -*-
import captor
import ctypes

class SHTC3(captor.Captor):
    def __init__(self):
        self.dll = ctypes.CDLL("./SHTC3.so")
        init = self.dll.init
        init.restype = ctypes.c_int
        init.argtypes = [ctypes.c_void_p]
        init(None)

    def read_temperature(self):
        temperature = self.dll.SHTC3_Read_TH
        temperature.restype = ctypes.c_float
        temperature.argtypes = [ctypes.c_void_p]
        return temperature(None)

    def read_humidity(self):
        humidity = self.dll.SHTC3_Read_RH
        humidity.restype = ctypes.c_float
        humidity.argtypes = [ctypes.c_void_p]
        return humidity(None)


if __name__ == "__main__":
    shtc3 = SHTC3()
    while True:
        print('Temperature = %6.2f°C , Humidity = %6.2f%%' % (shtc3.read_temperature(), shtc3.read_humidity()))