import json
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
FONT = 'tahoma.ttf'
FONT_BD = 'tahomabd.ttf'
RED_MARKER = Image.open(IMAGE_PATH + 'red.png')
BLUE_MARKER = Image.open(IMAGE_PATH + 'blue.png')
GREEN_MARKER = Image.open(IMAGE_PATH + 'green.png')
YELLOW_MARKER = Image.open(IMAGE_PATH + 'yellow.png')
GREY_MARKER = Image.open(IMAGE_PATH + 'grey.png')
PURPLE_MARKER = Image.open(IMAGE_PATH + 'purple.png')

# load german by default
t = gettext.translation('base', localedir=LOCALE_DIR,
                        languages=['de'], fallback=True)
t.install()
_ = t.gettext


def generate_images():

    cards = load_cards()

    for language in LANGUAGES:
        # load language files
        t = gettext.translation('base', localedir=LOCALE_DIR,
                                languages=[language], fallback=True)
        t.install()

        generate_all_cards(language, t.gettext, cards)


def generate_all_cards(language: str, fn_gettext, cards: list):

    _ = fn_gettext
    # create target language folder
    if path.isdir(IMAGE_PATH + language) == False:
        print('creating ' + language.upper() + ' folder')
        os.mkdir(IMAGE_PATH + language)

    for card in cards:
        generate_front_card_face(card, language)
        generate_back_card_face(card, language)


def generate_front_card_face(card: dict, language):

    # load front background image
    front_image = Image.open(IMAGE_PATH + 'card_front.jpg')

    # add text to card face
    draw = ImageDraw.Draw(front_image)
    image_width = front_image.width
    image_height = front_image.height

    # show card id
    font = ImageFont.truetype(FONT, 16)
    length = draw.textlength(card['id'], font)
    draw.text(((image_width - length)/2, image_height - 75), card['id'], (255, 255, 255),
              font=font, align='center')

    # show title
    font = ImageFont.truetype(FONT_BD, 35)
    font.size = 35
    length = draw.textlength(_('card_' + card['id']+'_title'), font)
    draw.text(((image_width - length)/2, 200), _('card_' + card['id']+'_title'), (255, 255, 255),
              font=font, align='center')

    # show scenario description
    font = ImageFont.truetype(FONT, 35)
    utils.text_box(
        _('card_' + card['id']+'_desc'),
        draw,
        font,
        (110, 300, image_width - 220, image_height),
        utils.ALLIGNMENT_CENTER,
        utils.ALLIGNMENT_TOP
    )

    # save image in language folder
    front_image.save(IMAGE_PATH + language + '/' + card_name(card['id'], True))


def generate_back_card_face(card: dict, language):

    # load front background image
    back_image = Image.open(IMAGE_PATH + 'card_back.jpg')

    back_image.putalpha(255)
    if card['red']:
        back_image.paste(RED_MARKER, (0, 0), RED_MARKER)
    if card['blue']:
        back_image.paste(BLUE_MARKER, (0, 0), BLUE_MARKER)
    if card['yellow']:
        back_image.paste(YELLOW_MARKER, (0, 0), YELLOW_MARKER)
    if card['green']:
        back_image.paste(GREEN_MARKER, (0, 0), GREEN_MARKER)
    if card['grey']:
        back_image.paste(GREY_MARKER, (0, 0), GREY_MARKER)
    if card['purple']:
        back_image.paste(PURPLE_MARKER, (0, 0), PURPLE_MARKER)

    # add text to card face
    draw = ImageDraw.Draw(back_image)

    # show card id
    font = ImageFont.truetype(FONT, 16)
    length = draw.textlength(card['id'], font)
    draw.text(((back_image.width - length)/2, 100), card['id'], (255, 255, 255),
              font=font, align='center')

    # save image in language folder
    final_image = Image.new("RGB", back_image.size, (255, 255, 255))
    final_image.paste(back_image, mask=back_image.split()
                      [3])  # 3 is the alpha channel
    final_image.save(IMAGE_PATH + language + '/' +
                     card_name(card['id'], False))


def card_name(id, front: bool):
    card_name = (BACK_SUFFIX, FRONT_SUFFIX)[front]
    return id + card_name + '.jpg'


def load_cards():
    f = open('cards.json')
    cards = json.load(f)
    f.close()
    return cards


generate_images()
