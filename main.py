#!/usr/bin/python3
# ./main.py -platform offscreen

import argparse
from datetime import datetime
import json
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import sys
from weather import Weather

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

DISP_SIZE = (640, 384)

WHITE = 0xffffffff
BLACK = 0xff000000
RED = 0xffff0000


class ForecastDisplay(QWidget):
    def __init__(self, icon_map, now, conditions):
        super().__init__()
        self.icon_map = icon_map
        self.now = now
        self.conditions = conditions
        self.initUI()

    def initUI(self):
        font_small = QFont('FreeFont')
        font_small.setWeight(QFont.Bold)
        font_small.setPixelSize(110)

        font_large = QFont('FreeFont')
        font_large.setWeight(QFont.Bold)
        font_large.setPixelSize(72)

        icons = QFont('Weather Icons')
        icons.setWeight(QFont.Normal)
        icons.setPixelSize(48)

        lbl1 = QLabel(self.now.strftime('%A'), self)
        lbl1.setFont(font_small)
        lbl1.move(0, 80)
        lbl1.resize(640, 110)
        lbl1.setAlignment(Qt.AlignCenter)

        lbl2 = QLabel(self.now.strftime('%B %d'), self)
        lbl2.setFont(font_large)
        lbl2.move(0, 200)
        lbl2.resize(640, 72)
        lbl2.setAlignment(Qt.AlignCenter)
        lbl2.setStyleSheet('QLabel { color : red; }')

        lbl3 = QLabel(self.icon_map[self.conditions['icon']], self)
        lbl3.setFont(icons)
        lbl3.move(10, 10)

        self.setGeometry(0, 0, DISP_SIZE[0], DISP_SIZE[1])
        self.setWindowTitle('Forecast Display')
        self.show()


def get_config():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_file', '-c', default=BASE_PATH + '/config.json')
    parser.add_argument('--debug_show', action='store_true')
    args, remaining = parser.parse_known_args()
    args = vars(args)

    # Parse from config file
    with open(args['config_file']) as file:
        json_data = json.load(file)
        args.update(json_data)

    return args, remaining


def main():
    config, argv = get_config()

    app = QApplication(sys.argv)

    # Load fonts
    QFontDatabase.addApplicationFont(BASE_PATH + '/fonts/freefont/FreeMonoBold.ttf')
    QFontDatabase.addApplicationFont(BASE_PATH + '/fonts/weather-icons/weathericons-regular-webfont.ttf')

    # Set default font
    font = QFont('FreeFont')
    font.setPixelSize(12)
    font.setStyleHint(QFont.AnyStyle, QFont.NoAntialias)
    app.setFont(font)

    with open(BASE_PATH + '/icon-mapping.json') as file:
        icon_map = json.load(file)

    weather = Weather(api_key=config['api_key'], city=config['city'], state=config['state'])
    conditions = weather.get_conditions()
    forecast = weather.get_forecast()

    now = datetime.now()

    display = ForecastDisplay(icon_map=icon_map, now=now, conditions=conditions)

    if config['debug_show']:
        # Show image in a window for debugging
        app.exec_()
    else:
        # Render to image
        img = QImage(display.size(), QImage.Format_RGB888)
        img.fill(WHITE)
        display.render(QPainter(img))

        # Send to e-paper display
        from epd7in5 import EPD
        epd = EPD()
        epd.init()
        epd.display_qimage(img, BLACK, RED)
        epd.sleep()


if __name__ == '__main__':
    main()
