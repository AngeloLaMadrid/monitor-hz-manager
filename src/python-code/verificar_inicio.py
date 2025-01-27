from cambiar_hz import getMonitorFrequency, changeShortcutIcon, changeMonitorFrequency, HZ_CONFIGURATIONS
import os

def main():
    currentFrequency = getMonitorFrequency()
    
    if currentFrequency not in HZ_CONFIGURATIONS:
        print(f"Frecuencia actual ({currentFrequency}Hz) no está soportada.")
        print(f"Las frecuencias soportadas son: {', '.join(str(hz) + 'Hz' for hz in HZ_CONFIGURATIONS)}")
        
        # Cambiar al icono de error
        error_icon = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'icons', 'error.ico'))
        if os.path.exists(error_icon):
            if changeShortcutIcon('error'):
                print("Icono de error establecido")
            else:
                print("Error al establecer icono de error")
        return
    
    if changeShortcutIcon(currentFrequency):
        print("Iconos actualizados correctamente")
    else:
        print("Error al actualizar los iconos")

if __name__ == "__main__":
    main()