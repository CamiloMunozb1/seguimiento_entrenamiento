import sqlite3
import bcrypt
import re 

class IngresoDB:
    def __init__(self, ruta_db):
        try:
            self.conn = sqlite3.connect(ruta_db)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}.")
    
    def cierre_base(self):
        self.conn.close()
        print("Cierre de la base de datos exitoso.")

class LoginUsuario:
    def __init__(self, conexion):
        self.conexion = conexion
        self.password_id = None
        self.opciones_program()

    def ingreso_usuario(self):
        try:
            self.email_usuario = str(input("Ingresa tu correo: ")).strip()
            self.password_usuario = str(input("Ingresa tu contraseña: ")).strip()

            validacion_email = r"[a-zA-Z0-9]+@[a-zA-Z]+\.[a-z-.]+$"
            validacion_password = r"^[a-zA-Z0-9@#$%^&+=]{6,}$"
            intentos_contraseña = 3

            if not self.email_usuario or not self.password_usuario:
                print("Se tienen que ingresar todos los campos.")
                return None  # Retornamos None si no hay datos.
            elif not re.fullmatch(validacion_email, self.email_usuario):
                print("Correo no válido, vuelve a ingresar el que se registró.")
                return None
            elif not re.fullmatch(validacion_password, self.password_usuario):
                print("Contraseña incorrecta o no cumple los parámetros.")
                return None
                
            self.conexion.cursor.execute("SELECT password_usuario FROM usuario_password WHERE email_usuario = ?", (self.email_usuario,))
            password = self.conexion.cursor.fetchone()
            if password:
                password_id = password[0]
                intentos_contraseña = 3
                while intentos_contraseña > 0:
                    if bcrypt.checkpw(self.password_usuario.encode("utf-8"), password_id):  # Aseguramos que password_id es una cadena
                        print("Sesión iniciada...")
                        self.password_id = password_id
                        return password_id  # Devolvemos el password_id
                    else:
                        intentos_contraseña -= 1
                        print(f"Contraseña incorrecta. Te quedan {intentos_contraseña} intentos.")
                        if intentos_contraseña > 0:
                            self.password_usuario = str(input("Vuelve a ingresar la contraseña: ")).strip()

                print("Se agotaron los intentos. Acceso denegado.")
                return None
            else:
                print("Usuario no encontrado.")
                return None

        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}.")
        except Exception as error:
            print(f"Error en el programa: {error}.")
        return None
    

    def opciones_program(self):
        self.opciones = {
            "1": self.opcion_uno,
            "2": self.opcion_dos,
            "3": self.opcion_tres
        }


    def mostrar_opciones(self):
        print("""
                Qué opción deseas?
                1. Ingresa tu rutina y peso.
                2. Actualiza tu rutina.
                3. Actualiza tu peso.
            """)
    

    def ejecutar_opciones(self):
        try:
            while True:
                self.mostrar_opciones()
                usuario = str(input("Ingresa la opción que deseas: "))
                if not usuario:
                    print("Necesitas ingresar una opción.")
                    return
                accion = self.opciones.get(usuario)
                if accion:
                    accion()
                    break
                else:
                    print("Ingresa un valor correcto entre 1 a 3.")
        except ValueError:
            print("Error de digitación, ingresar nuevamente.")

    def ingreso_info(self, password_id):
        try:
            self.nombre_rutina = str(input("Ingresa tu rutina: ")).strip()
            self.usuario_peso = str(input("Ingresa tu peso: ")).strip()

            if not self.nombre_rutina or not self.usuario_peso:
                print("Los campos deben estar completos.")
                return
            
            self.conexion.cursor.execute(
                "INSERT INTO usuario_entrenamiento(nombre_rutina,usuario_peso,password_id) VALUES (?,?,?)",
                (self.nombre_rutina, self.usuario_peso, password_id)
            )
            self.conexion.conn.commit()
            print("Rutina y peso subidos exitosamente.")
        
        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}.")
        except Exception as error:
            print(f"Error en el programa: {error}.")

    def opcion_uno(self):
        if self.password_id:# Llamamos a ingreso_usuario para obtener el password_id
            self.ingreso_info(self.password_id)  # Pasamos password_id a ingreso_info

    def opcion_dos(self):
        print("Opción 2 no implementada aún.")

    def opcion_tres(self):
        print("Opción 3 no implementada aún.")




ruta_db = r"TU_BASE_DATOS"
conexion = IngresoDB(ruta_db)
