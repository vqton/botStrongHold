from os import path
import yaml
import logging
import logging.config
import numpy as np
import pytesseract
import cv2
import re
from helpers import convertTime2Second


with open(r"config.yaml", "r") as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)


def extractText(imagePath):
    if path.isfile(imagePath) == False:
        logger.info(f"File {imagePath} not exist.")
        exit(0)

    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

    # Load image, grayscale, Otsu's threshold
    image = cv2.imread(imagePath)
    image = cv2.resize(image, None, fx=4.8, fy=4.8, interpolation=cv2.INTER_BITS2)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph open to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    # Find contours and remove small noise
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 50:
            cv2.drawContours(opening, [c], -1, 0, -1)

    # Invert and apply slight Gaussian blur
    result = 255 - opening
    result = cv2.GaussianBlur(result, (3, 3), 0)

    # Perform OCR
    data = pytesseract.image_to_string(result, lang="eng", config="--psm 6")
    # print(data)
    # result = re.sub("[^A-Za-z0-9]+", "", data)
    result = re.sub("[^0-9]+", "", data)
    if len(result) == 3:
        logger.info(f"Raw result {result}")
        return "0" + result

    logger.info(f"Final result {result}")
    return result


# extractText(r"temp/crop.jpg")
