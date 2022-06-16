# Python program to illustrate
# template matching
import cv2
import numpy as np


def detectObject(obj,scene):
    # Read the main image
    img_rgb = cv2.imread(scene)

    # Convert it to grayscale
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    wrongObject = r'images\object.png'
    # Read the template
    template = cv2.imread(obj, 0)
    # template = cv2.imread(wrongObject, 0)
    # template = cv2.imread(r'images\object.png', 0)

    # Store width and height of template in w and h
    w, h = template.shape[::-1]

    # Perform match operations.
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    # Specify a threshold
    threshold = 0.9

    # Store the coordinates of matched area in a numpy array
    loc = np.where(res >= threshold)

    isExisting = False
    # Draw a rectangle around the matched region.
    
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
        isExisting=True

    # Show the final image with the matched area.
    return isExisting


# print(detectObject(r'images\zero.jpg',r'temp\sample.png'))
# print(detectObject(r'images\scout\zeroscout.png',r'temp\sample.png'))
