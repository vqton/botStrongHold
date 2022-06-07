import cv2
import numpy as np
import os
import pytesseract


def getSection(_object, _template):
    img = cv2.imread(_object)
    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(_template, 0)
    w, h = template.shape[1], template.shape[0]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    THRESHOLD = 0.75
    loc = np.where(res >= THRESHOLD)

    # Draw boudning box
    for y, x in zip(loc[0], loc[1]):
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
        crop_img = img[y:y + h, x:x+w]
    if os.path.isfile('temp/crop.jpg'):
        os.remove('temp/crop.jpg')
    cv2.imwrite('temp/crop.jpg',crop_img)
  

def main():
    getSection('temp/sample.png', 'images/collectRes/object.png')


if __name__ == '__main__':
    main()
