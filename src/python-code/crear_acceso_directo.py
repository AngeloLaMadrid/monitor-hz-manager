import sys
import os
import win32com.client
from cambiar_hz import getMonitorFrequency, HZ_CONFIGURATIONS

def createShortcut():
    try:
        pythonPath = sys.executable
        scriptPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "cambiar_hz.py"))
        desktopPath = os.path.join(os.path.expanduser("~"), "Desktop")
        
        currentFrequency = getMonitorFrequency()
        
        # Verificar si la frecuencia actual está en las configuraciones permitidas
        if currentFrequency not in HZ_CONFIGURATIONS:
            print(f"¡Frecuencia inesperada detectada: {currentFrequency}Hz!")
            print(f"Las frecuencias soportadas son: {', '.join(str(hz) + 'Hz' for hz in HZ_CONFIGURATIONS)}")
            iconPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icons", "error.ico"))
        else:
            iconPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icons", f"{currentFrequency}_hz.ico"))
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(os.path.join(desktopPath, "cambiar_hz.lnk"))
        shortcut.TargetPath = pythonPath
        shortcut.Arguments = f'"{scriptPath}"'
        shortcut.WorkingDirectory = os.path.dirname(scriptPath)
        shortcut.IconLocation = f"{iconPath},0"
        shortcut.save()
        
        if currentFrequency not in HZ_CONFIGURATIONS:
            print("Icono de error establecido exitosamente")
        else:
            print("Acceso directo creado exitosamente")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    createShortcut()