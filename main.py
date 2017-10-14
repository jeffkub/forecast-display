#!/usr/bin/python3
# ./main.py -platform offscreen

import argparse
from datetime import datetime
import json
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os
import sys
from weather import Weather

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

DISP_SIZE = (640, 384)

WHITE = 0xffffffff
BLACK = 0xff000000
RED = 0xffff0000


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

    with open(BASE_PATH + '/icon-mapping.json') as file:
        icon_map = json.load(file)

    weather = Weather(api_key=config['api_key'], city=config['city'], state=config['state'])
    conditions = weather.get_conditions()
    forecast = weather.get_forecast()

    now = datetime.now()

    display = uic.loadUi(BASE_PATH + '/layout.ui')
    display.high.setText('{}\N{DEGREE SIGN}'.format(forecast[0]['high']['fahrenheit']))
    display.low.setText('{}\N{DEGREE SIGN}'.format(forecast[0]['low']['fahrenheit']))
    display.temp.setText('{:.0f}\N{DEGREE SIGN}'.format(conditions['temp_f']))
    display.feels_like.setText('Feels like {:.0f}\N{DEGREE SIGN}'.format(float(conditions['feelslike_f'])))
    display.cond.setText(icon_map[conditions['icon']])
    display.percip.setText('{}%'.format(forecast[0]['pop']))
    display.weekday.setText(now.strftime('%A'))
    display.date.setText(now.strftime('%B %d'))
    display.show()

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
