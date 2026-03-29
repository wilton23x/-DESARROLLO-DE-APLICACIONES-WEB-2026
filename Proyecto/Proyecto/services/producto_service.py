from conexion.conexion import obtener_conexion

def listar_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos")
    datos = cursor.fetchall()

    conexion.close()
    return datos


def insertar_producto(nombre, autor, cantidad, precio):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO productos (nombre, autor, cantidad, precio) VALUES (%s, %s, %s, %s)",
        (nombre, autor, cantidad, precio)
    )

    conexion.commit()
    conexion.close()


def obtener_producto(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    # ✅ CORREGIDO
    cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
    dato = cursor.fetchone()

    conexion.close()
    return dato


def actualizar_producto(id, nombre, autor, cantidad, precio):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # ✅ CORREGIDO
    cursor.execute(
        "UPDATE productos SET nombre=%s, autor=%s, cantidad=%s, precio=%s WHERE id=%s",
        (nombre, autor, cantidad, precio, id)
    )

    conexion.commit()
    conexion.close()


def eliminar_producto(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # CORREGIDO
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))

    conexion.commit()
    conexion.close()


def buscar_productos(nombre):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos WHERE nombre LIKE %s", (f"%{nombre}%",))
    datos = cursor.fetchall()

    conexion.close()
    return datos