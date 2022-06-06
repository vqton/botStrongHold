from email.policy import strict
import os
import time
from cv2 import log
import pyautogui as gui

from helpers import *


def getExecPath():

    # how to determinte x86 or x64 windows os
    exeSubPath = r'\Firefly Studios\Stronghold Kingdoms\StrongholdKingdoms.exe'
    if os.path.exists(r'C:\Program Files (x86)'):
        return r'C:\Program Files (x86)' + exeSubPath
    else:
        return r'C:\Program Files' + exeSubPath


def startapp():
    os.startfile(getExecPath())
    time.sleep(25)


def login():
    time.sleep(2)
    # boxUser = gui.locateAllOnScreen(r'images/login/user_1.png',
    # grayscale=True, confidence=0.7)

    time.sleep(2)
    posUser = gui.locateCenterOnScreen(
        r'images/login/user_1.png', grayscale=True, confidence=0.7)

    time.sleep(2)
    gui.leftClick(posUser)

    with gui.hold('ctrl'):
        gui.press('a')

    time.sleep(1)
    gui.typewrite('vuquangton@ymail.com')

    time.sleep(0.5)
    gui.press('tab')

    time.sleep(0.5)
    gui.typewrite('5319dca90')

    time.sleep(3)
    autoLogin = gui.locateCenterOnScreen(
        r'images/login/autoLoginCheck.png', grayscale=True, confidence=0.7)

    time.sleep(3)
    gui.leftClick(autoLogin)

    time.sleep(0.5)
    gui.press('enter')

    time.sleep(5)
    playGame = gui.locateCenterOnScreen(
        r'images/login/play.png', grayscale=True, confidence=0.85)

    time.sleep(3)
    gui.leftClick(playGame)


# getExecPath()

