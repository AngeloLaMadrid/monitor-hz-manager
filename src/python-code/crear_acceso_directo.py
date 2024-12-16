import sys
import os
import win32com.client
from cambiar_hz import obtener_frecuencia_monitor, CONFIGURACIONES_HZ

def crear_acceso_directo():
    try:
        python_path = sys.executable
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "cambiar_hz.py"))
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        
        frecuencia_actual = obtener_frecuencia_monitor()
        icono_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icons", f"{frecuencia_actual}_hz.ico"))
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(os.path.join(desktop_path, "verificar_hz.lnk"))
        shortcut.TargetPath = python_path
        shortcut.Arguments = f'"{script_path}"'
        shortcut.WorkingDirectory = os.path.dirname(script_path)
        shortcut.IconLocation = f"{icono_path},0"
        shortcut.save()
        
        print("Acceso directo creado exitosamente")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    crear_acceso_directo()