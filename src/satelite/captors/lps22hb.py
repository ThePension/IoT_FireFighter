#!/usr/bin/python3
# -*- coding:utf-8 -*-

from captors.captor import Captor
import measure
import time
import smbus
# i2c address
LPS22HB_I2C_ADDRESS = 0x5C
#
LPS_ID = 0xB1
# Register
LPS_INT_CFG = 0x0B  # Interrupt register
LPS_THS_P_L = 0x0C  # Pressure threshold registers
LPS_THS_P_H = 0x0D
LPS_WHO_AM_I = 0x0F  # Who am I
LPS_CTRL_REG1 = 0x10  # Control registers
LPS_CTRL_REG2 = 0x11
LPS_CTRL_REG3 = 0x12
LPS_FIFO_CTRL = 0x14  # FIFO configuration register
LPS_REF_P_XL = 0x15  # Reference pressure registers
LPS_REF_P_L = 0x16
LPS_REF_P_H = 0x17
LPS_RPDS_L = 0x18  # Pressure offset registers
LPS_RPDS_H = 0x19
LPS_RES_CONF = 0x1A  # Resolution register
LPS_INT_SOURCE = 0x25  # Interrupt register
LPS_FIFO_STATUS = 0x26  # FIFO status register
LPS_STATUS = 0x27  # Status register
LPS_PRESS_OUT_XL = 0x28  # Pressure output registers
LPS_PRESS_OUT_L = 0x29
LPS_PRESS_OUT_H = 0x2A
LPS_TEMP_OUT_L = 0x2B  # Temperature output registers
LPS_TEMP_OUT_H = 0x2C
LPS_RES = 0x33  # Filter reset register


# It's a captor that can read the pressure and temperature from a LPS22HB sensor
class LPS22HB(Captor):
    def __init__(self, address=LPS22HB_I2C_ADDRESS):
        """
        The function is called __init__ and it takes one argument, address, which is set to the default
        value of 0x5D

        :param address: The I2C address of the LPS22HB
        """
        self._address = address
        self._bus = smbus.SMBus(1)
        self.LPS22HB_RESET()  # Wait for reset to complete
        # Low-pass filter disabled , output registers not updated until MSB and LSB have been read , Enable Block Data Update , Set Output Data Rate to 0
        self._write_byte(LPS_CTRL_REG1, 0x02)

    def LPS22HB_RESET(self):
        """
        Set the SWRESET bit in the CTRL_REG2 register to 1, then wait until the bit is cleared.
        """
        Buf = self._read_u16(LPS_CTRL_REG2)
        Buf |= 0x04
        self._write_byte(LPS_CTRL_REG2, Buf)  # SWRESET Set 1
        while Buf:
            Buf = self._read_u16(LPS_CTRL_REG2)
            Buf &= 0x04

    def LPS22HB_START_ONESHOT(self):
        """
        Set the ONE_SHOT bit in the LPS_CTRL_REG2 register to 1.
        """
        Buf = self._read_u16(LPS_CTRL_REG2)
        Buf |= 0x01  # ONE_SHOT Set 1
        self._write_byte(LPS_CTRL_REG2, Buf)

    def _read_byte(self, cmd):
        """
        It reads a byte from the I2C device at the address specified by the address parameter

        :param cmd: The command to send to the device
        :return: The value of the register at the address specified by cmd.
        """
        return self._bus.read_byte_data(self._address, cmd)

    def _read_u16(self, cmd):
        """
        It reads two bytes from the I2C bus, and returns the value as a 16-bit unsigned integer

        :param cmd: The command to send to the device
        :return: The value of the register is being returned.
        """
        LSB = self._bus.read_byte_data(self._address, cmd)
        MSB = self._bus.read_byte_data(self._address, cmd+1)
        return (MSB << 8) + LSB

    def _write_byte(self, cmd, val):
        """
        _write_byte() writes a byte to the I2C bus

        :param cmd: The command to send to the device
        :param val: the value to write
        """
        self._bus.write_byte_data(self._address, cmd, val)

    def retrieveMeasure(self):
        """
        It reads the temperature and pressure from the sensor and returns them as a dictionary
        :return: A dictionary with the temperature and pressure values.
        """

        u8Buf = [0, 0, 0]

        PRESS_DATA = None
        TEMP_DATA = None

        while PRESS_DATA == None or TEMP_DATA == None:
            # Generate a new temperature data
            self.LPS22HB_START_ONESHOT()
            if (self._read_byte(LPS_STATUS) & 0x01) == 0x01:  # a new pressure data is generated
                u8Buf[0] = self._read_byte(LPS_PRESS_OUT_XL)
                u8Buf[1] = self._read_byte(LPS_PRESS_OUT_L)
                u8Buf[2] = self._read_byte(LPS_PRESS_OUT_H)
                PRESS_DATA = ((u8Buf[2] << 16)+(u8Buf[1] << 8)+u8Buf[0])/4096.0
            if (self._read_byte(LPS_STATUS) & 0x02) == 0x02:   # a new temperature data is generated
                u8Buf[0] = self._read_byte(LPS_TEMP_OUT_L)
                u8Buf[1] = self._read_byte(LPS_TEMP_OUT_H)
                TEMP_DATA = ((u8Buf[1] << 8)+u8Buf[0])/100.0
        return {'temperature':TEMP_DATA, 'pressure':PRESS_DATA}


if __name__ == '__main__':
    PRESS_DATA = 0.0
    TEMP_DATA = 0.0
    u8Buf = [0, 0, 0]
    print("\nPressure Sensor Test Program ...\n")
    lps22hb = LPS22HB()
    while True:
        time.sleep(0.1)
        lps22hb.LPS22HB_START_ONESHOT()
        if (lps22hb.read_byte(LPS_STATUS) & 0x01) == 0x01:  # a new pressure data is generated
            u8Buf[0] = lps22hb.read_byte(LPS_PRESS_OUT_XL)
            u8Buf[1] = lps22hb.read_byte(LPS_PRESS_OUT_L)
            u8Buf[2] = lps22hb.read_byte(LPS_PRESS_OUT_H)
            PRESS_DATA = ((u8Buf[2] << 16)+(u8Buf[1] << 8)+u8Buf[0])/4096.0
        if (lps22hb.read_byte(LPS_STATUS) & 0x02) == 0x02:   # a new temperature data is generated
            u8Buf[0] = lps22hb.read_byte(LPS_TEMP_OUT_L)
            u8Buf[1] = lps22hb.read_byte(LPS_TEMP_OUT_H)
            TEMP_DATA = ((u8Buf[1] << 8)+u8Buf[0])/100.0
        print('Pressure = %6.2f hPa , Temperature = %6.2f °C\r\n' %
              (PRESS_DATA, TEMP_DATA))
