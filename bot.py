import cv2
from django.urls import clear_script_prefix
import numpy as np
import pyautogui as gui
import time

# stash_img = cv2.imread('images\\apple.png', cv2.IMREAD_UNCHANGED)
# map_img = cv2.imread('images\\test.png', cv2.IMREAD_UNCHANGED)


# # cv2.imshow('stash', stash_img)
# # cv2.waitKey()
# # cv2.destroyAllWindows()


# # cv2.imshow('map', map_img)
# # cv2.waitKey()
# # cv2.destroyAllWindows()


# result = cv2.matchTemplate(stash_img, map_img, cv2.TM_CCOEFF_NORMED)


# # cv2.imshow('Result', result)
# # cv2.waitKey()
# # cv2.destroyAllWindows


# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# w = stash_img.shape[1]
# h = stash_img.shape[0]

# cv2.rectangle(map_img, max_loc,
#               (max_loc[0] + w, max_loc[1] + h), (0, 255, 255), 2)

# threshold = .60


# yloc, xloc = np.where(result >= threshold)


# for (x, y) in zip(xloc, yloc):
#     cv2.rectangle(map_img, (x, y), (x + w, y + h), (0, 255, 255), 2)


# rectangles = []
# for (x, y) in zip(xloc, yloc):
#     rectangles.append([int(x), int(y), int(w), int(h)])
#     rectangles.append([int(x), int(y), int(w), int(h)])

# rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

# cv2.putText(map_img, text='Arnold', org=(max_loc[0], max_loc[1]),
#             fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(0, 0, 0),
#             thickness=2, lineType=cv2.LINE_AA)


# cv2.imshow('map', map_img)

# cv2.waitKey()
# cv2.destroyAllWindows()
def sendScout():
    posScout = gui.locateOnScreen(
        'E:/botStrongHold/images/scout.png', grayscale=True, confidence=0.8)
    time.sleep(5)
    ptsScout = gui.center(posScout)
    time.sleep(2)
    gui.moveTo(ptsScout.x, ptsScout.y, 1)
    time.sleep(2)
    gui.mouseDown(ptsScout.x, ptsScout.y)
    time.sleep(2)
    gui.mouseUp(ptsScout.x, ptsScout.y)


# def PressCheckOK():
#     posCheckOK = gui.locateOnScreen(
#         'E:/botStrongHold/images/checkOK.png', grayscale=True, confidence=0.8)
#     time.sleep(5)
#     pts = gui.center(posCheckOK)
#     time.sleep(5)
#     gui.moveTo(pts.x, pts.y)
#     time.sleep(2)
#     gui.mouseDown(pts.x, pts.y)
#     time.sleep(2)
#     gui.mouseUp(pts.x, pts.y)
#     # gui.click('E:/botStrongHold/images/checkOK.png')
#     time.sleep(1)
#     PressGo()


def PressGo():
    posGO = gui.locateOnScreen(
        'E:/botStrongHold/images/butGo.png', grayscale=True, confidence=0.8)
    time.sleep(5)
    pts = gui.center(posGO)
    time.sleep(5)
    gui.moveTo(pts.x, pts.y)
    time.sleep(2)
    gui.mouseDown(pts.x, pts.y)
    time.sleep(2)
    gui.mouseUp(pts.x, pts.y)
    # gui.click('E:/botStrongHold/images/checkOK.png')
    time.sleep(1)

try:
    time.sleep(2)
    pos = gui.locateOnScreen(
        'E:/botStrongHold/images/apple.png', grayscale=True, confidence=0.8)
    time.sleep(5)
    pts = gui.center(pos)
    gui.moveTo(pts.x, pts.y)
    time.sleep(2)
    gui.mouseDown(pts.x, pts.y)
    time.sleep(2)
    gui.mouseUp(pts.x, pts.y)
    time.sleep(2)
    sendScout()
    time.sleep(2)
    PressGo()
except gui.ImageNotFoundException:
    print("An exception occurred")


# pyautogui.click('images\\apple.png')
# pyautogui.moveTo(max_loc[0], max_loc[1], 5)
