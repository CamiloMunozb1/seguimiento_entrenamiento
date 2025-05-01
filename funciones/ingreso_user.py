# Importamos los módulos necesarios
import sqlite3  # Para manejar la base de datos SQLite
import bcrypt   # Para encriptar contraseñas de forma segura
import re       # Para validar el formato del correo y la contraseña usando expresiones regulares


class IngresoDB:
    def __init__(self,rutadb):
        try:
            # Se intenta conectar a la base de datos SQLite con la ruta especificada.
            self.conn = sqlite3.connect(rutadb)
            self.cursor = self.conn.cursor() # Se obtiene el cursor para ejecutar queries SQL.
        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}.")  # Si falla la conexión, se muestra el error.

    def cierre_base(self):
        # Método para cerrar la conexión con la base de datos.
        self.conn.close()
        print("Cierre de la base de datos exitoso.")


class IngresoUsuario:
    def __init__(self,conexion):
        # Recibe un objeto de tipo IngresoDB ya conectado.
        self.conexion = conexion
    
    def registro_usuario(self):
        try:
            # Se solicitan los datos del usuario.
            self.nombre_usuario = str(input("Ingresa tu nombre: ")).strip()
            self.apellido_usuario = str(input("Ingresa tu apellido: ")).strip()
            self.email_usuario = str(input("Ingresa tu correo: ")).strip()
            self.password_usuario = str(input("Crea tu contraseña(maximo 6 caracteres): ")).strip()

            # Expresiones regulares para validar formato de email y contraseña.
            validacion_email = r"[a-zA-Z-0-9]+@[a-zA-Z]+\.[a-z-.]+$"
            validacion_password = r"^[a-zA-Z0-9@#$%^&+=]{6,}$"
            # Encriptamos la contraseña usando bcrypt.
            encriptador_password = bcrypt.hashpw(self.password_usuario.encode("utf-8"),bcrypt.gensalt())

            # Validación: campos vacíos.
            if not all([self.nombre_usuario,self.apellido_usuario,self.email_usuario,self.password_usuario]):
                print("Los campos deben estar completos.")
                return
            # Validación: formato de la contraseña.
            elif not re.fullmatch(validacion_email, self.email_usuario):
                print("El email no es valido, vuelve a ingresar uno valido")
                return
            # Validación: formato de la contraseña.
            elif not re.fullmatch(validacion_password,self.password_usuario):
                print("Contraseña no valida, ingresa una valida.")
                return
            
            # Verificar si el correo ya existe en la base de datos.
            self.conexion.cursor.execute("SELECT 1 FROM usuario_password WHERE email_usuario = ?",(self.email_usuario,))
            if self.conexion.cursor.fetchone():
                print("Este correo ya se registro.")
                return
            
            # Insertar nombre y apellido en la tabla usuario_datos.
            self.conexion.cursor.execute("INSERT INTO usuario_datos(nombre_usuario,apellido_usuario) VALUES(?,?)",(self.nombre_usuario,self.apellido_usuario))
            self.conexion.conn.commit()

            # Obtener el ID del nuevo usuario
            usuario_id = self.conexion.cursor.lastrowid

            # Insertar email y contraseña en la tabla usuario_password, vinculados al usuario_id.
            self.conexion.cursor.execute("INSERT INTO usuario_password(email_usuario,password_usuario, usuario_id) VALUES(?,?,?)",(self.email_usuario,encriptador_password,usuario_id))
            self.conexion.conn.commit()
            print("Datos registrados exitosamente.")


        # Captura de errores de base de datos y errores generales.
        except sqlite3.Error as error:
            print(f"Error en la base de datos: {error}.")
        except Exception as error:
            print(f"Error en el programa: {error}.")



