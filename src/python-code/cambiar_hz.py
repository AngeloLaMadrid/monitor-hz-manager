import ctypes
import os
import win32com.client
import win32api
import win32con

def get_icon_path(hz):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'icons', f'{hz}_hz.ico'))

CONFIGURACIONES_HZ = [60, 144]

def obtener_frecuencia_monitor():
    try:
        hdc = ctypes.windll.user32.GetDC(0)
        frecuencia = ctypes.windll.gdi32.GetDeviceCaps(hdc, 116)
        ctypes.windll.user32.ReleaseDC(0, hdc)
        return frecuencia
    except:
        return 60

def cambiar_frecuencia_monitor(frecuencia):
    try:
        device = win32api.EnumDisplayDevices(None, 0)
        settings = win32api.EnumDisplaySettings(device.DeviceName, win32con.ENUM_CURRENT_SETTINGS)
        settings.DisplayFrequency = frecuencia
        return win32api.ChangeDisplaySettings(settings, 0) == win32con.DISP_CHANGE_SUCCESSFUL
    except:
        return False

def cambiar_icono_acceso_directo(frecuencia):
    try:
        icono = get_icon_path(frecuencia)
        if not os.path.exists(icono):
            return False
            
        shortcut_path = os.path.join(os.path.expanduser("~"), "Desktop", "verificar_hz.lnk")
        shortcut = win32com.client.Dispatch("WScript.Shell").CreateShortCut(shortcut_path)
        shortcut.IconLocation = f"{icono},0"
        shortcut.save()
        return True
    except:
        return False

def main():
    frecuencia_actual = obtener_frecuencia_monitor()
    if frecuencia_actual not in CONFIGURACIONES_HZ:
        return
        
    siguiente = CONFIGURACIONES_HZ[1] if frecuencia_actual == CONFIGURACIONES_HZ[0] else CONFIGURACIONES_HZ[0]
    
    if cambiar_frecuencia_monitor(siguiente):
        cambiar_icono_acceso_directo(siguiente)

if __name__ == "__main__":
    main()