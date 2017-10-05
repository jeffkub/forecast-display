import argparse
from datetime import datetime
import json
import os
from PIL import Image, ImageDraw, ImageFont
from weather import Weather

DISP_SIZE = (640, 384)

DISP_PALETTE = [
    255, 255, 255,
      0,   0,   0,
    255,   0,   0
]

WHITE = 0
BLACK = 1
RED = 2

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def get_config():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_file', '-c', default=BASE_PATH + '/config.json')
    parser.add_argument('--debug_show', action='store_true')
    args = vars(parser.parse_args())

    # Parse from config file
    with open(args['config_file']) as file:
        json_data = json.load(file)
        args.update(json_data)

    return args


def center_text(draw, xy, box, text, fill, font):
    text_size = draw.textsize(text, font)
    pos = tuple(map(lambda pos, box, text_size: pos + (box - text_size)/2, xy, box, text_size))
    draw.text(pos, text, fill, font)


def main():
    config = get_config()

    font = ImageFont.truetype(BASE_PATH + '/fonts/freefont/FreeMonoBold.ttf', 72)
    font_large = ImageFont.truetype(BASE_PATH + '/fonts/freefont/FreeMonoBold.ttf', 110)

    weather = Weather(api_key=config['api_key'], city=config['city'], state=config['state'])
    print(weather.get_conditions())

    im = Image.new('P', DISP_SIZE)
    im.putpalette(DISP_PALETTE)

    now = datetime.now()

    draw = ImageDraw.ImageDraw(im)
    center_text(draw, (0, 80), (640, 110), now.strftime('%A'), BLACK, font_large)
    center_text(draw, (0, 200), (640, 72), now.strftime('%B %d'), RED, font)

    if config['debug_show']:
        # Show image in a window for debugging
        im.show()
    else:
        # Show on e-paper display
        from epd7in5 import EPD
        epd = EPD()
        epd.init()
        epd.display_image(im, BLACK, RED)
        epd.sleep()


if __name__ == '__main__':
    main()
