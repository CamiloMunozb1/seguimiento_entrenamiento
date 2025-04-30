import sqlite3
import bcrypt
import re


class IngresoDB:
    def __init__(self,rutadb):
        try:
            self.conn = sqlite3.connect(rutadb)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}.")

    def cierre_base(self):
        self.conn.close()
        print("Cierre de la base de datos exitoso.")


class IngresoUsuario:
    def __init__(self,conexion):
        self.conexion = conexion
    
    def registro_usuario(self):
        try:
            self.nombre_usuario = str(input("Ingresa tu nombre: ")).strip()
            self.apellido_usuario = str(input("Ingresa tu apellido: ")).strip()
            self.email_usuario = str(input("Ingresa tu correo: ")).strip()
            self.password_usuario = str(input("Crea tu contraseña(maximo 6 caracteres): ")).strip()

            validacion_email = r"[a-zA-Z-0-9]+@[a-zA-Z]+\.[a-z-.]+$"
            validacion_password = r"^[a-zA-Z0-9@#$%^&+=]{6,}$"
            encriptador_password = bcrypt.hashpw(self.password_usuario.encode("utf-8"),bcrypt.gensalt())

            if not all([self.nombre_usuario,self.apellido_usuario,self.email_usuario,self.password_usuario]):
                print("Los campos deben estar completos.")
                return
            elif not re.fullmatch(validacion_email, self.email_usuario):
                print("El email no es valido, vuelve a ingresar uno valido")
                return
            elif not re.fullmatch(validacion_password,self.password_usuario):
                print("Contraseña no valida, ingresa una valida.")
                return
            
            
            self.conexion.cursor.execute("SELECT 1 FROM usuario_password WHERE email_usuario = ?",(self.email_usuario,))
            if self.conexion.cursor.fetchone():
                print("Este correo ya se registro.")
                return
            
            self.conexion.cursor.execute("INSERT INTO usuario_datos(nombre_usuario,apellido_usuario) VALUES(?,?)",(self.nombre_usuario,self.apellido_usuario))
            self.conexion.conn.commit()

            usuario_id = self.conexion.cursor.lastrowid

            self.conexion.cursor.execute("INSERT INTO usuario_password(email_usuario,password_usuario, usuario_id) VALUES(?,?,?)",(self.email_usuario,encriptador_password,usuario_id))
            self.conexion.conn.commit()
            print("Datos registrados exitosamente.")


        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}.")
        except Exception as error:
            print(f"Error en el programa: {error}.")


ruta_db = r"TU_DATA_BASE"
conexion = IngresoDB(ruta_db)

