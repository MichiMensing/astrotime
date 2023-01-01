import os
from os import path
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import gettext
from pathlib import Path
import utils

# constants
LANGUAGES = ['de', 'en']
IMAGE_PATH = '../images/'
FRONT_SUFFIX = '_front'
BACK_SUFFIX = '_back'
LOCALE_DIR = Path(__file__).resolve().parent.parent / 'locales'

# load german by default
t = gettext.translation('base', localedir=LOCALE_DIR,
                        languages=['de'], fallback=True)
t.install()
_ = t.gettext


def generate_images():

    for language in LANGUAGES:
        # load language files
        t = gettext.translation('base', localedir=LOCALE_DIR,
                                languages=[language], fallback=True)
        t.install()

        # load front background image
        front_image = Image.open(IMAGE_PATH + 'card_front.jpg')
        generate_all_cards(language, front_image, t.gettext)


def generate_all_cards(language: str, front_image: Image, fn_gettext):

    _ = fn_gettext
    # create target language folder
    if path.isdir(IMAGE_PATH + language) == False:
        print('creating ' + language.upper() + ' folder')
        os.mkdir(IMAGE_PATH + language)

    # add text to card face

    draw = ImageDraw.Draw(front_image)
    image_width = front_image.width
    image_height = front_image.height

    # show card id
    font = ImageFont.truetype("tahoma.ttf", 16)
    length = draw.textlength('219', font)
    draw.text(((image_width - length)/2, image_height - 75), "219", (255, 255, 255),
              font=font, align='center')

    # show title
    font = ImageFont.truetype("tahomabd.ttf", 35)
    length = draw.textlength(_('card_219_title'), font)
    draw.text(((image_width - length)/2, 200), _('card_219_title'), (255, 255, 255),
              font=font, align='center')

    # show scenario description
    font = ImageFont.truetype("tahoma.ttf", 35)
    utils.text_box(
        _('card_219_desc'),
        draw,
        font,
        (110, 300, image_width - 220, image_height),
        utils.ALLIGNMENT_CENTER,
        utils.ALLIGNMENT_TOP
    )

    # save image in language folder
    front_image.save(IMAGE_PATH + language + '/' + card_name('219', True))

# generate card file name


def card_name(id, front: bool):
    card_name = (BACK_SUFFIX, FRONT_SUFFIX)[front]
    return id + card_name + '.jpg'


generate_images()
