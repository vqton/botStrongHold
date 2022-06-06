import win32gui
import pyautogui as gui
import time
from os import listdir
from os.path import isfile, join
results = []
top_windows = []


def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def BringWindow2Front(sName):
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if sName.lower() in i[1].lower():
            print(i)
            win32gui.ShowWindow(i[0], 5)
            win32gui.SetForegroundWindow(i[0])
            break


def clickPOS(pts):
    gui.moveTo(pts.x, pts.y)
    time.sleep(0.5)
    gui.mouseDown(pts.x, pts.y)
    time.sleep(0.5)
    gui.mouseUp(pts.x, pts.y)
    time.sleep(3)

def getListFiles(sPath):
    onlyfiles = [f for f in listdir(sPath) if isfile(join(sPath, f))]
    return onlyfiles