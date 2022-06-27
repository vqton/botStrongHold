import cv2
import numpy as np
import os
import re
from os import path
import pytesseract
from imgPreprocessing import *
from getDurationsSection import getSection

# get grayscale image


# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


def core():
    if os.path.isdir("./temp") == False:
        os.mkdir("./temp")
    # getSection('temp/sample.jpg', 'images/collectRes/object.png')
    image = cv2.imread(r"temp/crop.jpg")
    # image = cv2.imread('aurebesh.jpg')
    gray = get_grayscale(image)
    # thresh =
    thresholding(gray)
    # opening =
    opening(gray)
    # canny =
    canny(gray)
    pytesseract.pytesseract.tesseract_cmd = (
        "C:/Program Files/Tesseract-OCR/tesseract.exe"
    )
    text = pytesseract.image_to_string(image, config="--psm 6")
    # print(re.sub("[^0-9]+", "", text))
    return re.sub("[^0-9]+", "", text)


# core()
# clickHome
