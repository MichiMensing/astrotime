
from PIL import Image
from math import sqrt
from import_from_excel import generate_i18n_files
from pytesseract import pytesseract
import uuid

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


def read_front_image(image_path, result_i18n):
    image = Image.open(image_path)

    # crop image to text area
    height = image.height
    width = image.width
    margin = 75
    text_area_image = image.crop((margin, margin, width-margin, height-margin))

    # read title and scenario
    text = pytesseract.image_to_string(text_area_image, lang='deu')
    text_array = str.splitlines(text)
    title = text_array.pop(0)
    scenario = ' '.join(text_array).strip()

    # read id
    id_area_image = image.crop(
        (4*margin, height-1.5*margin, width-4.1*margin, height-0.5*margin))
    id = read_id_number(id_area_image)

    generate_i18n_files((id, title, scenario), result_i18n)


def read_back_image(image_path, result_cards):
    image = Image.open(image_path)
    card = get_default_card()

    # crop image to text area
    width = image.width
    margin = 75
    id_area_image = image.crop(
        (4.1*margin, 0.7*margin, width-4.2*margin, 1.7*margin))

    # read id
    card['id'] = read_id_number(id_area_image)

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
    pix = image.getpixel(coordinates)
    image.putpixel(coordinates, (0, 255, 0))

    # euclidean distance
    d = sqrt(pow(pix[0] - color[0], 2) + pow(pix[1] -
             color[1], 2) + pow(pix[2] - color[2], 2))
    return True if d < 40 else False


def read_id_number(image) -> str:
    # grayscale
    id_area_image = image.convert('L')
    # Threshold
    id_area_image = id_area_image.point(lambda p: 255 if p > 100 else 0)
    # To mono
    id_area_image = id_area_image.convert('1')

    id_text = pytesseract.image_to_string(
        id_area_image, lang='eng', config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
    id_area_image.save('crop.jpg')

    return ''.join(id_text).strip() if id_text != '' else str(uuid.uuid4())


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


result_i18n = []
read_front_image('./test_0.jpg', result_i18n)
result_cards = []
read_back_image('./test_11.jpg', result_cards)

print(result_i18n)
print(result_cards)
