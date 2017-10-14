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


def get_config(argv):
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_file', '-c', default=BASE_PATH + '/config.json')
    parser.add_argument('--outfile', '-o', default=None)
    parser.add_argument('--skip_weather', action='store_true')
    args = vars(parser.parse_args(argv))

    # Parse from config file
    with open(args['config_file']) as file:
        json_data = json.load(file)
        args.update(json_data)

    return args


def main():
    # Initialize QT in offscreen mode (no window needed)
    app = QApplication(sys.argv + '-platform offscreen'.split())

    # Get configuration from command line and config file
    config = get_config(app.arguments()[1:])

    # Load fonts
    QFontDatabase.addApplicationFont(BASE_PATH + '/fonts/freefont/FreeMonoBold.ttf')
    QFontDatabase.addApplicationFont(BASE_PATH + '/fonts/weather-icons/weathericons-regular-webfont.ttf')

    # Load weather icon map file
    with open(BASE_PATH + '/icon-mapping.json') as file:
        icon_map = json.load(file)

    # Get weather forecast and conditions
    weather = Weather(api_key=config['api_key'], city=config['city'], state=config['state'])
    conditions = weather.get_conditions()
    forecast = weather.get_forecast()

    # Get current time
    now = datetime.now()

    # Load display layout
    display = uic.loadUi(BASE_PATH + '/layout.ui')

    # Update the display with weather data
    if not config['skip_weather']:
        display.high.setText('{}\N{DEGREE SIGN}'.format(forecast[0]['high']['fahrenheit']))
        display.low.setText('{}\N{DEGREE SIGN}'.format(forecast[0]['low']['fahrenheit']))
        display.temp.setText('{:.0f}\N{DEGREE SIGN}'.format(conditions['temp_f']))
        display.feels_like.setText('Feels like {:.0f}\N{DEGREE SIGN}'.format(float(conditions['feelslike_f'])))
        display.cond.setText(icon_map[conditions['icon']])
        display.percip.setText('{}%'.format(forecast[0]['pop']))
        display.weekday.setText(now.strftime('%A'))
        display.date.setText(now.strftime('%B %d'))

    # Render to image
    img = QImage(display.size(), QImage.Format_RGB888)
    display.render(QPainter(img))

    if config['outfile']:
        # Save image to file
        img.save(config['outfile'])
    else:
        # Send to e-paper display
        from epd7in5 import EPD
        epd = EPD()
        epd.init()
        epd.display_qimage(img, BLACK, RED)
        epd.sleep()


if __name__ == '__main__':
    main()
