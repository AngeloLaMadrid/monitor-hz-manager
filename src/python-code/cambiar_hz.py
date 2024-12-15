import ctypes
import os
import win32com.client
import win32api
import win32con 
import re
import tkinter as tk
from tkinter import ttk

ACCESOS_DIRECTOS = {
    "local": "verificar_hz.lnk",
    "escritorio": os.path.join(os.path.expanduser("~\\Desktop"), "verificar_hz.lnk")
}

CONFIGURACIONES_HZ = {
    60: os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'icons', '60_hz.ico')),
    144: os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'icons', '144_hz.ico'))
}

def obtener_hz_del_icono() -> tuple[int, bool]:
    try:
        resultados = {}
        for ubicacion, path in ACCESOS_DIRECTOS.items():
            if not os.path.exists(path):
                print(f"El acceso directo en {ubicacion} no existe.")
                continue

            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(path)
            icon_path = shortcut.IconLocation.split(',')[0]
            
            if not os.path.exists(icon_path):
                print(f"El archivo de icono no existe: {icon_path}")
                continue

            icon_filename = os.path.basename(icon_path)
            match = re.search(r'(\d+)_hz\.ico', icon_filename.lower())
            
            if match:
                resultados[ubicacion] = int(match.group(1))
            else:
                print(f"No se encontró coincidencia en el icono de {ubicacion}")
                return None, False

        if len(resultados) == 2 and len(set(resultados.values())) == 1:
            return list(resultados.values())[0], True
        else:
            print("Los accesos directos tienen diferentes frecuencias o faltan accesos directos")
            return None, False

    except Exception as e:
        print(f"Error al leer Hz de los iconos: {e}")
        return None, False

def cambiar_icono_acceso_directo(frecuencia: int) -> bool:
    try:
        icono = CONFIGURACIONES_HZ.get(frecuencia)
        if not icono or not os.path.exists(icono):
            print(f"No hay icono definido para {frecuencia}Hz o no existe el archivo.")
            return False

        exito = True
        for ubicacion, path in ACCESOS_DIRECTOS.items():
            try:
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(path)
                shortcut.IconLocation = f"{os.path.abspath(icono)},0"
                shortcut.save()
                print(f"Icono actualizado en {ubicacion}")
            except Exception as e:
                print(f"Error al actualizar icono en {ubicacion}: {e}")
                exito = False

        return exito

    except Exception as e:
        print(f"Error al cambiar los iconos: {e}")
        return False

def obtener_siguiente_frecuencia(frecuencia_actual: int) -> int:
    frecuencias = sorted(CONFIGURACIONES_HZ.keys())
    try:
        indice_actual = frecuencias.index(frecuencia_actual)
        siguiente = frecuencias[(indice_actual + 1) % len(frecuencias)]
        print(f"Siguiente frecuencia: {siguiente}Hz")
        return siguiente
    except ValueError:
        print(f"Frecuencia actual {frecuencia_actual}Hz no encontrada. Usando la primera frecuencia disponible: {frecuencias[0]}Hz")
        return frecuencias[0]

def cambiar_frecuencia_monitor(frecuencia: int) -> bool:
    try:
        device = win32api.EnumDisplayDevices(None, 0)
        settings = win32api.EnumDisplaySettings(device.DeviceName, win32con.ENUM_CURRENT_SETTINGS)
        settings.DisplayFrequency = frecuencia
        result = win32api.ChangeDisplaySettings(settings, 0)
        if result == win32con.DISP_CHANGE_SUCCESSFUL:
            print(f"Frecuencia cambiada a {frecuencia}Hz exitosamente.")
            return True
        else:
            print(f"Fallo al cambiar la frecuencia a {frecuencia}Hz. Resultado: {result}")
            return False
    except Exception as e:
        print(f"Error al cambiar la frecuencia: {e}")
        return False

def obtener_frecuencia_monitor() -> int:
    try:
        hdc = ctypes.windll.user32.GetDC(0)
        frecuencia = ctypes.windll.gdi32.GetDeviceCaps(hdc, 116)
        ctypes.windll.user32.ReleaseDC(0, hdc)
        print(f"Frecuencia actual del monitor: {frecuencia}Hz")
        return frecuencia
    except Exception as e:
        print(f"Error al obtener frecuencia: {e}")
        return 60

def mostrar_ventana_advertencia(frecuencia: int, frecuencias_soportadas: list) -> None:
    ventana = tk.Tk()
    ventana.title("Advertencia")
    ancho = 400
    alto = 200
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    mensaje = f"""
    ¡ADVERTENCIA!
    
    Frecuencia {frecuencia}Hz no soportada
    Frecuencias soportadas: {sorted(frecuencias_soportadas)}Hz
    
    Esta ventana se cerrará en 3 segundos...
    """
    
    label = ttk.Label(ventana, text=mensaje, justify="center", foreground="red")
    label.pack(expand=True)
    
    ventana.after(4000, ventana.destroy)
    ventana.mainloop()

def validar_frecuencia_soportada(frecuencia: int) -> bool:
    try:
        if frecuencia not in CONFIGURACIONES_HZ:
            mostrar_ventana_advertencia(frecuencia, CONFIGURACIONES_HZ.keys())
            return False
        return True
    except Exception as e:
        print(f"Error al validar frecuencia: {e}")
        return False

def main():
    frecuencia_actual = obtener_frecuencia_monitor()
    
    if not validar_frecuencia_soportada(frecuencia_actual):
        print(f"Ejecute el programa cuando la frecuencia esté en un valor soportado.")
        return
        
    hz_icono, coinciden = obtener_hz_del_icono()

    if not coinciden or hz_icono != frecuencia_actual:
        print(f"\nLa frecuencia del monitor ({frecuencia_actual}Hz) no coincide con los iconos")
        print("Actualizando iconos...")
        if cambiar_icono_acceso_directo(frecuencia_actual):
            print("Iconos actualizados correctamente.")
        return
    
    siguiente_frecuencia = obtener_siguiente_frecuencia(frecuencia_actual)
    print(f"\nCambiando la frecuencia a {siguiente_frecuencia}Hz...")
    
    if cambiar_frecuencia_monitor(siguiente_frecuencia):
        if cambiar_icono_acceso_directo(siguiente_frecuencia):
            print("Iconos actualizados correctamente.")
        else:
            print("Error al actualizar los iconos.")
    else:
        print("Error al cambiar la frecuencia del monitor.")
    
    print(f"Frecuencia cambiada a {siguiente_frecuencia}Hz")

if __name__ == "__main__":
    main()