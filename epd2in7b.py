##
 #  @filename   :   epd2in7b.py
 #  @brief      :   Implements for Dual-color e-paper library
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     July 31 2017
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
EPD_WIDTH       = 176
EPD_HEIGHT      = 264

# EPD2IN7B commands
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
DATA_START_TRANSMISSION_2                   = 0x13
PARTIAL_DATA_START_TRANSMISSION_1           = 0x14
PARTIAL_DATA_START_TRANSMISSION_2           = 0x15
PARTIAL_DISPLAY_REFRESH                     = 0x16
LUT_FOR_VCOM                                = 0x20
LUT_WHITE_TO_WHITE                          = 0x21
LUT_BLACK_TO_WHITE                          = 0x22
LUT_WHITE_TO_BLACK                          = 0x23
LUT_BLACK_TO_BLACK                          = 0x24
PLL_CONTROL                                 = 0x30
TEMPERATURE_SENSOR_COMMAND                  = 0x40
TEMPERATURE_SENSOR_CALIBRATION              = 0x41
TEMPERATURE_SENSOR_WRITE                    = 0x42
TEMPERATURE_SENSOR_READ                     = 0x43
VCOM_AND_DATA_INTERVAL_SETTING              = 0x50
LOW_POWER_DETECTION                         = 0x51
TCON_SETTING                                = 0x60
TCON_RESOLUTION                             = 0x61
SOURCE_AND_GATE_START_SETTING               = 0x62
GET_STATUS                                  = 0x71
AUTO_MEASURE_VCOM                           = 0x80
VCOM_VALUE                                  = 0x81
VCM_DC_SETTING_REGISTER                     = 0x82
PROGRAM_MODE                                = 0xA0
ACTIVE_PROGRAM                              = 0xA1
READ_OTP_DATA                               = 0xA2

