##
 #  @filename   :   epd7in5.py
 #  @brief      :   Implements for Dual-color e-paper library
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     July 10 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 #

import epdif
import RPi.GPIO as GPIO

# Display resolution
EPD_WIDTH       = 640
EPD_HEIGHT      = 384

# EPD7IN5 commands
PANEL_SETTING                               = 0x00
POWER_SETTING                               = 0x01
POWER_OFF                                   = 0x02
POWER_OFF_SEQUENCE_SETTING                  = 0x03
POWER_ON                                    = 0x04
POWER_ON_MEASURE                            = 0x05
BOOSTER_SOFT_START                          = 0x06
DEEP_SLEEP                                  = 0x07
DATA_START_TRANSMISSION_1                   = 0x10
DATA_STOP                                   = 0x11
DISPLAY_REFRESH                             = 0x12
IMAGE_PROCESS                               = 0x13
LUT_FOR_VCOM                                = 0x20
LUT_BLUE                                    = 0x21
LUT_WHITE                                   = 0x22
LUT_GRAY_1                                  = 0x23
LUT_GRAY_2                                  = 0x24
LUT_RED_0                                   = 0x25
LUT_RED_1                                   = 0x26
LUT_RED_2                                   = 0x27
LUT_RED_3                                   = 0x28
LUT_XON                                     = 0x29
PLL_CONTROL                                 = 0x30
TEMPERATURE_SENSOR_COMMAND                  = 0x40
TEMPERATURE_CALIBRATION                     = 0x41
TEMPERATURE_SENSOR_WRITE                    = 0x42
TEMPERATURE_SENSOR_READ                     = 0x43
VCOM_AND_DATA_INTERVAL_SETTING              = 0x50
LOW_POWER_DETECTION                         = 0x51
TCON_SETTING                                = 0x60
TCON_RESOLUTION                             = 0x61
SPI_FLASH_CONTROL                           = 0x65
REVISION                                    = 0x70
GET_STATUS                                  = 0x71
AUTO_MEASUREMENT_VCOM                       = 0x80
READ_VCOM_VALUE                             = 0x81
VCM_DC_SETTING                              = 0x82

class EPD:
    def __init__(self):
        self.reset_pin = epdif.RST_PIN
        self.dc_pin = epdif.DC_PIN
        self.busy_pin = epdif.BUSY_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

    def digital_write(self, pin, value):
        epdif.epd_digital_write(pin, value)

    def digital_read(self, pin):
        return epdif.epd_digital_read(pin)

    def delay_ms(self, delaytime):
        epdif.epd_delay_ms(delaytime)

    def send_command(self, command):
        self.digital_write(self.dc_pin, GPIO.LOW)
        # the parameter type is list but not int
        # so use [command] instead of command
        epdif.spi_transfer([command])

    def send_data(self, data):
        self.digital_write(self.dc_pin, GPIO.HIGH)
        # the parameter type is list but not int
        # so use [data] instead of data
        epdif.spi_transfer([data])

    def init(self):
        if (epdif.epd_init() != 0):
            return -1
        self.reset()

        self.send_command(POWER_SETTING)
        self.send_data(0x37)
        self.send_data(0x00)

        self.send_command(PANEL_SETTING)
        self.send_data(0xCF)
        self.send_data(0x08)

        self.send_command(BOOSTER_SOFT_START)
        self.send_data(0xc7)
        self.send_data(0xcc)
        self.send_data(0x28)

        self.send_command(POWER_ON)
        self.wait_until_idle()

        self.send_command(PLL_CONTROL)
        self.send_data(0x3c)

        self.send_command(TEMPERATURE_CALIBRATION)
        self.send_data(0x00)

        self.send_command(VCOM_AND_DATA_INTERVAL_SETTING)
        self.send_data(0x77)

        self.send_command(TCON_SETTING)
        self.send_data(0x22)

        self.send_command(TCON_RESOLUTION)
        self.send_data(0x02)     #source 640
        self.send_data(0x80)
        self.send_data(0x01)     #gate 384
        self.send_data(0x80)

        self.send_command(VCM_DC_SETTING)
        self.send_data(0x1E)      #decide by LUT file

        self.send_command(0xe5)           #FLASH MODE
        self.send_data(0x03)

    def wait_until_idle(self):
        while(self.digital_read(self.busy_pin) == 0):      # 0: busy, 1: idle
            self.delay_ms(100)

    def reset(self):
        self.digital_write(self.reset_pin, GPIO.LOW)         # module reset
        self.delay_ms(200)
        self.digital_write(self.reset_pin, GPIO.HIGH)
        self.delay_ms(200)

    def display_image(self, image, black, red):
        assert (image.size == (self.width, self.height))

        pixels = image.load()

        self.send_command(DATA_START_TRANSMISSION_1)

        for y in range(0, self.height):
            for x in range(0, self.width, 2):
                data = 0

                if pixels[x, y] == black:
                    data |= 0x00
                elif pixels[x, y] == red:
                    data |= 0x40
                else:
                    data |= 0x30

                if pixels[x + 1, y] == black:
                    data |= 0x00
                elif pixels[x + 1, y] == red:
                    data |= 0x04
                else:
                    data |= 0x03

                self.send_data(data)

        self.send_command(DISPLAY_REFRESH)
        self.delay_ms(100)
        self.wait_until_idle()

    def sleep(self):
        self.send_command(POWER_OFF)
        self.wait_until_idle()
        self.send_command(DEEP_SLEEP)
        self.send_data(0xa5)

### END OF FILE ###
