# Importamos las clases necesarias desde los módulos de funciones.
# IngresoDB se encarga de conectarse a la base de datos.
# IngresoUsuario y LoginUsuario contienen la lógica para crear usuarios e iniciar sesión.
from funciones.ingreso_user import IngresoDB, IngresoUsuario
from funciones.login_usuario import IngresoDB, LoginUsuario

# Ruta a la base de datos SQLite (puede ser modificada según el entorno).
ruta_db = r"TU_BASE_DATOS"
# Se crea una conexión a la base de datos usando la clase IngresoDB.
conexion = IngresoDB(ruta_db)

# Bucle principal del programa (menú de inicio).
while True:
    print("""
            Bienvenido a tu seguimiento de entrenamiento.
            1. Crea una cuenta.
            2. Inicia sesión.
            3. Salir
        """)
    try:
        # Se pide al usuario que ingrese una opción del menú.
        usuario = str(input("Ingresa una opción: "))

        # Si no ingresa nada, se le avisa y el programa termina.
        if not usuario:
            print("Debes indicar una opción.")
            break
        
        # Opción 1: Crear una nueva cuenta de usuario.
        elif usuario == "1":
            registro = IngresoUsuario(conexion)
            registro.registro_usuario()

        # Opción 2: Iniciar sesión con un usuario existente.
        elif usuario == "2":
            login = LoginUsuario(conexion)
            password_id = login.ingreso_usuario()

            # Si el inicio de sesión es exitoso, se muestran más opciones (submenú).
            if password_id:
                login.ejecutar_opciones()

        # Opción 3: Salir del programa.
        elif usuario == "3":
            print("Gracias por ingresar al seguimiento de entrenamiento.")
            break

        # Si se ingresa algo diferente a 1, 2 o 3, se muestra un mensaje de error.
        else:
            print("Debes indicar una opción de 1-3.")

        # Se detiene el flujo hasta que el usuario presione enter.
        input("\nPresiona enter para continuar...")

    # Si el usuario ingresa un valor inválido (no se espera en este punto), se maneja.
    except ValueError:
        print("Error en la digitación de las opciones, ingresa una válida.")

    # Captura de errores generales para evitar que el programa se caiga.
    except Exception as error:
        print(f"Error en el programa: {error}.")