class EPD:
    def __init__(self):
        self.reset_pin = epdif.RST_PIN
        self.dc_pin = epdif.DC_PIN
        self.busy_pin = epdif.BUSY_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

    lut_vcom_dc = [
        0x00    ,0x00,
        0x00    ,0x1A    ,0x1A    ,0x00    ,0x00    ,0x01,        
        0x00    ,0x0A    ,0x0A    ,0x00    ,0x00    ,0x08,        
        0x00    ,0x0E    ,0x01    ,0x0E    ,0x01    ,0x10,        
        0x00    ,0x0A    ,0x0A    ,0x00    ,0x00    ,0x08,        
        0x00    ,0x04    ,0x10    ,0x00    ,0x00    ,0x05,        
        0x00    ,0x03    ,0x0E    ,0x00    ,0x00    ,0x0A,        
        0x00    ,0x23    ,0x00    ,0x00    ,0x00    ,0x01    
    ]

    # R21H
    lut_ww = [
        0x90    ,0x1A    ,0x1A    ,0x00    ,0x00    ,0x01,
        0x40    ,0x0A    ,0x0A    ,0x00    ,0x00    ,0x08,
        0x84    ,0x0E    ,0x01    ,0x0E    ,0x01    ,0x10,
        0x80    ,0x0A    ,0x0A    ,0x00    ,0x00    ,0x08,
        0x00    ,0x04    ,0x10    ,0x00    ,0x00    ,0x05,
        0x00    ,0x03    ,0x0E    ,0x00    ,0x00    ,0x0A,
        0x00    ,0x23    ,0x00    ,0x00    ,0x00    ,0x01
    ]

    # R22H    r
    lut_bw = [
        0xA0    ,0x1A    ,0x1A    ,0x00    ,0x00    ,0x01,
        0x00    ,0x0A    ,0x0A    ,0x00    ,0x00    ,0x08,
        0x84    ,0x0E    ,0x01    ,0x0E    ,0x01    ,0x10,
        0x90    ,0x0A    ,0x0A    ,0x00    ,0x00    ,0x08,
        0xB0    ,0x04    ,0x10    ,0x00    ,0x00    ,0x05,
        0xB0    ,0x03    ,0x0E    ,0x00    ,0x00    ,0x0A,
        0xC0    ,0x23    ,0x00    ,0x00    ,0x00    ,0x01
    ]

    # R23H    w
    lut_bb = [
        0x90    ,0x1A    ,0x1A    ,0x00    ,0x00    ,0x01,
        0x40    ,0x0A    ,0x0A    ,0x00    ,0x00    ,0x08,
        0x84    ,0x0E    ,0x01    ,0x0E    ,0x01    ,0x10,
        0x80    ,0x0A    ,0x0A    ,0x00    ,0x00    ,0x08,
        0x00    ,0x04    ,0x10    ,0x00    ,0x00    ,0x05,
        0x00    ,0x03    ,0x0E    ,0x00    ,0x00    ,0x0A,
        0x00    ,0x23    ,0x00    ,0x00    ,0x00    ,0x01
    ]

    # R24H    b
    lut_wb = [
        0x90    ,0x1A    ,0x1A    ,0x00    ,0x00    ,0x01,
        0x20    ,0x0A    ,0x0A    ,0x00    ,0x00    ,0x08,
        0x84    ,0x0E    ,0x01    ,0x0E    ,0x01    ,0x10,
        0x10    ,0x0A    ,0x0A    ,0x00    ,0x00    ,0x08,
        0x00    ,0x04    ,0x10    ,0x00    ,0x00    ,0x05,
        0x00    ,0x03    ,0x0E    ,0x00    ,0x00    ,0x0A,
        0x00    ,0x23    ,0x00    ,0x00    ,0x00    ,0x01
    ]

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

        self.send_command(POWER_ON)
        self.wait_until_idle()

        self.send_command(PANEL_SETTING)
        self.send_data(0xaf)        #KW-BF   KWR-AF    BWROTP 0f
        
        self.send_command(PLL_CONTROL)
        self.send_data(0x3a)       #3A 100HZ   29 150Hz 39 200HZ    31 171HZ

        self.send_command(POWER_SETTING)
        self.send_data(0x03)                  # VDS_EN, VDG_EN
        self.send_data(0x00)                  # VCOM_HV, VGHL_LV[1], VGHL_LV[0]
        self.send_data(0x2b)                  # VDH
        self.send_data(0x2b)                  # VDL
        self.send_data(0x09)                  # VDHR

        self.send_command(BOOSTER_SOFT_START)
        self.send_data(0x07)
        self.send_data(0x07)
        self.send_data(0x17)

        # Power optimization
        self.send_command(0xF8)
        self.send_data(0x60)
        self.send_data(0xA5)

        # Power optimization
        self.send_command(0xF8)
        self.send_data(0x89)
        self.send_data(0xA5)

        # Power optimization
        self.send_command(0xF8)
        self.send_data(0x90)
        self.send_data(0x00)
        
        # Power optimization
        self.send_command(0xF8)
        self.send_data(0x93)
        self.send_data(0x2A)

        # Power optimization
        self.send_command(0xF8)
        self.send_data(0x73)
        self.send_data(0x41)

        self.send_command(VCM_DC_SETTING_REGISTER)
        self.send_data(0x12)                   
        self.send_command(VCOM_AND_DATA_INTERVAL_SETTING)
        self.send_data(0x87)        # define by OTP

        self.set_lut()

        self.send_command(PARTIAL_DISPLAY_REFRESH)
        self.send_data(0x00)        

        return 0

    def wait_until_idle(self):
        while(self.digital_read(self.busy_pin) == 0):      # 0: busy, 1: idle
            self.delay_ms(100)

    def reset(self):
        self.digital_write(self.reset_pin, GPIO.LOW)         # module reset
        self.delay_ms(200)
        self.digital_write(self.reset_pin, GPIO.HIGH)
        self.delay_ms(200)    

    def set_lut(self):
        self.send_command(LUT_FOR_VCOM)               # vcom
        for count in range(0, 44):
            self.send_data(self.lut_vcom_dc[count])
        
        self.send_command(LUT_WHITE_TO_WHITE)         # ww --
        for count in range(0, 42):
            self.send_data(self.lut_ww[count])
        
        self.send_command(LUT_BLACK_TO_WHITE)         # bw r
        for count in range(0, 42):
            self.send_data(self.lut_bw[count])

        self.send_command(LUT_WHITE_TO_BLACK)         # wb w
        for count in range(0, 42):
            self.send_data(self.lut_bb[count])

        self.send_command(LUT_BLACK_TO_BLACK)         # bb b
        for count in range(0, 42):
            self.send_data(self.lut_wb[count])

    def display_frame(self, frame_buffer_black, frame_buffer_red):
        self.send_command(TCON_RESOLUTION)
        self.send_data(EPD_WIDTH >> 8)
        self.send_data(EPD_WIDTH & 0xff)        #176      
        self.send_data(EPD_HEIGHT >> 8)        
        self.send_data(EPD_HEIGHT & 0xff)       #264

        if (frame_buffer_black != None):
            self.send_command(DATA_START_TRANSMISSION_1)           
            self.delay_ms(2)
            for i in range(0, int(self.width * self.height / 8)):
                self.send_data(frame_buffer_black[i])  
            self.delay_ms(2)                  
        if (frame_buffer_red != None):
            self.send_command(DATA_START_TRANSMISSION_2)
            self.delay_ms(2)
            for i in range(0, int(self.width * self.height / 8)):
                self.send_data(frame_buffer_red[i])  
            self.delay_ms(2)        

        self.send_command(DISPLAY_REFRESH) 
        self.wait_until_idle()

    def display_image(self, image):
        assert(image.size == (self.width, self.height))

        pixels = image.load()

        # Convert image to binary format to send
        frame_black = [0] * int(self.width * self.height / 8)
        frame_red = [0] * int(self.width * self.height / 8)
        for y in range(0, self.height):
            for x in range(0, self.width):
                if pixels[x, y] == 1:
                    frame_black[int((x + y * self.width) / 8)] |= 0x80 >> (x % 8)
                elif pixels[x, y] == 2:
                    frame_red[int((x + y * self.width) / 8)] |= 0x80 >> (x % 8)

        self.display_frame(frame_black, frame_red)

    # After this command is transmitted, the chip would enter the deep-sleep
    # mode to save power. The deep sleep mode would return to standby by
    # hardware reset. The only one parameter is a check code, the command would
    # be executed if check code = 0xA5. 
    # Use EPD::Reset() to awaken and use EPD::Init() to initialize.
    def sleep(self):
        self.send_command(DEEP_SLEEP)
        self.send_data(0xa5)

### END OF FILE ###
