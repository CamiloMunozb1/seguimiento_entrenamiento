from funciones.ingreso_user import IngresoDB, IngresoUsuario
from funciones.login_usuario import IngresoDB, LoginUsuario


ruta_db = r"TU_BASE_DATOS"
conexion = IngresoDB(ruta_db)


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
            registro = IngresoUsuario(conexion)
            registro.registro_usuario()
        elif usuario == "2":
            login = LoginUsuario(conexion)
            password_id = login.ingreso_usuario()
            if password_id:
                login.ejecutar_opciones()
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