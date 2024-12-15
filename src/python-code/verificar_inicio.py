from cambiar_hz import obtener_frecuencia_monitor, cambiar_icono_acceso_directo, validar_frecuencia_soportada, obtener_hz_del_icono

def main():
    # Verificar y actualizar iconos de los accesos directos si existen
    hz_icono, coinciden = obtener_hz_del_icono()
    if not coinciden:
        print("Los iconos de los accesos directos no coinciden. Actualizando iconos...")
        cambiar_icono_acceso_directo(hz_icono)

    frecuencia_actual = obtener_frecuencia_monitor()

    if not validar_frecuencia_soportada(frecuencia_actual):
        print("Frecuencia no soportada")
        return
    
    if cambiar_icono_acceso_directo(frecuencia_actual):
        print("Iconos actualizados correctamente")
    else:
        print("Error al actualizar los iconos")

if __name__ == "__main__":
    main()