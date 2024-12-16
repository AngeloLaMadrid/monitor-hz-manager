from cambiar_hz import obtener_frecuencia_monitor, cambiar_icono_acceso_directo, CONFIGURACIONES_HZ

def main():
    frecuencia_actual = obtener_frecuencia_monitor()
    
    if frecuencia_actual not in CONFIGURACIONES_HZ:
        print("Frecuencia no soportada")
        return
    
    if cambiar_icono_acceso_directo(frecuencia_actual):
        print("Iconos actualizados correctamente")
    else:
        print("Error al actualizar los iconos")

if __name__ == "__main__":
    main()  