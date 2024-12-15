import sys
import os
import win32com.client
from cambiar_hz import obtener_frecuencia_monitor

def obtener_ubicacion_python():
    try:
        return sys.executable
    except Exception as e:
        print(f"Error al obtener la ubicación de python.exe: {e}")
        return None

def obtener_icono_hz():
    try:
        frecuencia_actual = obtener_frecuencia_monitor()
        icono_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icons", f"{frecuencia_actual}_hz.ico"))
        if os.path.exists(icono_path):
            return icono_path
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icons", "error.ico"))
    except:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icons", "error.ico"))

def crear_acceso_directo():
    try:
        python_path = obtener_ubicacion_python()
        if not python_path:
            raise ValueError("No se pudo obtener la ubicación de Python")

        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "cambiar_hz.py"))
        if not os.path.exists(script_path):
            raise FileNotFoundError("No se encuentra el archivo cambiar_hz.py")

        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        shell = win32com.client.Dispatch("WScript.Shell")
        
        icono_path = obtener_icono_hz()
        
        # Crear acceso directo local
        shortcut_local = shell.CreateShortCut("verificar_hz.lnk")
        shortcut_local.TargetPath = python_path
        shortcut_local.Arguments = f'"{script_path}"'
        shortcut_local.WorkingDirectory = os.path.dirname(script_path)
        shortcut_local.IconLocation = f"{icono_path},0"
        shortcut_local.save()
        
        # Crear acceso directo en el escritorio
        shortcut_desktop = shell.CreateShortCut(os.path.join(desktop_path, "verificar_hz.lnk"))
        shortcut_desktop.TargetPath = python_path
        shortcut_desktop.Arguments = f'"{script_path}"'
        shortcut_desktop.WorkingDirectory = os.path.dirname(script_path)
        shortcut_desktop.IconLocation = f"{icono_path},0"
        shortcut_desktop.save()
        
        print("Accesos directos creados exitosamente")
        
    except Exception as e:
        print(f"Error al crear acceso directo: {e}")

if __name__ == "__main__":
    crear_acceso_directo()