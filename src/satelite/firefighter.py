#!/usr/bin/python
# -*- coding:utf-8 -*-

import ../common/measure as Measure
import ./sensors/shtc3 as SHTC3
import ./sensors/lps22hb as LPS22HB
import ./sensors/picam as PiCamera

class firefighter:
    def __init__(self):
        self.name = "Firefighter"
        self.measures = []

    def __str__(self):
        return self.name + ": " + str(self.measures)

    def __repr__(self):
        return self.name + ": " + str(self.measures)
