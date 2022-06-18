from extractText import extractText
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
    "salt",
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
    dctSettings["go"] = f"{int(pts[0])},{int(pts[1])}"
    wrtJSONSettings(SETTING_FILENAME, dctSettings)
    clickPOS(pts)

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

        dctSettings["scout"] = f"{int(pts[0])},{int(pts[1])}"
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
            AddUpdateValueDict(dctSettings, "close", ps1)
            wrtJSONSettings(SETTING_FILENAME, dctSettings)
            clickPOS(ps1)
            time.sleep(TIME_LOCATING)

        with open(r"temp\data.txt", "w") as f:
            f.write("250")

        letGo()
    except Exception as e:
        print(f"sendScout: {e}")
        pass


def clickWorldButton():
    try:
        posMapBtn = gui.locateOnScreen(
            r"images/collectRes/map.png", grayscale=True, confidence=0.3
        )
        time.sleep(TIME_LOCATING * 3)
        pts = gui.center(posMapBtn)
        print(f"Map world button: {pts}")
        AddUpdateValueDict(dctSettings, "map", pts)
        print(dctSettings)
        clickPOS(pts)
        # wrtJSONSettings(SETTING_FILENAME, dctSettings)
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
        if "home" not in dctSettings:
            pos = gui.locateOnScreen(
                r"images\\home.png", grayscale=True, confidence=0.6
            )
            time.sleep(3)
            print(dctSettings)
            pts = gui.center(pos)
            ptHome = pts
            print(f"Home {ptHome}")
            AddUpdateValueDict(dctSettings, "home", pts)
            wrtJSONSettings(SETTING_FILENAME, dctSettings)

        itemHome = dctSettings["home"]
        pts = (
            int(itemHome[: itemHome.index(",")]),
            int(itemHome[-itemHome.index(",") :]),
        )

        time.sleep(1)
        clickPOS(pts)

        # wrtJSonSetting('settings.json', json.dumps(dctSettings))
    except Exception as e:
        gui.alert(e, "clickHome Exception")
        print(f"Exception clickHome {e}")


def wrtEstTime():
    with open(r"temp\data.txt", "w") as f:
        f = open(r"temp\data.txt", "w")


def main():
    if isfile(SETTING_FILENAME):
        with open(SETTING_FILENAME, "r") as fp:
            dctSettings = json.load(fp)
            print(dctSettings)
    else:
        wrtJSONSettings(SETTING_FILENAME, {})

    wrtEstTime()
    activeWndStrongHold()
    clickWorldButton()
    clickHome()
    for item in lstRes:
        pts = getPosRes(item)
        if pts is not None:
            gui.screenshot(r"temp/scene.png")
            time.sleep(1)
            isExisting = detectObject(
                r"images/collectRes/" + item + "/1.png", r"temp/scene.png"
            )
            while isExisting:
                getResourceByPos(pts)
                sTime = extractText(r"temp/crop.jpg")
                sec = convertTime2Second(sTime)
                print(f"Second: {sec}")
                clickHome()
                gui.screenshot(r"temp/scene.png")
                time.sleep(1)
                isExisting = detectObject(
                    r"images/collectRes/" + item + "/1.png", r"temp/scene.png"
                )
                time.sleep(int(sec))
    # core()
    pass


if __name__ == "__main__":
    main()
