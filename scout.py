from requests import get
from extractText import extractText
from getDurationsSection import getSection
from ocr import core
from functools import reduce
import os
from os import path
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
import yaml

matchTemplateImagePath = ""
sText = ""
lstRes = [
    "stash",
    "apple",
    "fish",
    "meat",
    "veg",
    "salt",
    "cheese",
    "bread",
    "wood",
    "stone",
    "iron",
    "clothes",
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
        if path.exists(r"temp\sample.png"):
            os.remove(r"temp\sample.png")
        gui.screenshot(r"temp\sample.png")
        time.sleep(TIME_LOCATING)
        getSection(r"temp\sample.png", r"images\object.png")
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
            else:
                ps1 = parseString2Tuple(dctSettings["close"])
                clickPOS(ps1)
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


def clickCapital():
    try:
        if "capital" not in dctSettings:
            bxCap = gui.locateOnScreen(
                r"E:\botStrongHold\images\capital.png", grayscale=True, confidence=0.5
            )
            time.sleep(TIME_LOCATING * 2)
            pts = gui.center(bxCap)
            logger.info(f"Capital at {pts}")
            dctSettings["capital"] = f"{int(pts[0])}, {int(pts[1])}"
            wrtJSONSettings(SETTING_FILENAME, dctSettings)
            clickPOS(pts)
        else:
            pts = parseString2Tuple(dctSettings["capital"])
            clickPOS(pts)
    except Exception as e:
        logger.debug(f"Click capital error message {e}")
        exit(1)


def getPosRes(sResource):
    sPath = "images/collectRes/" + sResource + "/"
    lstFile = getListFiles(sPath)
    for f in lstFile:
        spathRes = join(sPath, f)
        posResource = gui.locateOnScreen(spathRes, grayscale=True, confidence=0.8)
        time.sleep(TIME_LOCATING)
        if not isinstance(posResource, type(None)):
            # matchTemplateImagePath = spathRes
            with open(r"temp/abc.txt", "w") as fp:
                fp.write(str(spathRes))
            pts = gui.center(posResource)
            logger.info(f"Found {spathRes} - {sResource} at {pts[0]},{pts[1]}")
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
        f.write(str(0))


def main():

    # Get the logger specified in the file
    round = 0
    if "screen" not in dctSettings:
        pts = gui.size()
        dctSettings["screen"] = f"{int(pts[0])}, {int(pts[1])}"
        wrtJSONSettings(SETTING_FILENAME, dctSettings)
    wrtEstTime()
    activeWndStrongHold()
    clickWorldButton()
    clickHome()
    clickCapital()
    # gui.dragTo(45, 500, duration=0.5)
    gui.moveTo(849, 449, 1)

    while round < 3:
        gui.scroll(round)
        for item in lstRes:
            logger.info(f"Looking for {item}")
            # print(item)
            pts = getPosRes(item)
            if pts is not None:
                logger.info(f"Found {item} at {pts[0]},{pts[1]}")
                while True:
                    activeWndStrongHold()
                    getResourceByPos(pts)
                    sTime = extractText(r"temp/crop.jpg")
                    sec = convertTime2Second(sTime)
                    with open(r"temp/data.txt", "w") as fp:
                        fp.write(str(sec))
                    clickHome()
                    clickCapital()
                    gui.screenshot(r"temp/scene.png")
                    with open(r"temp/abc.txt", "r") as f:
                        imgPath = f.readline()
                    # imgPath = matchTemplateImagePath
                    logger.info(f"Checking {imgPath}")
                    isExisting = detectObject(imgPath, r"temp/scene.png")
                    logger.debug(f"{imgPath}")
                    if isExisting == False:
                        break
                    clickHome()
                    logger.info(f"Next scouting start in {sec} seconds")
                    time.sleep(int(sec))
    round += 1
    pass


if __name__ == "__main__":
    # initialization logging
    with open(r"config.yaml", "r") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
        logging.config.dictConfig(config)
        logger = logging.getLogger(__name__)
    if os.path.isdir("temp") == False:
        os.makedirs("temp")
    if isfile(SETTING_FILENAME) == False:
        wrtJSONSettings(SETTING_FILENAME, {})
    if len(dctSettings) == 0:
        with open(SETTING_FILENAME, "r") as f:
            dctSettings = json.loads(f.read())
            logger.info(dctSettings)
    main()
