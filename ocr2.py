import cv2
from pytesseract import pytesseract
import numpy as np


img = cv2.imread(r"temp/crop.jpg")

img = cv2.resize(img, None, fx=1.8, fy=1.8, interpolation=cv2.INTER_CUBIC)

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

kernel = np.ones((1, 1), np.uint8)
img = cv2.dilate(img, kernel, iterations=1)
img = cv2.erode(img, kernel, iterations=1)

cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
data = pytesseract.image_to_string(img, lang="eng", config="--psm 6")

cv2.imshow("dec", img)
cv2.waitKey()
cv2.destroyAllWindows()

print(data)
