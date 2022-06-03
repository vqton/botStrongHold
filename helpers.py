import win32gui

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
