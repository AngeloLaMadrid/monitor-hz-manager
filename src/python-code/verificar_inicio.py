from cambiar_hz import getMonitorFrequency, changeShortcutIcon, HZ_CONFIGURATIONS

def main():
    currentFrequency = getMonitorFrequency()
    
    if currentFrequency not in HZ_CONFIGURATIONS:
        print("Frecuencia no soportada")
        return
    
    if changeShortcutIcon(currentFrequency):
        print("Iconos actualizados correctamente")
    else:
        print("Error al actualizar los iconos")

if __name__ == "__main__":
    main()