import win32gui
import pyautogui as gui
import time
from os import listdir
from os.path import isfile, join
results = []
top_windows = []


def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def convertTime2Secound(sTime):
    a = ""
    for x in sTime:
        if x.isdigit():
            a = a+x
    sec = int(a[:2]) * 60 + int(a[-2:])
    return sec

def BringWindow2Front(sName):
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if sName.lower() in i[1].lower():
            print(i)
            win32gui.ShowWindow(i[0], 5)
            win32gui.SetForegroundWindow(i[0])
            break


def clickPOS(pts):
    gui.moveTo(pts[0], pts[1])
    time.sleep(0.5)
    gui.mouseDown(pts[0], pts[1])
    time.sleep(0.5)
    gui.mouseUp(pts[0], pts[1])
    time.sleep(3)

def getListFiles(sPath):
    onlyfiles = [f for f in listdir(sPath) if isfile(join(sPath, f))]
    return onlyfiles