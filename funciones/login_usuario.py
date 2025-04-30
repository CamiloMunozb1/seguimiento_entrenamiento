import sqlite3
import bcrypt
import pandas as pd
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
            "3": self.opcion_tres,
            "4": self.opcion_cuatro,
            "5": self.opcion_cinco
        }


    def mostrar_opciones(self):
        print("""
                Qué opción deseas?
                1. Ingresa tu rutina y peso.
                2. Actualiza tu rutina.
                3. Actualiza tu peso.
                4. Mostrar rutinas.
                5. Cerrar sesion.
            """)
    

    def ejecutar_opciones(self):
        try:
            while True:
                self.mostrar_opciones()
                usuario = str(input("Ingresa la opción que deseas: "))
                if not usuario:
                    print("Necesitas ingresar una opción.")
                    continue
                accion = self.opciones.get(usuario)
                if accion:
                    accion()
                    if usuario == "5":
                        break
                else:
                    print("Ingresa un valor correcto entre 1 a 3.")
        except ValueError:
            print("Error de digitación, ingresar nuevamente.")

    def ingreso_info(self, password_id):
        try:
            self.nombre_rutina = str(input("Ingresa tu rutina: ")).strip()
            self.usuario_peso = float(input("Ingresa tu peso: "))

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
    
    def actualizar_rutina(self, password_id):
        try:
            self.nombre_rutina = str(input("Ingresa tu nueva rutina: ")).strip()
            if not self.nombre_rutina:
                print("El campo no puede estar vacio.")
                return
            
            self.conexion.cursor.execute(
                "UPDATE usuario_entrenamiento set nombre_rutina = ? WHERE password_id = ?",
                (self.nombre_rutina, password_id)
            )
            self.conexion.conn.commit()
            print("Rutina actualizada con exito.")
        
        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}.")
        except Exception as error:
            print(f"Error en el programa: {error}.")
    
    def actualizar_peso(self, password_id):
        try:
            self.usuario_peso = float(input("Ingresa tu peso: "))
            if not self.usuario_peso:
                print("El campo no puede estar vacio.")
                return
            
            self.conexion.cursor.execute(
                "UPDATE usuario_entrenamiento SET usuario_peso = ? WHERE password_id = ?",
                (self.usuario_peso, password_id)
            )
            self.conexion.conn.commit()
            print("Peso actualizada con exito.")
        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}.")
        except Exception as error:
            print(f"Error en el programa: {error}.")
    
    def mostrar_rutinas(self, password_id):
        try:
            query = """
                    SELECT
                        nombre_rutina,
                        usuario_peso
                    FROM usuario_entrenamiento
                    WHERE password_id = ?
                """
            resultado_df = pd.read_sql_query(query, self.conexion.conn, params=(password_id,))
            if not resultado_df.empty:
                print(resultado_df)
            else:
                print("No se encontraron rutinas o pesos del usuario.")

        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}.")

    def opcion_uno(self):
        if not self.password_id:# Llamamos a ingreso_usuario para obtener el password_id
            password_id = self.ingreso_usuario()# Pasamos password_id a ingreso_info
            if not password_id:
                return
        else:
            password_id = self.password_id
        self.ingreso_info(password_id)

    def opcion_dos(self):
        if not self.password_id:
            password_id = self.ingreso_usuario()
            if not password_id:
                return
        else:
            password_id = self.password_id
        self.actualizar_rutina(password_id)

    def opcion_tres(self):
        if not self.password_id:
            password_id = self.ingreso_usuario()
            if not password_id:
                return
        else:
            password_id = self.password_id
        self.actualizar_peso(password_id)
    
    def opcion_cuatro(self):
        if not self.password_id:
            password_id = self.ingreso_usuario()
            if not password_id:
                return
        else:
                password_id = self.password_id
        self.mostrar_rutinas(password_id)

    def opcion_cinco(self):
        self.password_id = None
        print("Cerrando sesion.")


ruta_db = r"TU_DATA_BASE"
conexion = IngresoDB(ruta_db)
