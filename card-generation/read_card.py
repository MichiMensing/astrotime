
from PIL import Image
from pytesseract import pytesseract

path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract_cmd = path_to_tesseract

# color id, coordinates, color rgb
COLOR_ARRAY = [('red', (60, 120), (173, 15, 14)),
               ('yellow', (150, 120), (239, 199, 3)),
               ('green', (210, 120), (1, 155, 33)),
               ('blue', (510, 120), (84, 154, 250)),
               ('grey', (570, 120), (131, 131, 131)),
               ('purple', (640, 120), (106, 0, 154))]

ATTRIBUTE_COLOR = (239, 199, 3)


def read_front_image(image_path):
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

    print(title + ' - ' + scenario)

    # read id
    id_area_image = image.crop(
        (4*margin, height-1.5*margin, width-4*margin, height-0.5*margin))

    id_text = pytesseract.image_to_string(id_area_image, lang='deu')
    id = ''.join(id_text).strip()
    print(id)


def read_back_image(image_path):
    image = Image.open(image_path)
    card = get_default_card()

    # crop image to text area
    width = image.width
    margin = 75
    id_area_image = image.crop(
        (4*margin, 0.5*margin, width-4*margin, 2*margin))

    # read id
    id_text = pytesseract.image_to_string(id_area_image, lang='deu')
    card['id'] = id_text

    # read color markers
    for id, coords, color in COLOR_ARRAY:
        card[id] = is_color_present(image, coords, color)

    # read attribute pattern
    band_height = 71
    mid_offset = 20
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

    print(card)
    return card


def is_color_present(image, coordinates, color) -> bool:
    pix = image.getpixel(coordinates)
    return True if pix == color else False


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


read_front_image('../images/de/1_front.jpg')
read_back_image('../images/de/4_back.jpg')
