from genericpath import exists
import cv2
import numpy as np
import os
import pytesseract
import logging


def getSection(_object, _template):
    img = cv2.imread(_object, 1)
    print(_object)
    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(_template, 0)
    w, h = template.shape[1], template.shape[0]
    # w, h = template.shape[:-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    THRESHOLD = 0.73
    loc = np.where(res >= THRESHOLD)

    crop_img = None
    # Draw boudning box
    for y, x in zip(loc[0], loc[1]):
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
        crop_img = img[y : y + h, x : x + w]

    cv2.imwrite("temp/crop.jpg", crop_img)

    # if os.path.isfile('temp/crop.jpg'):
    #     os.remove('temp/crop.jpg')


def main():
    logging.basicConfig(filename="myapp.log", level=logging.INFO)
    logging.info("Started")

    if os.path.isfile(r"temp/sample.png") and os.path.isfile(
        r"images/collectRes/object.jpg"
    ):
        getSection(r"temp/sample.png", r"images/collectRes/object.png")
    else:
        exit(1)
    logging.info("Finished")


if __name__ == "__main__":
    main()
