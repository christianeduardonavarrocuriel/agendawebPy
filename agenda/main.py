import web
import sqlite3

urls = (
    "/", "Index",
    "/insertar","Insertar",
    "/detalle/(.*)", "Detalle",
    "/editar/(.*)", "Editar",
    "/borrar/(.*)", "Borrar"
    )

render = web.template.render("templates/")

app = web.application(urls, globals())

class Index:
    def GET(self):
        try:
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            personas = cursor.execute("select * from personas;")
            respuesta = {
                "personas" : personas.fetchall(),
                "error": None
            }
            conection.close()
            return render.index(respuesta)
        except sqlite3.OperationalError as error:
            print(f"Error 000: {error.args[0]}")
            respuesta = {
                "personas" : [],
                "error": "Error al conectar con la base de datos"
            }
            print(f"RESPUESTA: {respuesta}")
            return render.index(respuesta)
        except Exception as error:
            print(f"Error conexión: {error.args[0]}")
            respuesta = {
                "personas" : [],
                "error": "Error al conectar con la base de datos"
            }
            return render.index(respuesta)

class Insertar:
    def GET(self):
        try:
            return render.insertar()
        except Exception as error:
            print(f"Error 001: {error.args[0]}")
            return render.insertar()

    def POST(self):
        try:
            form = web.input()
            print(f"Form data: {form}")
            
            # Validación: verificar que los campos no estén vacíos
            if not form.nombre.strip() or not form.email.strip():
                print("Error: Campos vacíos detectados")
                return render.insertar("Por favor, llena todos los campos")
            
            # Validación: verificar formato de email (nombre@email.com)
            email = form.email.strip()
            if not email.endswith("@email.com") or email == "@email.com":
                print("Error: Formato de email incorrecto")
                return render.insertar("Email incorrecto. Debe terminar en @email.com")
            
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            sql = "INSERT INTO personas(nombre, email) VALUES (?, ?);"
            data = (form.nombre.strip(), email)
            cursor.execute(sql, data)
            print("Executed SQL query successfully.")
            conection.commit()
            conection.close()
            return web.seeother("/")
        except sqlite3.OperationalError as error:
            print(f"Error 002: {error.args[0]}")
            return render.insertar("Error al conectar con la base de datos")
        except Exception as error:
            print(f"Error 003: {error.args[0]}")
            return render.insertar("Error al conectar con la base de datos")


class Detalle:

    def GET(self,id_persona):
        try:
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            sql = "select * from personas where id_persona = ?;"
            datos = (id_persona,)
            personas = cursor.execute(sql,datos)
            
            respuesta={
                "persona" : personas.fetchone(),
                "error": None
            }
            print(f"RESPUESTA: {respuesta}")
            conection.close()
            return render.detalle(respuesta)
        except sqlite3.OperationalError as error:
            print(f"Error 004: {error.args[0]}")
            respuesta={
                "persona" : None,
                "error": "Error al conectar con la base de datos"
            }
            return render.detalle(respuesta)
        except Exception as error:
            print(f"Error conexión detalle: {error.args[0]}")
            respuesta={
                "persona" : None,
                "error": "Error al conectar con la base de datos"
            }
            return render.detalle(respuesta)


class Editar:
    def GET(self, id_persona):
        try:
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            sql = "select * from personas where id_persona = ?;"
            datos = (id_persona,)
            personas = cursor.execute(sql, datos)
            
            respuesta = {
                "persona": personas.fetchone(),
                "error": None
            }
            conection.close()
            return render.editar(respuesta)
        except sqlite3.OperationalError as error:
            print(f"Error 005: {error.args[0]}")
            respuesta = {
                "persona": None,
                "error": "Error al conectar con la base de datos"
            }
            return render.editar(respuesta)
        except Exception as error:
            print(f"Error conexión editar: {error.args[0]}")
            respuesta = {
                "persona": None,
                "error": "Error al conectar con la base de datos"
            }
            return render.editar(respuesta)
    
    def POST(self, id_persona):
        try:
            form = web.input()
            
            # Validación: verificar que los campos no estén vacíos
            if not form.nombre.strip() or not form.email.strip():
                print("Error: Campos vacíos detectados en edición")
                # Recargar la página de edición si hay campos vacíos
                conection = sqlite3.connect("agenda.db")
                cursor = conection.cursor()
                personas = cursor.execute("select * from personas where id_persona = ?;", (id_persona,))
                respuesta = {"persona": personas.fetchone(), "error": None, "error_message": "Por favor, llena todos los campos"}
                conection.close()
                return render.editar(respuesta)
            
            # Validación: verificar formato de email (nombre@email.com)
            email = form.email.strip()
            if not email.endswith("@email.com") or email == "@email.com":
                print("Error: Formato de email incorrecto en edición")
                # Recargar la página de edición si el formato es incorrecto
                conection = sqlite3.connect("agenda.db")
                cursor = conection.cursor()
                personas = cursor.execute("select * from personas where id_persona = ?;", (id_persona,))
                respuesta = {"persona": personas.fetchone(), "error": None, "error_message": "Email incorrecto. Debe terminar en @email.com"}
                conection.close()
                return render.editar(respuesta)
            
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            sql = "UPDATE personas SET nombre = ?, email = ? WHERE id_persona = ?;"
            data = (form.nombre.strip(), email, id_persona)
            cursor.execute(sql, data)
            conection.commit()
            conection.close()
            return web.seeother("/")
        except sqlite3.OperationalError as error:
            print(f"Error 006: {error.args[0]}")
            # En caso de error, mostrar mensaje en la página de edición
            respuesta = {
                "persona": None,
                "error": "Error al conectar con la base de datos"
            }
            return render.editar(respuesta)
        except Exception as error:
            print(f"Error conexión editar POST: {error.args[0]}")
            respuesta = {
                "persona": None,
                "error": "Error al conectar con la base de datos"
            }
            return render.editar(respuesta)


class Borrar:
    def GET(self, id_persona):
        try:
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            sql = "select * from personas where id_persona = ?;"
            datos = (id_persona,)
            personas = cursor.execute(sql, datos)
            
            respuesta = {
                "persona": personas.fetchone(),
                "error": None
            }
            conection.close()
            return render.borrar(respuesta)
        except sqlite3.OperationalError as error:
            print(f"Error 007: {error.args[0]}")
            respuesta = {
                "persona": None,
                "error": "Error al conectar con la base de datos"
            }
            return render.borrar(respuesta)
        except Exception as error:
            print(f"Error conexión borrar: {error.args[0]}")
            respuesta = {
                "persona": None,
                "error": "Error al conectar con la base de datos"
            }
            return render.borrar(respuesta)
    
    def POST(self, id_persona):
        try:
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            sql = "DELETE FROM personas WHERE id_persona = ?;"
            cursor.execute(sql, (id_persona,))
            conection.commit()
            conection.close()
            print(f"Persona con ID {id_persona} borrada exitosamente")
            return web.seeother("/")
        except sqlite3.OperationalError as error:
            print(f"Error 008: {error.args[0]}")
            respuesta = {
                "persona": None,
                "error": "Error al conectar con la base de datos"
            }
            return render.borrar(respuesta)
        except Exception as error:
            print(f"Error conexión borrar POST: {error.args[0]}")
            respuesta = {
                "persona": None,
                "error": "Error al conectar con la base de datos"
            }
            return render.borrar(respuesta)


application = app.wsgifunc()


if __name__ == "__main__":
    app.run()