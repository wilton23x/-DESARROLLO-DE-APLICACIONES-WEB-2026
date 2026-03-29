import mysql.connector

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="desarrollo_web"
        )
        return conexion

    except mysql.connector.Error as err:
        print(f" Error de conexión a MySQL: {err}")
        return None