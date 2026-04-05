from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.pdfgen import canvas
import io
import os

from models.usuario import Usuario

from services.usuario_service import (
    obtener_usuario_por_id,
    obtener_usuario_por_email,
    insertar_usuario,
    obtener_usuarios
)

from services.producto_service import (
    listar_productos,
    insertar_producto,
    actualizar_producto,
    eliminar_producto,
    obtener_producto,
    buscar_productos
)

from forms.producto_form import ProductoForm

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)
app.secret_key = "clave_super_segura_2026"

# =========================
# LOGIN MANAGER
# =========================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# =========================
# USER LOADER
# =========================
@login_manager.user_loader
def load_user(user_id):
    user = obtener_usuario_por_id(user_id)
    if user:
        return Usuario(
            user["id_usuario"],
            user["nombre"],
            user["email"],
            user["password"]
        )
    return None


# =========================
# HOME
# =========================
@app.route('/')
def inicio():
    return render_template('index.html')
# =========================
# REGISTRO
# =========================
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":

        nombre = request.form["nombre"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        if obtener_usuario_por_email(email):
            flash("El correo ya está registrado")
            return redirect(url_for("registro"))

        insertar_usuario(nombre, email, password)
        flash("Usuario registrado correctamente")
        return redirect(url_for("login"))

    return render_template("usuarios/form.html")


# =========================
# LOGIN
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = obtener_usuario_por_email(email)

        if user and check_password_hash(user['password'], password):

            usuario = Usuario(
                user['id_usuario'],
                user['nombre'],
                user['email'],
                user['password']
            )

            login_user(usuario)

            return redirect(url_for('inicio'))

        flash("Usuario o contraseña incorrectos")

    return render_template('usuarios/login.html')
# =========================
# LOGOUT
# =========================
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
# =========================
# PRODUCTOS
# =========================
@app.route("/productos")
@login_required
def ver_productos():
    productos = listar_productos()
    return render_template("productos/lista.html", productos=productos)


@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():

    if request.method == "POST":

        try:
            insertar_producto(
                request.form["nombre"],
                request.form["autor"],
                int(request.form["cantidad"]),
                float(request.form["precio"])
            )

            flash("Producto agregado correctamente")
            return redirect(url_for("ver_productos"))

        except Exception as e:
            print(e)
            flash("Error al guardar producto")
            return redirect(url_for("nuevo_producto"))

    return render_template("productos/form.html", producto=None)


@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):

    if request.method == "POST":

        form = ProductoForm(request.form)
        errores = form.validar()

        if errores:
            for e in errores:
                flash(e)
            return redirect(url_for("editar_producto", id=id))

        actualizar_producto(
            id,
            form.nombre,
            form.autor,
            int(form.cantidad or 0),
            float(form.precio)
        )

        flash("Producto actualizado")
        return redirect(url_for("ver_productos"))

    producto = obtener_producto(id)
    return render_template("productos/form.html", producto=producto)


@app.route("/productos/eliminar/<int:id>")
@login_required
def eliminar_producto_route(id):
    eliminar_producto(id)
    flash("Producto eliminado")
    return redirect(url_for("ver_productos"))


@app.route("/productos/buscar")
@login_required
def buscar_producto():

    nombre = request.args.get("nombre")

    if nombre:
        productos = buscar_productos(nombre)
    else:
        productos = None

    return render_template("productos/buscar.html", productos=productos)


# =========================
# PDF
# =========================
@app.route("/productos/pdf")
@login_required
def exportar_pdf():

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    productos = listar_productos()

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(180, 800, "REPORTE DE PRODUCTOS")

    pdf.setFont("Helvetica-Bold", 12)
    y = 760

    pdf.drawString(50, y, "ID")
    pdf.drawString(80, y, "Nombre")
    pdf.drawString(200, y, "Autor")
    pdf.drawString(320, y, "Cantidad")
    pdf.drawString(400, y, "Precio")

    pdf.setFont("Helvetica", 10)
    y -= 20

    for p in productos:

        pdf.drawString(50, y, str(p.get("id_producto", p.get("id"))))
        pdf.drawString(80, y, p["nombre"])
        pdf.drawString(200, y, p["autor"])
        pdf.drawString(320, y, str(p["cantidad"]))
        pdf.drawString(400, y, "$" + str(p["precio"]))

        y -= 20

        if y < 50:
            pdf.showPage()
            y = 800

    pdf.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="reporte_productos.pdf")


# =========================
# USUARIOS
# =========================
@app.route("/usuarios")
@login_required
def usuarios():
    datos = obtener_usuarios()
    return render_template("usuarios/lista.html", usuarios=datos)


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)