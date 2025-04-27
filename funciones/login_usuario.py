import sqlite3
import bcrypt
import re 

class IngresoDB:
    def __init__(self,ruta_db):
        try:
            self.conn = sqlite3.connect(ruta_db)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}.")
    
    def cierre_base(self):
        self.conn.close()
        print("Cierre de la base de datos exitoso.")

class LoginUsuario:
    def __init__(self,conexion):
        self.conexion = conexion

    def ingreso_usuario(self):
        try:
            self.email_usuario = str(input("Ingresa tu correo: ")).strip()
            self.password_usuario = str(input("Ingresa tu contraseña: ")).strip()

            validacion_email = r"[a-zA-Z-0-9]+@[a-zA-Z]+\.[a-z-.]+$"
            validacion_password = r"^[a-zA-Z0-9@#$%^&+=]{6,}$"
            intentos_contraseña = 3

            if not self.email_usuario or not self.password_usuario:
                print("Se tienen que ingresar todos los campos.")
                return
            elif not re.fullmatch(validacion_email, self.email_usuario):
                print("Correo no valido, vuelve a ingresar el que se registro.")
                return
            elif not re.fullmatch(validacion_password, self.password_usuario):
                print("Contraseña incorrecta o no cumple los parametos.")
                return
                
            self.conexion.cursor.execute("SELECT password_usuario FROM usuario_password WHERE email_usuario = ?",(self.email_usuario,))
            password = self.conexion.cursor.fetchone()
            if password:
                password_id = password[0]
                intentos_contraseña = 3
                while intentos_contraseña > 0:
                    if bcrypt.checkpw(self.password_usuario.encode("utf-8"), password_id):
                        print("Sesion iniciada...")
                        return
                    else:
                        intentos_contraseña -=1
                        print(f"Contraseña incorrecta. Te quedan {intentos_contraseña} intentos.")
                            
                        if intentos_contraseña > 0:
                            self.password_usuario = str(input("Vuelve a ingresar la contraseña: ")).strip()

                print("se agotaron los intentos. Acceso denegado.")
            else:
                print("Usuario no encontrado.")

        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}.")
        except Exception as error:
            print(f"Error en el programa: {error}.")



ruta_db = r"TU_RUTA_DB"
conexion = IngresoDB(ruta_db)
