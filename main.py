from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import epd2in7b

DISP_SIZE = (264, 176)

DISP_PALETTE = [
    255, 255, 255,
      0,   0,   0,
    255,   0,   0
]

WHITE = 0
BLACK = 1
RED = 2


def create_frame(image):
    width, height = image.size
    pixels = image.load()
    frame_black = [0] * int(width * height / 8)
    frame_red = [0] * int(width * height / 8)

    for y in range(0, height):
        for x in range(0, width):
            if pixels[x, y] == BLACK:
                frame_black[int((x + y * width) / 8)] |= 0x80 >> (x % 8)
            elif pixels[x, y] == RED:
                frame_red[int((x + y * width) / 8)] |= 0x80 >> (x % 8)

    return frame_black, frame_red


def main():
    font = ImageFont.truetype('fonts/gnu-freefont-freemono/FreeMonoBold.ttf', 32)
    font_large = ImageFont.truetype('fonts/gnu-freefont-freemono/FreeMonoBold.ttf', 48)

    im = Image.new('P', DISP_SIZE)
    im.putpalette(DISP_PALETTE)

    now = datetime.now()

    draw = ImageDraw.ImageDraw(im)
    draw.text((0, 40), now.strftime('%A'), BLACK, font_large)
    draw.text((0, 88), now.strftime('%B %d'), BLACK, font)

    rot = im.transpose(Image.ROTATE_90)
    rot.show()

    frame_black, frame_red = create_frame(rot)

    epd = epd2in7b.EPD()
    epd.init()
    epd.display_frame(frame_black, frame_red)


if __name__ == '__main__':
    main()
