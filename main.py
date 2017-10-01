import argparse
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

DISP_SIZE = (264, 176)

DISP_PALETTE = [
    255, 255, 255,
      0,   0,   0,
    255,   0,   0
]

WHITE = 0
BLACK = 1
RED = 2


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug_show', action='store_true')

    args = parser.parse_args()

    font = ImageFont.truetype('fonts/freefont/FreeMonoBold.ttf', 32)
    font_large = ImageFont.truetype('fonts/freefont/FreeMonoBold.ttf', 48)

    im = Image.new('P', DISP_SIZE)
    im.putpalette(DISP_PALETTE)

    now = datetime.now()

    draw = ImageDraw.ImageDraw(im)
    draw.text((0, 40), now.strftime('%A'), BLACK, font_large)
    draw.text((0, 88), now.strftime('%B %d'), RED, font)

    if args.debug_show:
        # Show image in a window for debugging
        im.show()
    else:
        # Show on e-paper display
        import epd2in7b
        epd = epd2in7b.EPD()
        epd.init()
        epd.display_image(im.transpose(Image.ROTATE_90), BLACK, RED)
        epd.sleep()


if __name__ == '__main__':
    main()
