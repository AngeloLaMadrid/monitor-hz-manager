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
        iconPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icons", f"{currentFrequency}_hz.ico"))
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(os.path.join(desktopPath, "cambiar_hz.lnk"))
        shortcut.TargetPath = pythonPath
        shortcut.Arguments = f'"{scriptPath}"'
        shortcut.WorkingDirectory = os.path.dirname(scriptPath)
        shortcut.IconLocation = f"{iconPath},0"
        shortcut.save()
        
        print("Acceso directo creado exitosamente")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    createShortcut()