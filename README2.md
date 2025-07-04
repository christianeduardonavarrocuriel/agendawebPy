# Agenda Web.py - Mejoras Implementadas

Guía simple de las mejoras agregadas a la aplicación de agenda web.

## 🎯 ¿Qué se agregó?

### ✅ Funcionalidades Nuevas
- **Editar personas**: Ahora puedes modificar nombre y email
- **Borrar personas**: Eliminar registros con confirmación
- **Botones "Regresar"**: En todas las páginas para navegar fácil
- **No campos vacíos**: Ya no se pueden guardar registros sin datos

## 📝 Cambios en Cada Archivo

### 🔧 main.py (El cerebro de la aplicación)

**Lo que se agregó:**
- **Nueva ruta**: `/editar` y `/borrar` para que funcionen los botones
- **Validación**: Si alguien deja campos vacíos, no se guarda nada
- **Clases nuevas**: `Editar` y `Borrar` para manejar estas acciones

**Tips importantes:**
- `if not form.nombre.strip()` → Revisa si el campo está vacío
- `required` en HTML → El navegador no deja enviar formularios vacíos
- `UPDATE` y `DELETE` → Comandos SQL para modificar y borrar

### 🎨 Templates HTML (Lo que ve el usuario)

#### insertar.html y editar.html
**Cambio clave:** Se agregó `required` a los campos
```html
<input type="text" name="nombre" required>
<input type="email" name="email" required>
```
**¿Por qué?** Para que no se puedan enviar campos vacíos

#### detalle.html, insertar.html, editar.html
**Cambio clave:** Botón "Regresar" en todas las páginas
```html
<a href="/">
    <button type="button">Regresar</button>
</a>
```
**¿Por qué?** Para que el usuario pueda volver atrás fácilmente

#### borrar.html (Nuevo archivo)
**Lo que hace:** Pregunta "¿Estás seguro?" antes de borrar
**¿Por qué?** Para evitar borrar personas por accidente

## 🚫 Principales Problemas Solucionados

### ❌ "Not Found" al presionar Editar
**Problema:** El botón no funcionaba
**Solución:** Agregar la ruta `/editar` en main.py

### ❌ Registros vacíos en la base de datos
**Problema:** Se podían guardar personas sin nombre o email
**Solución:** Validación con `required` en HTML y verificación en Python

### ❌ Sin navegación
**Problema:** Una vez en una página, era difícil regresar
**Solución:** Botones "Regresar" en todas las páginas

## 💡 Conceptos Simples Explicados

### ¿Qué es `required`?
- Se pone en los campos de formulario
- El navegador no deja enviar si está vacío
- Es como un "guardián" que dice "¡Hey! Llena este campo"

### ¿Qué hace `.strip()`?
- Elimina espacios en blanco al inicio y final
- Ejemplo: "  Juan  " se convierte en "Juan"
- Útil para detectar si alguien solo puso espacios

### ¿Para qué sirven las rutas?
- Le dicen a la aplicación qué hacer cuando alguien va a una dirección
- `/editar/123` → "Ve a editar la persona con ID 123"
- Sin ruta = "Not Found" (página no encontrada)

## 🎯 Resultado Final

Ahora la aplicación es completamente funcional:
- ✅ Crear nuevas personas (con validación)
- ✅ Ver lista y detalles
- ✅ Editar información existente
- ✅ Borrar con confirmación
- ✅ Navegación fácil entre páginas

## 🚀 Para Usar la Aplicación

1. **Crear base de datos:** `sqlite3 agenda.db < ../sql/agenda.sql`
2. **Instalar dependencias:** `pip install -r requirements.txt`  
3. **Ejecutar:** `sudo waitress-serve --port=80 main:application`
4. **Abrir navegador:** `http://localhost`

¡Y listo! Tu agenda web funciona perfectamente 🎉

---

## Sección Original del README.md

## 9. Cómo Agregar la Funcionalidad de "Editar"

### Error "Not Found" al presionar Editar
**Problema:** Aparecía "Not Found" porque faltaba implementar la ruta `/editar` en la aplicación.

**Solución:**

1. **Agregar ruta en main.py:**
```python
urls = (
    "/", "Index",
    "/insertar","Insertar", 
    "/detalle/(.*)", "Detalle",
    "/editar/(.*)", "Editar"    # ← Agregar esta línea
    )
```

2. **Crear clase Editar en main.py:**
```python
class Editar:
    def GET(self, id_persona):
        conection = sqlite3.connect("agenda.db")
        cursor = conection.cursor()
        personas = cursor.execute("select * from personas where id_persona = ?;", (id_persona,))
        respuesta = {"persona": personas.fetchone(), "error": None}
        conection.close()
        return render.editar(respuesta)
    
    def POST(self, id_persona):
        form = web.input()
        conection = sqlite3.connect("agenda.db")
        cursor = conection.cursor()
        cursor.execute("UPDATE personas SET nombre = ?, email = ? WHERE id_persona = ?;", 
                      (form.nombre, form.email, id_persona))
        conection.commit()
        conection.close()
        return web.seeother("/")
```

3. **Crear templates/editar.html:**
```html
$def with (respuesta={})
<!DOCTYPE html>
<html lang="es">
    <head><title>SQLITE demo</title></head>
    <body>
        <h1>Editar Persona</h1>
        <form method="POST">
            $ nombre = '%s' % respuesta['persona'][1]
            $ email = '%s' % respuesta['persona'][2]
            <label>Nombre</label>
            <input type="text" name="nombre" value=$nombre><br>
            <label>Email</label>
            <input type="text" name="email" value=$email><br>
            <input type="submit" value="Actualizar">
            <a href="/"><button type="button">Regresar</button></a>
        </form>
    </body>
</html>
```

¡Listo! Ahora funciona el botón "Editar".
