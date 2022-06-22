from pandas import ExcelWriter
from requests import get
from extractText import extractText
from getDurationsSection import getSection
from ocr import core
from functools import reduce
import os
import logging
import logging.config
import json
from dict2xml import dict2xml
from detectObject import detectObject
from posixpath import split
import pygetwindow as gw
import time
import pyautogui as gui
from helpers import *
from startapp import login, startapp

logging.config.fileConfig(fname="log.config", disable_existing_loggers=False)
logger = logging.getLogger(__name__)
sText = ""
lstRes = [
    "stash",
    "fish",
    "veg",
    "salt",
    "apple",
    "wood",
    "stone",
    "iron",
    "cheese",
    "meat",
    "clothes",
    "bread",
    "wine",
    "furniture",
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
    try:
        if "go" not in dctSettings:
            posGo = gui.locateOnScreen(
                "images/scout/butGo.png", grayscale=True, confidence=0.7
            )
            time.sleep(TIME_LOCATING)
            pts = gui.center(posGo)
            clickPOS(pts)
            dctSettings["go"] = f"{ int(pts[0])}, {int(pts[1])}"
            wrtJSONSettings(SETTING_FILENAME, dctSettings)
        else:
            pts = parseString2Tuple(dctSettings["go"])
            logger.info(f"Let go: {pts}")
            clickPOS(pts)
    except Exception as e:
        print(f"letGo: {e}")
        logger.debug(f"letGo: {e}")

    pass


def isNotAvailableScout():
    isavailable = detectObject(r"images\scout\zero.jpg", r"temp\sample.png")
    return isavailable


def sendScout():

    try:
        if "scout" not in dctSettings:
            posCollect = gui.locateOnScreen(
                r"images\scout\scout.png", grayscale=True, confidence=0.7
            )
            time.sleep(TIME_LOCATING)
            pts = gui.center(posCollect)
            dctSettings["scout"] = f"{int(pts[0])}, {int(pts[1])}"

            wrtJSONSettings(SETTING_FILENAME, dctSettings)
        else:
            pt = dctSettings["scout"]
            pts = parseString2Tuple(pt)
        clickPOS(pts)

        clickPOS(pts)
        if isfile(r"temp\sample.png"):
            os.remove(r"temp\sample.png")
        gui.screenshot(r"temp\sample.png")
        time.sleep(TIME_LOCATING)

        isAS = isNotAvailableScout()
        if isAS == True:
            if "close" not in dctSettings:
                pos = gui.locateOnScreen(
                    r"images/scout/closeBtn.png", grayscale=True, confidence=0.75
                )
                time.sleep(TIME_LOCATING)
                ps1 = gui.center(pos)
                dctSettings["close"] = f"{int(ps1[0])}, {int(ps1[1])}"
                wrtJSONSettings(SETTING_FILENAME, dctSettings)
                clickPOS(ps1)
                print(f" in {ps1}")
            else:
                ps1 = parseString2Tuple(dctSettings["close"])
                clickPOS(ps1)
                print(f" not in {ps1}")
            time.sleep(TIME_LOCATING)

        with open(r"temp\data.txt", "w") as f:
            sTime = extractText(r"temp\crop.jpg")
            second = convertTime2Second(sTime)
            f.write(str(second))

        letGo()
    except Exception as e:
        print(f"sendScout: {e}")
        logger.debug(f"sendScout: {e}")
        pass


def clickWorldButton():
    try:
        if "map" in dctSettings:
            ptsHome = parseString2Tuple(dctSettings["map"])
            clickPOS(ptsHome)
        else:
            time.sleep(5)
            posMapBtn = gui.locateOnScreen(
                r"images/collectRes/map.png", grayscale=True, confidence=0.75
            )
            time.sleep(TIME_LOCATING * 3)
            pts = gui.center(posMapBtn)
            print(f"Map world button: {pts}")
            dctSettings["map"] = f"{int(pts[0])}, {int(pts[1])}"
            clickPOS(pts)
            wrtJSONSettings(SETTING_FILENAME, dctSettings)
    except Exception as e:
        gui.alert(e, "clickWorldButton")
        logger.debug(f"clickWorldButton: {e}")
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
    try:
        clickPOS(pts)
        sendScout()
    except Exception as e:
        print(f"getResourceByPos: {e}")
        logger.debug(f"getResourceByPos: {e}")


def getResource(sResource):
    posResource = getPosRes(sResource)
    time.sleep(TIME_LOCATING)
    if isinstance(posResource, type(None)):
        return None
    else:
        print(f"{sResource}: ({posResource[0]},{posResource[1]})")
        clickPOS(posResource)
        sendScout()


def searchCaptital():
    try:
        bxCap = gui.locateOnScreen(
            r"images/capital1.png", grayscale=True, confidence=0.7
        )
        time.sleep(2)
        pts = gui.center(bxCap)
        clickPOS(pts)
    except Exception as e:
        gui.alert(e, "Search Capital")
        logger.debug(e)
        exit(1)
    pass


def clickHome():
    try:
        if "select" not in dctSettings:
            box = gui.locateOnScreen(
                r"images\\select.png", grayscale=True, confidence=0.8
            )
            time.sleep(2)
            pos = gui.center(box)
            gui.moveTo(pos[0], pos[1], 0.5)
            dctSettings["select"] = f"{int(pos[0])}, {int(pos[1])}"
            wrtJSONSettings(SETTING_FILENAME, dctSettings)
            clickPOS(pos)
            gui.screenshot(r"temp\scene.png")
        else:
            pos = parseString2Tuple(dctSettings["select"])
            clickPOS(pos)
        gui.screenshot(r"temp\scene.png")
        blCheck = detectObject(r"images\home2.png", r"temp\scene.png")
        while blCheck == False:
            gui.click(pos)
            gui.screenshot(r"temp\scene.png")
            blCheck = detectObject(r"images\home2.png", r"temp\scene.png")
    except Exception as e:
        gui.alert(e, "clickHome Exception")
        print(f"Exception clickHome {e}")
        logger.debug(f"Exception clickHome {e}")


def wrtEstTime():
    with open(r"temp\data.txt", "w") as f:
        f.write("0")
        f.close()


def main():

    # Get the logger specified in the file

    wrtEstTime()
    activeWndStrongHold()
    clickWorldButton()
    clickHome()
    searchCaptital()
    # gui.dragTo(50, 50, duration=0.5)
    for item in lstRes:
        print(item)
        pts = getPosRes(item)
        if pts is not None:
            logger.info(f"Found {item} at {pts[0]},{pts[1]}")
            while True:
                getResourceByPos(pts)
                if isfile(r"temp/crop.jpg") == False:
                    getSection(r"temp/sample.png", r"images/object.png")
                sTime = extractText(r"temp/crop.jpg")
                sec = convertTime2Second(sTime)
                print(f"Second: {sec}")
                clickHome()
                gui.screenshot(r"temp/scene.png")
                time.sleep(1)
                for x in getListFiles(r"images/collectRes/" + item):
                    imgPath = r"images/collectRes/" + item + "/" + x
                    logger.info(f"Checking {imgPath}")
                    isExisting = detectObject(imgPath, r"temp/scene.png")
                if isExisting == False:
                    break
                clickHome()
                time.sleep(int(sec))

    pass


if __name__ == "__main__":
    if len(dctSettings) == 0:
        with open(SETTING_FILENAME, "r") as f:
            dctSettings = json.loads(f.read())
            print(dctSettings)

    main()
