# Agenda Web.py y SQLite3

Ejemplo de una aplicacion web con SQLite3 y web.py

## Funcionalidades Implementadas

### ✅ Funcionalidades Principales
- **Listar personas**: Visualizar todas las personas en la agenda
- **Insertar persona**: Agregar nueva persona con nombre y email
- **Ver detalle**: Mostrar información detallada de una persona
- **Editar persona**: Modificar datos existentes de una persona
- **Navegación**: Botones de "Regresar" en todas las páginas

### ✅ Estructura de la Base de Datos
- Tabla `personas` con campos:
  - `id_persona` (clave primaria autoincremental)
  - `nombre` (varchar 50)
  - `email` (varchar 50)

### ✅ Rutas Implementadas
- `/` - Página principal con lista de personas
- `/insertar` - Formulario para agregar nueva persona
- `/detalle/<id>` - Ver detalles de una persona específica
- `/editar/<id>` - Formulario para editar una persona existente

## 0. Configuración Inicial de la Base de Datos

Antes de ejecutar la aplicación, es necesario crear la estructura de la base de datos:

```bash
cd agenda
sqlite3 agenda.db < ../sql/agenda.sql
```

Este comando creará la tabla `personas` y agregará datos de prueba.

## 1. Requisitos

Si se desea ejecutar la aplicacion en un entorno de desarrollo, se recomienda utilizar un entorno virtual. Para crear un entorno virtual, se puede utilizar el siguiente comando:

```bash
python3 -m venv .venv
```

Para activar el entorno virtual, se puede utilizar el siguiente comando:

```bash
source .venv/bin/activate
```

En el caso de Windows, el comando para activar el entorno virtual es:

```bash
.venv\Scripts\Activate.ps1
```

o

```bash
.venv\Scripts\activate.bat
```

Nota: es problable que se necesite ejecutar el siguiente comando para permitir la ejecucion de scripts en PowerShell:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
o

```bash
Set-ExecutionPolicy Unrestricted -Scope Process
```

Para instalar las dependencias necesarias, se puede utilizar el siguiente comando:

```bash
pip install -r requirements.txt
```


## 2. Configurar la aplicacion de web utilizar Servidores WSGI (Web Server Gateway Interface)

Para que la aplicacion web.py pueda ser ejecutada por un servidor **WSGI**, se debe modificar el archivo `main.py` para que defina una variable `application` que sea una funcion **WSGI**. A continuacion se muestra un ejemplo de como hacerlo:

```python
application = app.wsgifunc()
```


## 3. Configuración de Gunicorn

Si se trabaja en un entorno de producción, es recomendable utilizar un servidor WSGI como **gunicorn** o **waitress** para ejecutar la aplicacion web.py. Estos servidores son más eficientes y seguros que el servidor de desarrollo integrado de web.py.

### 3.1 Instalar Gunicorn

**gunicorn** es WSGI HTTP Server para **UNIX/Linux**.

Instalar gunicorn en tu entorno virtual o globalmente:

```bash
pip install gunicorn
```

### 3.2 Ejecutar la aplicacion con gunicorn

Para ejecutar la aplicacion con gunicorn, se utiliza el siguiente comando:

```bash
gunicorn -b 0.0.0.0:8080 main:application
```

Para ejecutar la aplicacion en el puerto 80, se requiere permisos de superusuario, este comando se debe ejecutar con `sudo`, en el caso de Codespaces, es necesario ejecutarlo de esta forma para que la aplicacion sea accesible desde el navegador y en las rutas no le agregue el puerto 8080, al redireccionar a la aplicacion:

```bash
sudo gunicorn -b 0.0.0.0:80 main:application
```

## 4. Configuración de Waitress

Waitress es un servidor WSGI para aplicaciones Python que funciona en Windows y UNIX. Es una alternativa a gunicorn.

### 4.1. Instalar waitress

**waitress** es un servidor WSGI para aplicaciones Python que funciona en Windows y UNIX

```bash
pip install waitress
```

### 4.2. Ejecutar la aplicacion con waitress

Para ejecutar la aplicacion con waitress, se utiliza el siguiente comando:

```bash
waitress-serve --port=8080 main:application
```

Si se desea ejecutar en el puerto 80, se debe ejecutar cambiando el puerto en el comando anterior:

```bash
sudo waitress-serve --port=80 main:application
```

## 5. Ejecutar la aplicacion con web.py

Para ejecutar la aplicacion con web.py, se utiliza el siguiente comando:

```bash
python3 main.py 8080
```
Si se desea ejecutar en el puerto 80, se debe ejecutar con permisos de superusuario:

```bash
sudo python3 main.py 80
```

## 6. Acceder a la aplicacion

Para acceder a la aplicacion, se debe abrir un navegador web y escribir la siguiente URL:

```
http://localhost:8080
```
O si se ejecuta en el puerto 80, simplemente:

```
http://localhost
```
## 7. Desactivar el entorno virtual
Para desactivar el entorno virtual, se puede utilizar el siguiente comando:

```bash
desactivate
```
## 8. Detener la aplicacion
Para detener la aplicacion, se puede utilizar el comando `Ctrl+C` en la terminal donde se esta ejecutando la aplicacion. Si se esta ejecutando con gunicorn o waitress, se debe detener el proceso correspondiente.