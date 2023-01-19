import cv2


def detect_crop_images(card_images, file_path):
    image = cv2.imread(file_path)

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


card_images = []
files = ['../images/cards/cards_000_front.jpg',
         '../images/cards/cards_001_back.jpg']

for path in files:
    detect_crop_images(card_images, path)

for i, image in enumerate(card_images):
    cv2.imwrite('./test_{0}.jpg'.format(i), image)
