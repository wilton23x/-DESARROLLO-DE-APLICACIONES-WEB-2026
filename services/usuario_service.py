from conexion.conexion import obtener_conexion

def obtener_usuario_por_email(email):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    usuario = cursor.fetchone()

    conexion.close()
    return usuario


def obtener_usuario_por_id(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id,))
    usuario = cursor.fetchone()

    conexion.close()
    return usuario


def insertar_usuario(nombre, email, password):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
        (nombre, email, password)
    )

    conexion.commit()
    conexion.close()


# ✅ CORREGIDO
def obtener_usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios")
    datos = cursor.fetchall()

    conexion.close()
    return datos