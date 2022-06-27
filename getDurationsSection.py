from genericpath import exists
import cv2
import numpy as np
import os
import yaml
import pytesseract
import logging
import logging.config

with open(r"config.yaml", "r") as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)


def getSection(_scene, _template):
    isFound = False
    img = cv2.imread(_scene, 1)
    logger.info(f"{_scene}")

    # Convert to grayscale
    # img = cv2.resize(img, None, fx=0.8, fy=0.8, interpolation=cv2.INTER_CUBIC)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(_template, 0)
    w, h = template.shape[1], template.shape[0]
    # w, h = template.shape[:-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    THRESHOLD = 0.7
    loc = np.where(res >= THRESHOLD)

    crop_img = None
    # Draw boudning box
    for y, x in zip(loc[0], loc[1]):
        isFound = True
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
        crop_img = img[y : y + h, x : x + w]

    if isFound:
        cv2.imwrite(r"temp/crop.jpg", crop_img)
    else:
        logger.info(f"There is nothing")
    # if os.path.isfile('temp/crop.jpg'):
    #     os.remove('temp/crop.jpg')


# def main():
#     logging.basicConfig(filename="myapp.log", level=logging.INFO)
#     logging.info("Started")

#     if os.path.isfile(r"temp/sample.png") and os.path.isfile(
#         r"images/collectRes/object.jpg"
#     ):
#         getSection(r"temp/sample.png", r"images/collectRes/object.png")
#     else:
#         exit(1)
#     logging.info("Finished")


# if __name__ == "__main__":
#     main()
