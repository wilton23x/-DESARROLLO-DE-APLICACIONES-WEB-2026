from flask import Flask, render_template, request, redirect, url_for, flash
from conexion.conexion import obtener_conexion
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secreto123"

# =========================
# MODELO USUARIO
# =========================
class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, email, password):
        self.id = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password

# =========================
# LOGIN MANAGER
# =========================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# =========================
# CARGAR USUARIO
# =========================
@login_manager.user_loader
def load_user(user_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conexion.close()

    if user:
        return Usuario(
            user["id_usuario"],
            user["nombre"],
            user["email"],
            user["password"]
        )
    return None

# =========================
# REGISTRO
# =========================
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # VALIDAR EMAIL
        cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        existe = cursor.fetchone()

        if existe:
            flash("El correo ya está registrado")
            return redirect(url_for("registro"))

        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s,%s,%s)",
            (nombre, email, password)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

        flash("Usuario registrado correctamente")
        return redirect(url_for("login"))

    return render_template("usuarios/form.html")

# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conexion.close()

        if user and check_password_hash(user["password"], password):
            usuario = Usuario(
                user["id_usuario"],
                user["nombre"],
                user["email"],
                user["password"]
            )
            login_user(usuario)
            return redirect(url_for("lista_productos"))
        else:
            flash("Correo o contraseña incorrectos")

    return render_template("usuarios/login.html")

# =========================
# LOGOUT
# =========================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada")
    return redirect(url_for("login"))

# =========================
# INICIO
# =========================
@app.route("/")
def inicio():
    return render_template("index.html")

# =========================
# CONTACTOS
# =========================
@app.route("/contactos", methods=["GET", "POST"])
def contactos():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        mensaje = request.form["mensaje"]

        print("Nuevo mensaje:")
        print(nombre, correo, mensaje)

        flash("Mensaje enviado correctamente ✅")
        return redirect(url_for("contactos"))

    return render_template("contactos.html")

# =========================
# DATOS
# =========================
@app.route("/datos")
def datos_archivos():
    return render_template("datos.html")

# =========================
# PRODUCTOS
# =========================
@app.route("/productos")
@login_required
def lista_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("productos/lista.html", productos=productos)

# =========================
# NUEVO PRODUCTO
# =========================
@app.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        autor = request.form["autor"]
        cantidad = int(request.form["cantidad"])
        precio = float(request.form["precio"])

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO productos (nombre, autor, cantidad, precio)
            VALUES (%s, %s, %s, %s)
        """, (nombre, autor, cantidad, precio))

        conexion.commit()
        cursor.close()
        conexion.close()

        flash("Producto agregado correctamente")
        return redirect(url_for("lista_productos"))

    return render_template("productos/form.html", producto=None)

# =========================
# EDITAR
# =========================
@app.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.form["nombre"]
        autor = request.form["autor"]
        cantidad = int(request.form["cantidad"])
        precio = float(request.form["precio"])

        cursor.execute("""
            UPDATE productos
            SET nombre=%s, autor=%s, cantidad=%s, precio=%s
            WHERE id=%s
        """, (nombre, autor, cantidad, precio, id))

        conexion.commit()
        cursor.close()
        conexion.close()

        flash("Producto actualizado")
        return redirect(url_for("lista_productos"))

    cursor.execute("SELECT * FROM productos WHERE id=%s", (id,))
    producto = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template("productos/form.html", producto=producto)

# =========================
# ELIMINAR
# =========================
@app.route("/eliminar/<int:id>")
@login_required
def eliminar_producto(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE id=%s", (id,))
    conexion.commit()

    cursor.close()
    conexion.close()

    flash("Producto eliminado")
    return redirect(url_for("lista_productos"))

# =========================
# BUSCAR
# =========================
@app.route("/buscar")
@login_required
def buscar_producto():
    nombre = request.args.get("nombre", "")

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos WHERE nombre LIKE %s", ("%" + nombre + "%",))
    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("buscar.html", productos=productos)

# =========================
# USUARIOS
# =========================
@app.route("/usuarios")
@login_required
def usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT id_usuario, nombre, email FROM usuarios")
    datos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("usuarios/list.html", usuarios=datos)

# =========================
# EJECUTAR
# =========================
if __name__ == "__main__":
    app.run(debug=True)