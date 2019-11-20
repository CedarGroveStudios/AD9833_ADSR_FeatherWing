# The MIT License (MIT)
#
# Copyright (c) 2019 Cedar Grove Studios
# Thanks to Bryan Siepert for the driver concept inspiration
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`cedargrove_ad5245`
================================================================================

CircuitPython library for the Analog Devices AD5245 I2C Potentionmeter


* Author(s): Cedar Grove Studios

Implementation Notes
--------------------

**Hardware:**

* `Cedar Grove Studios AD5245 breakout`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

_AD5245_DEFAULT_ADDRESS  = 0x2C        # 0b00101100

class AD5245:
    """Driver for the DS3502 I2C Potentiometer.

        :param address: The I2C device address for the device. Default is ``0x2C``.
        :param wiper: The default and inital wiper value. Default is 0.
    """

    _BUFFER = bytearray(1)

    def __init__(self, address=_AD5245_DEFAULT_ADDRESS, wiper = 0):
        import board
        import busio

        self._i2c = busio.I2C(board.SCL, board.SDA)
        from adafruit_bus_device.i2c_device import I2CDevice
        self._device = I2CDevice(self._i2c, address)

        self._wiper = wiper
        self._default_wiper = wiper
        self._normalized_wiper = self._wiper / 255.0
        self._write_to_device(0, wiper)

    def _write_to_device(self, command, value):
        """Write command and data value to the device."""
        with self._device:
            self._device.write(bytes([command & 0xff, value & 0xff]))

    def _read_from_device(self):
        """Reads the contents of the data register."""
        with self._device:
            self._device.readinto(self._BUFFER)
        return self._BUFFER

    @property
    def wiper(self):
        """The raw value of the potentionmeter's wiper.
            :param wiper_value: The raw wiper value from 0 to 255.
        """
        return self._wiper

    @wiper.setter
    def wiper(self, value=0):
        if value < 0 or value > 255:
            raise ValueError("raw wiper value must be from 0 to 255")
        self._write_to_device(0x00, value)
        self._wiper = value

    @property
    def normalized_wiper(self):
        """The normalized value of the potentionmeter's wiper.
            :param normalized_wiper_value: The normalized wiper value from 0.0 to 1.0.
        """
        return self._normalized_wiper

    @normalized_wiper.setter
    def normalized_wiper(self, value):
        if value < 0 or value > 1.0:
            raise ValueError("normalized wiper value must be from 0.0 to 1.0")
        self._write_to_device(0x00, int(value * 255.0))
        self._normalized_wiper = value

    @property
    def default_wiper(self):
        """The default value of the potentionmeter's wiper.
            :param wiper_value: The raw wiper value from 0 to 255.
        """
        return self._default_wiper

    @default_wiper.setter
    def default_wiper(self, value):
        if value < 0 or value > 255:
            raise ValueError("default wiper value must be from 0 to 255")
        self._default_wiper = value

    def set_default(self, default):
        """A dummy helper to maintain UI compatibility digital
            potentiometers with EEROM capability (dS3502). The AD5245's
            wiper value will be set to 0 unless the default value is
            set explicitly during or after class instantiation."""
        self._default_wiper = default

    def shutdown(self):
        """Connects the W to the B terminal and open circuits the A terminal.
            The contents of the wiper register are not changed."""
        self._write_to_device(0x20, 0)
