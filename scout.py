import os
import fnmatch
import pygetwindow as gw
import time
import pyautogui as gui
from helpers import *
from ocr import *
from startapp import login, startapp


def clickWorldButton():
    time.sleep(5)
    posMapBtn = gui.locateCenterOnScreen(
        r'images/collectRes/map.png', grayscale=True, confidence=0.5)
    time.sleep(3)
    gui.mouseDown(posMapBtn.x, posMapBtn.y, 1)
    time.sleep(0.5)
    gui.mouseUp(posMapBtn.x, posMapBtn.y, 1)

    time.sleep(5)
    gui.alert('Hello World', 'Abc')


def getResources(sResource):
    pass


def main():
    # BringWindow2Front('Stronghold Kingdoms - World 11')
    try:
        win = gw.getWindowsWithTitle('Stronghold Kingdoms - World 11')[0]
        if len(win) == 0:
            time.sleep(5)
            startapp()
            time.sleep(25)
            login()
        else:
            win.activate()
            win.restore()

        time.sleep(5)
        clickWorldButton()
        print('abc xyz')
    except gui.ImageNotFoundException:
        print('Image Not Found Exception')


if __name__ == '__main__':
    main()
