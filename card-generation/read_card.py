
from math import sqrt
from import_from_excel import generate_i18n_files
from pytesseract import pytesseract
import uuid
import cv2

path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract_cmd = path_to_tesseract

# color id, coordinates, color rgb
COLOR_ARRAY = [
    ('green', (60, 120), (53, 150, 53)),
    ('red', (150, 120), (191, 32, 29)),
    ('yellow', (210, 120), (255, 248, 79)),
    ('purple', (510, 120), (114, 78, 124)),
    ('grey', (570, 120), (204, 230, 195)),
    ('blue', (640, 120), (47, 164, 218))
]

ATTRIBUTE_COLOR = (254, 247, 96)


def read_front_image(image, result_i18n):

    # crop image to text area
    height, width = image.shape[0], image.shape[1]
    margin = 75
    text_area_image = image[margin:height-margin, margin: width-margin].copy()

    # read title and scenario
    text = pytesseract.image_to_string(text_area_image, lang='deu')
    text_array = str.splitlines(text)
    title = text_array.pop(0)
    scenario = ' '.join(text_array).strip()

    # read id
    id_area_image = image[int(height-1.5*margin):int(height -
                          0.5*margin), int(4*margin):int(width-4.1*margin)].copy()
    id = read_id_number(id_area_image, True)

    generate_i18n_files((id, title, scenario), result_i18n)


def read_back_image(image, result_cards):
    card = get_default_card()

    # crop image to text area
    width = image.shape[1]
    margin = 75
    id_area_image = image[int(0.7*margin):int(1.7*margin), int(
                          4.1*margin):int(width-4.2*margin)].copy()

    # read id
    card['id'] = read_id_number(id_area_image, False)

    # read color markers
    for id, coords, color in COLOR_ARRAY:
        card[id] = is_color_present(image, coords, color)

    # read attribute pattern
    band_height = 73
    mid_offset = 30
    for i in range(20):
        row = i % 10
        if i < 10:
            x1 = 200
        else:
            x1 = 550
        if i % 10 < 5:
            y1 = 200 + row * band_height
        else:
            y1 = 200 + row * band_height + mid_offset
        card['attr_'+str(i)] = is_color_present(image,
                                                (x1, y1), ATTRIBUTE_COLOR)

    result_cards.append(card)


def is_color_present(image, coordinates, color) -> bool:
    b, g, r = image[coordinates[1], coordinates[0]]

    # euclidean distance
    d = sqrt(pow(r - color[0], 2) + pow(g -
             color[1], 2) + pow(b - color[2], 2))
    return True if d < 40 else False


def read_id_number(image, is_front) -> str:
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thres_image = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY)

    id_text = pytesseract.image_to_string(
        thres_image, lang='eng', config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')

    id = ''
    if id_text != '':
        id = ''.join(id_text).strip()
    else:
        id = str(uuid.uuid4())
        cv2.imwrite(
            './detection_errors/{0}_{1}.jpg'.format(id, 'front 'if is_front else 'back'), image)

    return id


def get_default_card():
    return {
        "id": '',
        "red": False,
        "yellow": False,
        "green": False,
        "blue": False,
        "grey": False,
        "purple": False,
        "attr_0": False,
        "attr_1": False,
        "attr_2": False,
        "attr_3": False,
        "attr_4": False,
        "attr_5": False,
        "attr_6": False,
        "attr_7": False,
        "attr_8": False,
        "attr_9": False,
        "attr_10": False,
        "attr_11": False,
        "attr_12": False,
        "attr_13": False,
        "attr_14": False,
        "attr_15": False,
        "attr_16": False,
        "attr_17": False,
        "attr_18": False,
        "attr_19": False
    }
