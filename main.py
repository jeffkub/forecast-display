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

def center_text(draw, xy, box, text, fill, font):
    text_size = draw.textsize(text, font)
    pos = tuple(map(lambda pos, box, text_size: pos + (box - text_size)/2, xy, box, text_size))
    draw.text(pos, text, fill, font)

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
    center_text(draw, (0, 40), (264, 48), now.strftime('%A'), BLACK, font_large)
    center_text(draw, (0, 88), (264, 32), now.strftime('%B %d'), RED, font)

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
