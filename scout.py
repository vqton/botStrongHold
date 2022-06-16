from ocr import core
from functools import reduce
import os
import json
from dict2xml import dict2xml
from detectObject import detectObject
from posixpath import split
import pygetwindow as gw
import time
import pyautogui as gui
from helpers import *
from startapp import login, startapp

sText = ""
lstRes = [
    "stash",
    "apple",
    "wood",
    "stone",
    "iron",
    "cheese",
    "meat",
    "clothes",
    "bread",
]
isExisting = False
iSecondSleep = 10
TIME_LOCATING = 1
ptHome = (0, 0)
SETTING_FILENAME = "settings.json"

dctSettings = {}


def activeWndStrongHold():
    try:
        win = gw.getWindowsWithTitle("Stronghold Kingdoms - World 11")[0]
        win.activate()
        win.restore()
    except Exception as e:
        startapp()
        time.sleep(5)
        login()
        time.sleep(5)


def letGo():
    posGo = gui.locateOnScreen("images/scout/butGo.png", grayscale=True, confidence=0.7)
    time.sleep(TIME_LOCATING)
    pts = gui.center(posGo)
    clickPOS(pts)
    dctSettings["go"] = {"x": pts[0], "x": pts[1]}
    wrtJSONSettings(SETTING_FILENAME, dctSettings)
    clickPOS(ptHome)
    pass


def isNotAvailableScout():
    isavailable = detectObject(r"images\scout\zero.jpg", r"temp\sample.png")
    return isavailable


def sendScout():
    try:
        posCollect = gui.locateOnScreen(
            r"images\scout\scout.png", grayscale=True, confidence=0.7
        )
        time.sleep(TIME_LOCATING)
        pts = gui.center(posCollect)
        dctSettings["scout"] = {"x": int(pts[0]), "y": int(pts[1])}

        wrtJSONSettings(SETTING_FILENAME, dctSettings)
        clickPOS(pts)

        if isfile(r"temp\sample.png"):
            os.remove(r"temp\sample.png")

        gui.screenshot(r"temp\sample.png")
        time.sleep(TIME_LOCATING)

        isAS = isNotAvailableScout()

        if isAS == True:
            pos = gui.locateOnScreen(
                r"images/scout/closeBtn.png", grayscale=True, confidence=0.75
            )
            time.sleep(TIME_LOCATING)
            ps1 = gui.center(pos)
            # dctSettings["close"] = {"x": int(ps1[0]), "y": int(ps1[1])}
            dctSettings["close"] = {"x": 0, "y": 0}
            dctSettings["close"]["x"] = int(ps1[0])
            dctSettings["close"]["y"] = int(ps1[1])
            wrtJSONSettings(SETTING_FILENAME, dctSettings)
            clickPOS(ps1)
            time.sleep(TIME_LOCATING)

        # time.sleep(TIME_LOCATING)
        # sTime = core()
        # sec = convertTime2Secound(sTime)
        f = open(r"temp\data.txt", "w")
        # if sec.isdigit():
        #     f.write(str(sec))
        # else:
        f.write("250")
        f.close()

        time.sleep(0.5)
        letGo()
    except Exception as e:
        print(f"sendScout: {e}")
        pass


def clickWorldButton():
    try:
        time.sleep(5)
        posMapBtn = gui.locateOnScreen(
            r"images/collectRes/map.png", grayscale=True, confidence=0.75
        )
        time.sleep(TIME_LOCATING * 3)
        pts = gui.center(posMapBtn)
        print(f"Map world button: {pts}")
        dctSettings["map"] = {"x": int(pts[0]), "y": int(pts[1])}
        dctSettings["map"]["x"] = int(pts[0])
        dctSettings["map"]["y"] = int(pts[1])
        clickPOS(pts)

        wrtJSONSettings(SETTING_FILENAME, dctSettings)
    except Exception as e:
        gui.alert(e, "clickWorldButton")
        exit(1)


def getPosRes(sResource):
    sPath = "images/collectRes/" + sResource + "/"
    lstFile = getListFiles(sPath)
    for f in lstFile:
        spathRes = join(sPath, f)
        posResource = gui.locateOnScreen(spathRes, grayscale=True, confidence=0.8)
        time.sleep(TIME_LOCATING)
        if not isinstance(posResource, type(None)):
            pts = gui.center(posResource)
            print(f"Found {sResource} at {pts[0]},{pts[1]}")
            return pts


def getResourceByPos(pts):
    clickPOS(pts)
    sendScout()


def getResource(sResource):
    posResource = getPosRes(sResource)
    time.sleep(TIME_LOCATING)
    if isinstance(posResource, type(None)):
        return None
    else:
        print(f"{sResource}: ({posResource[0]},{posResource[1]})")
        clickPOS(posResource)
        sendScout()


def clickHome():
    try:

        pos = gui.locateOnScreen(r"images\\home.png", grayscale=True, confidence=0.6)
        time.sleep(1.5)
        pts = gui.center(pos)
        ptHome = pts
        print(f"Home ({pts[0]}, {pts[1]})")
        time.sleep(5)
        clickPOS(pts)
        dctSettings["home"] = {"x": 0, "y": 0}
        dctSettings["home"]["x"] = int(ptHome[0])
        dctSettings["home"]["y"] = int(ptHome[1])
        wrtJSONSettings(SETTING_FILENAME, dctSettings)
        # wrtJSonSetting('settings.json', json.dumps(dctSettings))
    except Exception as e:
        print(f"Exception clickHome {e}")


# lstRes = ['bread', 'wood']


def wrtEstTime():
    f = open(r"temp\data.txt", "w")
    f.write("0")
    f.close()


def main():
    wrtEstTime()
    activeWndStrongHold()
    clickWorldButton()
    clickHome()
    for item in lstRes:
        pts = getPosRes(item)
        if pts is not None:
            getResourceByPos(pts)
            exit(0)
    # core()
    pass


if __name__ == "__main__":
    main()
