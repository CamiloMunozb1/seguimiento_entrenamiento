
while True:
    print("""
            Bienvenido a tu seguimineto de entrenamiento.
            1. Crea una cuenta.
            2. Inicia sesion.
            3. Salir
        """)
    try:
        usuario = str(input("Ingresa una opcion: "))
        if not usuario:
            print("Debes indicar una opcion.")
            break
        elif usuario == "1":
            print("Proxima opcion.")
        elif usuario == "2":
            print("Proxima opcion.")
        elif usuario == "3":
            print("Gracias por ingresar al seguimiento de entrenamiento.")
            break
        else:
            print("Debes indicar una opcion de 1-3.")

        input("\nPresiona enter para continuar...")
    
    except ValueError:
        print("Error en la digitacion de las opciones, ingresa una valida.")
    except Exception as error:
        print(f"Error en el programa: {error}.")