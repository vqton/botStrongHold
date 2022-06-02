
import win32gui
import psutil
results = []
top_windows = []


def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def existingApp(sName):
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if sName in i[1].lower():
            return True
    return False


def checkIfProcessRunning(processName):
        '''Check if there are any running process that contains the given name processName.
        Iterate over the all the running process'''
        print('Checking if application is running...')
        for proc in psutil.process_iter():
                try:
                        # Check if process name contains the given name string.
                        if processName.lower() in proc.name().lower():
                                return True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
        return False;