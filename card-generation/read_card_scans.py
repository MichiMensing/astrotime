import glob
import json
import os
import cv2
from read_card import read_back_image, read_front_image
from os import path


def detect_crop_images(file_path):
    image = cv2.imread(file_path)
    card_images = []

    # turn to binary image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thres_image = cv2.threshold(gray_image, 250, 255, cv2.THRESH_BINARY)

    # remove noice fragments by erosion and dilation
    se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
    thres_image = cv2.morphologyEx(thres_image, cv2.MORPH_CLOSE, se1)
    thres_image = cv2.morphologyEx(thres_image, cv2.MORPH_OPEN, se2)

    # find contours
    contours, _ = cv2.findContours(
        thres_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:

        # get rotated bounding box
        rect = cv2.minAreaRect(contour)
        center = rect[0]
        size = rect[1]
        angle = rect[2]

        # skip contours that are too large or small
        if size[0] > 1500 or size[0] < 500:
            continue

        center, size = tuple(map(int, center)), tuple(map(int, size))
        height, width = image.shape[0], image.shape[1]

        # rotate image around center of bounding box, correct if detected as horizontal
        if size[0] > 850:
            size = (size[1], size[0])
            angle = angle + 90
        M = cv2.getRotationMatrix2D(center, angle, 1)
        img_rot = cv2.warpAffine(image, M, (width, height))

        img_crop = cv2.getRectSubPix(img_rot, size, center)

        card_images.append(img_crop)
    return card_images


files = list(map(lambda x: os.path.join('../images/cards/', x),
                 os.listdir('../images/cards/')))

result_i18n = []
result_cards = []

if path.isdir('./detection_errors') == False:
    os.mkdir('./detection_errors')

else:
    for filename in os.listdir('./detection_errors/'):
        file_path = os.path.join('./detection_errors/', filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)

for f, path in enumerate(files):
    print('Processing file {0} of {1}'.format(f+1, len(files)))
    card_images = detect_crop_images(path)
    is_front = True if path.find('front') != -1 else False

    for i, image in enumerate(card_images):
        if is_front:
            read_front_image(image, result_i18n)
        else:
            read_back_image(image, result_cards)

print('front cards processed: {0}'.format(len(result_i18n)/5))
print('back cards processed: {0}'.format(len(result_cards)))
print('id detection errors: {0}'.format(
    len(os.listdir('./detection_errors/'))))

with open('imported_json.json', 'w', encoding='utf-8') as f:
    json.dump(result_cards, f)

with open('imported_i18n.po', 'w', encoding='utf-8') as f:
    f.write('\n'.join(result_i18n))
