import ctypes
import os
import win32com.client
import win32api
import win32con

def getIconPath(hz):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'icons', f'{hz}_hz.ico'))

HZ_CONFIGURATIONS = [60, 144]

def getMonitorFrequency():
    try:
        hdc = ctypes.windll.user32.GetDC(0)
        frequency = ctypes.windll.gdi32.GetDeviceCaps(hdc, 116)
        ctypes.windll.user32.ReleaseDC(0, hdc)
        return frequency
    except:
        return 60

def changeMonitorFrequency(frequency):
    try:
        device = win32api.EnumDisplayDevices(None, 0)
        settings = win32api.EnumDisplaySettings(device.DeviceName, win32con.ENUM_CURRENT_SETTINGS)
        settings.DisplayFrequency = frequency
        return win32api.ChangeDisplaySettings(settings, 0) == win32con.DISP_CHANGE_SUCCESSFUL
    except:
        return False

def changeShortcutIcon(frequency):
    try:
        icon = getErrorIconPath() if frequency is None else getIconPath(frequency)
        if not os.path.exists(icon):
            return False
            
        shortcutPath = os.path.join(os.path.expanduser("~"), "Desktop", "cambiar_hz.lnk")
        shortcut = win32com.client.Dispatch("WScript.Shell").CreateShortCut(shortcutPath)
        shortcut.IconLocation = f"{icon},0"
        shortcut.save()
        return True
    except:
        return False

def getErrorIconPath():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icons", "error.ico"))


def main():
    currentFrequency = getMonitorFrequency()
    
    if currentFrequency not in HZ_CONFIGURATIONS:
        print(f"¡Frecuencia inesperada detectada: {currentFrequency}Hz!")
        print(f"Las frecuencias soportadas son: {', '.join(str(hz) + 'Hz' for hz in HZ_CONFIGURATIONS)}")
        if changeShortcutIcon(None):  # None indicará usar icono de error
            print("Icono de error establecido exitosamente")
        return

    nextFrequency = HZ_CONFIGURATIONS[1] if currentFrequency == HZ_CONFIGURATIONS[0] else HZ_CONFIGURATIONS[0]
    
    if changeMonitorFrequency(nextFrequency):
        changeShortcutIcon(nextFrequency)

if __name__ == "__main__":
    main()