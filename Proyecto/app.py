from flask import Flask, render_template, request, redirect, url_for
from Proyecto.models import Producto, Inventario
from conexion.conexion import obtener_conexion

import json
import csv

app = Flask(__name__)

# =========================
# INVENTARIO EN MEMORIA
# =========================
inventario = Inventario()


# =========================
# CARGAR CSV Y GUARDAR EN BD
# =========================
def cargar_csv():

    try:

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        with open("datos.csv", newline="", encoding="utf-8") as archivo:

            lector = csv.DictReader(archivo)

            for fila in lector:

                id = int(fila["id"])
                nombre = fila["nombre"]
                autor = fila["autor"]
                categoria = fila["categoria"]
                precio = float(fila["precio"])

                # Guardar en inventario
                producto = Producto(id, nombre, autor, 1, precio)
                inventario.agregar_producto(producto)

                # Guardar en base de datos
                sql = """
                INSERT INTO libros (id, nombre, autor, categoria, precio)
                VALUES (%s,%s,%s,%s,%s)
                """

                valores = (id, nombre, autor, categoria, precio)

                try:
                    cursor.execute(sql, valores)
                except:
                    pass

        conexion.commit()
        cursor.close()
        conexion.close()

        print("CSV cargado correctamente")

    except Exception as e:
        print("Error cargando CSV:", e)


# Ejecutar al iniciar
cargar_csv()


# =========================
# PAGINA INICIO
# =========================
@app.route("/")
def inicio():
    return render_template("index.html")


# =========================
# LISTAR PRODUCTOS
# =========================
@app.route("/productos")
def lista_productos():

    productos = inventario.mostrar_todos()

    return render_template(
        "productos/listproducts.html",
        productos=productos
    )


# =========================
# NUEVO PRODUCTO
# =========================
@app.route("/nuevo", methods=["GET", "POST"])
def nuevo_producto():

    if request.method == "POST":

        id = len(inventario.productos) + 1
        nombre = request.form["nombre"]
        autor = request.form["autor"]
        cantidad = int(request.form["cantidad"])
        precio = float(request.form["precio"])

        producto = Producto(id, nombre, autor, cantidad, precio)

        inventario.agregar_producto(producto)

        return redirect(url_for("lista_productos"))

    return render_template("productos/form.html", producto=None)


# =========================
# EDITAR PRODUCTO
# =========================
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):

    producto = inventario.productos.get(id)

    if request.method == "POST":

        producto.nombre = request.form["nombre"]
        producto.autor = request.form["autor"]
        producto.cantidad = int(request.form["cantidad"])
        producto.precio = float(request.form["precio"])

        return redirect(url_for("lista_productos"))

    return render_template(
        "productos/form.html",
        producto=producto
    )


# =========================
# ELIMINAR PRODUCTO
# =========================
@app.route("/eliminar/<int:id>")
def eliminar_producto(id):

    inventario.productos.pop(id, None)

    return redirect(url_for("lista_productos"))


# =========================
# BUSCAR PRODUCTO
# =========================
@app.route("/buscar", methods=["GET"])
def buscar_producto():

    nombre = request.args.get("nombre", "")

    productos = inventario.buscar_por_nombre(nombre) if nombre else []

    return render_template(
        "buscar.html",
        productos=productos
    )


# =========================
# LISTAR USUARIOS
# =========================
@app.route("/usuarios")
def usuarios():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuarios")
    datos = cursor.fetchall()

    usuarios = []

    for fila in datos:
        usuario = {
            "id": fila[0],
            "nombre": fila[1],
            "mail": fila[2]
        }
        usuarios.append(usuario)

    cursor.close()
    conexion.close()

    return render_template("usuarios.html", usuarios=usuarios)


# =========================
# CONTACTO
# =========================
@app.route("/contacto", methods=["GET", "POST"])
def contactos():

    if request.method == "POST":

        nombre = request.form["nombre"]
        correo = request.form["correo"]
        mensaje = request.form["mensaje"]

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO usuarios (nombre, mail, password)
        VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (nombre, correo, mensaje))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("inicio"))

    return render_template("contactos.html")


# =========================
# LECTURA DE ARCHIVOS
# =========================
@app.route("/datos")
def datos_archivos():

    txt = []
    try:
        with open("datos.txt", "r", encoding="utf-8") as f:
            txt = f.readlines()
    except:
        txt = ["No hay archivo TXT"]

    json_datos = []
    try:
        with open("datos.json", "r", encoding="utf-8") as f:
            json_datos = json.load(f)
    except:
        json_datos = []

    csv_datos = []
    try:
        with open("datos.csv", newline="", encoding="utf-8") as f:
            lector = csv.reader(f)
            for fila in lector:
                csv_datos.append(fila)
    except:
        csv_datos = []

    return render_template(
        "datos.html",
        txt=txt,
        json_datos=json_datos,
        csv_datos=csv_datos
    )


# =========================
# EJECUTAR APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)