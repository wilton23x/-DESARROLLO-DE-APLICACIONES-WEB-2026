from models import Producto, Inventario
from flask import Flask, render_template, request, redirect, g
import sqlite3
import os
import json
import csv

app = Flask(__name__)

# ==========================
# PERSISTENCIA EN ARCHIVOS
# ==========================

def guardar_txt(nombre, autor, cantidad, precio):
    with open("data/datos.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"{nombre},{autor},{cantidad},{precio}\n")


def guardar_json(nombre, autor, cantidad, precio):

    producto = {
        "nombre": nombre,
        "autor": autor,
        "cantidad": cantidad,
        "precio": precio
    }

    try:
        with open("data/datos.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except:
        datos = []

    datos.append(producto)

    with open("data/datos.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4)


def guardar_csv(nombre, autor, cantidad, precio):
    with open("data/datos.csv", "a", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow([nombre, autor, cantidad, precio])


# ==========================
# LECTURA DE ARCHIVOS
# ==========================

def leer_txt():

    datos = []

    try:
        with open("data/datos.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos.append(linea.strip().split(","))
    except:
        pass

    return datos


def leer_json():

    try:
        with open("data/datos.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except:
        datos = []

    return datos


def leer_csv():

    datos = []

    try:
        with open("data/datos.csv", "r", encoding="utf-8") as archivo:
            reader = csv.reader(archivo)

            for fila in reader:
                datos.append(fila)
    except:
        pass

    return datos


# ==========================
# BASE DE DATOS SQLITE
# ==========================

DATABASE = os.path.join("instance", "biblioteca.db")


def get_db():

    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row

    return g.db


@app.teardown_appcontext
def close_db(error):

    db = g.pop("db", None)

    if db is not None:
        db.close()


def crear_tabla():

    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            autor TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    """)

    db.commit()


# ==========================
# CREAR CARPETAS NECESARIAS
# ==========================

if not os.path.exists("instance"):
    os.makedirs("instance")

if not os.path.exists("data"):
    os.makedirs("data")

with app.app_context():
    crear_tabla()


# ==========================
# RUTAS PRINCIPALES
# ==========================

# ==========================
# RUTAS PRINCIPALES
# ==========================

@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/buscar")
def buscar_producto():
    return render_template("buscar.html")


@app.route("/contactos", methods=["GET","POST"])
def contactos():

    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        mensaje = request.form["mensaje"]

        print(nombre, correo, mensaje)

        return redirect("/")

    return render_template("contactos.html")


@app.route("/about")
def about():
    return render_template("about.html")

# ==========================
# CRUD PRODUCTOS
# ==========================

# LISTAR PRODUCTOS
@app.route("/productos")
def lista_productos():

    db = get_db()

    rows = db.execute("SELECT * FROM productos").fetchall()

    inventario = Inventario()

    for row in rows:

        producto = Producto(
            row["id"],
            row["nombre"],
            row["autor"],
            row["cantidad"],
            row["precio"]
        )

        inventario.agregar_producto(producto)

    productos = inventario.mostrar_todos()

    return render_template(
        "productos/listproducts.html",
        productos=productos
    )


# CREAR PRODUCTO
@app.route("/productos/nuevo", methods=["GET","POST"])
def nuevo_producto():

    if request.method == "POST":

        nombre = request.form["nombre"]
        autor = request.form["autor"]
        cantidad = request.form["cantidad"]
        precio = request.form["precio"]

        db = get_db()

        db.execute(
            """
            INSERT INTO productos
            (nombre, autor, cantidad, precio)
            VALUES (?, ?, ?, ?)
            """,
            (nombre, autor, cantidad, precio)
        )

        db.commit()

        guardar_txt(nombre, autor, cantidad, precio)
        guardar_json(nombre, autor, cantidad, precio)
        guardar_csv(nombre, autor, cantidad, precio)

        return redirect("/productos")

    return render_template("productos/form.html")


# EDITAR PRODUCTO
@app.route("/productos/editar/<int:id>", methods=["GET","POST"])
def editar_producto(id):

    db = get_db()

    if request.method == "POST":

        nombre = request.form["nombre"]
        autor = request.form["autor"]
        cantidad = request.form["cantidad"]
        precio = request.form["precio"]

        db.execute("""
            UPDATE productos
            SET nombre=?, autor=?, cantidad=?, precio=?
            WHERE id=?
        """, (nombre, autor, cantidad, precio, id))

        db.commit()

        return redirect("/productos")

    producto = db.execute(
        "SELECT * FROM productos WHERE id=?",
        (id,)
    ).fetchone()

    return render_template(
        "productos/form.html",
        producto=producto
    )


# ELIMINAR PRODUCTO
@app.route("/productos/eliminar/<int:id>")
def eliminar_producto(id):

    db = get_db()

    db.execute(
        "DELETE FROM productos WHERE id=?",
        (id,)
    )

    db.commit()

    return redirect("/productos")


# ==========================
# MOSTRAR DATOS DE ARCHIVOS
# ==========================

@app.route("/datos")
def ver_datos():

    txt = leer_txt()
    json_datos = leer_json()
    csv_datos = leer_csv()

    return render_template(
        "datos.html",
        txt=txt,
        json_datos=json_datos,
        csv_datos=csv_datos
    )


# ==========================

if __name__ == "__main__":
    app.run(debug=True)