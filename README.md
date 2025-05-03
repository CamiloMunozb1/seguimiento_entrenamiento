# 🏋️‍♂️ Gestor de Rutinas y Peso

Este es un proyecto en Python para gestionar rutinas de entrenamiento y peso de usuarios. Permite a los usuarios registrarse, iniciar sesión de forma segura con contraseña encriptada y realizar operaciones CRUD sobre sus rutinas personales.

## 📦 Características

- Registro y login de usuarios con validación de correo y contraseña.
- Encriptación de contraseñas con `bcrypt`.
- Almacenamiento local con base de datos `SQLite`.
- Funciones para:
  - Insertar rutina y peso.
  - Actualizar rutina.
  - Actualizar peso.
  - Mostrar todas las rutinas y pesos registrados.
  - Cerrar sesión.

## 🚀 Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu_usuario/gestor-rutinas.git
   cd gestor-rutinas


2. Instala las dependencias necesarias:


     pip install bcrypt pandas


3. Crea la base de datos si no existe.

## Uso

1. Ejecuta el sistema
2. El usuario inicia sesión con correo y contraseña.
3. Si los datos son correctos, puede:
       - Registrar su rutina y peso.
       - Actualizar su rutina.
       - Actualizar su peso.
       - Ver toda la información guardada.
       - Cerrar sesión.

## Seguridad

- Las contraseñas son almacenadas usando hashing con bcrypt.
- Se valida la entrada del usuario antes de interactuar con la base de datos.

## Tecnologías

- Python 3.x.
- SQLite.
- bcrypt.
- pandas.
- Expresiones regulares (re).

## Licencia

Este proyecto esta bajo una licencia MIT.

## Autor

Desarrollado por Juan Camilo Muñoz.
