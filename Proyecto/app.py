from Proyecto.models import Producto, Inventario
from flask import Flask, render_template, request, redirect, g
import sqlite3
import os

app = Flask(__name__)

# ==========================
# CONFIGURACIÓN BASE DE DATOS
# ==========================

DATABASE = os.path.join('instance', 'biblioteca.db')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
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

# Crear carpeta instance si no existe
if not os.path.exists('instance'):
    os.makedirs('instance')

with app.app_context():
    crear_tabla()

# ==========================
# RUTAS PRINCIPALES
# ==========================

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/contactos")
def contactos():
    return render_template("contactos.html")

@app.route("/about")
def about():
    return render_template("about.html")

# ==========================
# CRUD PRODUCTOS
# ==========================

# READ - Mostrar productos usando POO + Colecciones
@app.route("/productos")
def lista_productos():
    db = get_db()
    rows = db.execute("SELECT * FROM productos").fetchall()

    inventario = Inventario()

    # Convertimos registros SQLite en objetos Producto
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

    return render_template("productos/listproducts.html", productos=productos)


# CREATE - Nuevo producto
@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        autor = request.form["autor"]
        cantidad = request.form["cantidad"]
        precio = request.form["precio"]

        db = get_db()
        db.execute(
            "INSERT INTO productos (nombre, autor, cantidad, precio) VALUES (?, ?, ?, ?)",
            (nombre, autor, cantidad, precio)
        )
        db.commit()

        return redirect("/productos")

    return render_template("productos/form.html")


# DELETE - Eliminar producto
@app.route("/productos/eliminar/<int:id>")
def eliminar_producto(id):
    db = get_db()
    db.execute("DELETE FROM productos WHERE id = ?", (id,))
    db.commit()
    return redirect("/productos")


# UPDATE - Editar producto
@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
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

    return render_template("productos/form.html", producto=producto)


# ==========================
# BUSCAR PRODUCTO (Submenú requerido)
# ==========================

@app.route("/productos/buscar", methods=["GET", "POST"])
def buscar_producto():
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

    resultados = []

    if request.method == "POST":
        nombre = request.form["nombre"]
        resultados = inventario.buscar_por_nombre(nombre)

    return render_template("productos/buscar.html", productos=resultados)


# ==========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)