import os
from os import path
from PIL import Image
import gettext
from pathlib import Path

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

    # load front background image
    front_image = Image.open(IMAGE_PATH + 'card_front.jpg')

    print(LOCALE_DIR)

    for language in LANGUAGES:
        # load language files
        t = gettext.translation('base', localedir=LOCALE_DIR,
                                languages=[language], fallback=True)
        t.install()
        generate_all_cards(language, front_image, t.gettext)


def generate_all_cards(language: str, front_image, fn_gettext):

    _ = fn_gettext
    # create target language folder
    if path.isdir(IMAGE_PATH + language) == False:
        print('creating ' + language.upper() + ' folder')
        os.mkdir(IMAGE_PATH + language)

    # add text to card face
    print(_('card_219_title'))
    print(_('card_219_desc'))

    # save image in language folder
    front_image.save(IMAGE_PATH + language + '/' + card_name('219', True))

# generate card file name


def card_name(id, front: bool):
    card_name = (BACK_SUFFIX, FRONT_SUFFIX)[front]
    return id + card_name + '.jpg'


generate_images()
